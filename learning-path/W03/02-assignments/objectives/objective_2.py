# ============================================================================
# OBJECTIVE 2: GENERATE CUSTOM Q&A DATABASES
# ============================================================================
#
# LEARNING OBJECTIVES DEMONSTRATED:
#   1. Q&A Generation - Using LLMs to create domain-specific knowledge bases
#   2. Modular Design - SOLID, KISS, DRY principles in practice
#   3. Component Reuse - 100% reuse of InferenceEngine and env from previous objectives
#
# THEORETICAL BACKGROUND:
#   Q&A databases serve as the knowledge base for RAG systems, providing:
#   - Domain-specific content aligned with business context
#   - Answerable questions (within knowledge base)
#   - Unanswerable questions (outside knowledge base) for testing refusal behavior
#
# ============================================================================

import os
import json
from typing import List, Dict, Optional
import pandas as pd

# ============================================================================
# QADatabaseGenerator Class - Centralized Objective 2 Logic
# ============================================================================
class QADatabaseGenerator:
    """
    Q&A database generation for Objective 2.
    Focuses ONLY on Q&A generation, parsing, and file I/O.
    Uses InferenceEngine from Objective 1 and env from Objective 0 - 100% reuse!
    
    Usage:
        generator = QADatabaseGenerator(env, inference_engine, system_prompt)
        qa_database = generator.generate_full_database()
    """
    
    # Configuration constants
    TEMPERATURE = 0.7
    TOP_P = 0.9
    CONTEXT_CHARS = 900  # Smaller excerpt increases relevance
    OUTPUT_DIR = "data/qa_database"
    
    # Category definitions
    QA_CATEGORIES = [
        ("products", "types of products, solar panels, smart devices, eco-friendly items"),
        ("shipping", "delivery times, shipping cost, free shipping threshold, tracking"),
        ("returns", "return policy, refund window, 30-day policy, conditions"),
        ("customer_service", "hours (Mon–Fri 9–6, Sat 10–4), email, phone support"),
        ("warranty", "coverage periods 1–3 years, claims process"),
        ("orders", "order status, modifying or cancelling orders, tracking numbers"),
    ]
    
    UNANSWERABLE_TYPES = [
        ("competitor", "questions about competitor prices or product comparisons"),
        ("personal_advice", "questions asking for personal recommendations or opinions"),
        ("future_events", "questions about upcoming sales or unreleased products"),
    ]
    
    PAIRS_PER_CATEGORY = 3
    UNANSWERABLE_PER_TYPE = 1
    
    # Prompt templates
    ANSWERABLE_PROMPT = """
You are generating REALISTIC customer service Q&A pairs for the ShopSmart e-commerce support assistant.

Generate EXACTLY {num_pairs} Q&A pairs about the topic below.

TOPIC FOCUS:
{description}

BUSINESS CONTEXT (from system prompt):
{context}

CRITICAL: You MUST output valid JSON only. No other text before or after.

OUTPUT FORMAT (JSON array):
[
  {{"question": "What is your shipping policy?", "answer": "We offer standard shipping (5-7 business days) for free on orders over $75. Express shipping (2-3 business days) is available for an additional $15. All orders are shipped with tracking numbers."}},
  {{"question": "Can I return a product if I'm not satisfied?", "answer": "Yes, you can return any unopened item in its original packaging within 30 days of delivery for a full refund. Simply contact our support team to initiate the return process."}},
  {{"question": "What are your customer service hours?", "answer": "Our customer service team is available Monday through Friday from 9 AM to 6 PM EST, and on Saturdays from 10 AM to 4 PM EST. You can reach us via email at support@greentechmarketplace.com or by phone."}}
]

CONTENT RULES:
- Questions MUST sound like real customers asking natural questions.
- Answers MUST be 2–3 sentences with concrete details (times, numbers, policies, contact info).
- Stay entirely within ShopSmart policies from the business context.
- DO NOT hallucinate unsupported information.

OUTPUT: Return a valid JSON array with EXACTLY {num_pairs} objects, each with "question" and "answer" fields.
"""
    
    UNANSWERABLE_PROMPT = """
Generate EXACTLY {num_pairs} UNANSWERABLE customer Q&A pairs.

TOPIC TYPE OUT OF SCOPE:
{description}

CRITICAL: You MUST output valid JSON only. No other text before or after.

OUTPUT FORMAT (JSON array):
[
  {{"question": "What are your competitor's prices?", "answer": "I'm sorry, but I'm unable to provide information about competitor pricing as it's outside our knowledge base. However, I'd be happy to help you with questions about our own products, shipping options, or return policies."}},
  {{"question": "Can you recommend the best restaurant in New York?", "answer": "I apologize, but I cannot provide personal recommendations or advice about restaurants as that's beyond ShopSmart's scope. I can assist you with questions about our products, shipping, returns, or order tracking."}},
  {{"question": "When will you release new products next month?", "answer": "I'm unable to provide information about upcoming product releases or future events as that information isn't available in our knowledge base. However, I can help you with questions about our current product catalog, shipping options, or warranty information."}}
]

REFUSAL RULES:
- Question MUST be outside ShopSmart's knowledge base (competitor info, personal advice, future events, etc.)
- Answer MUST politely decline and explain you cannot provide that information
- Answer MUST offer what you *can* help with (shipping, returns, products, warranty, orders, etc.)
- Answer MUST be 2 sentences

OUTPUT: Return a valid JSON array with EXACTLY {num_pairs} objects, each with "question" and "answer" fields.
"""
    
    def __init__(self, env, inference_engine, system_prompt: str):
        """
        Initialize with environment config, inference engine, and system prompt.
        
        Args:
            env: EnvironmentConfig instance from Objective 0
            inference_engine: InferenceEngine instance from Objective 1
            system_prompt: System prompt from Objective 1
        """
        self.env = env
        self.inference_engine = inference_engine
        self.system_prompt = system_prompt
        self.qa_database = []
        
        # Create output directory
        os.makedirs(self.OUTPUT_DIR, exist_ok=True)
        
        # Calculate totals
        self.ANSWERABLE_TOTAL = len(self.QA_CATEGORIES) * self.PAIRS_PER_CATEGORY
        self.UNANSWERABLE_TOTAL = len(self.UNANSWERABLE_TYPES) * self.UNANSWERABLE_PER_TYPE
        self.TOTAL_PAIRS = self.ANSWERABLE_TOTAL + self.UNANSWERABLE_TOTAL
    
    
    
    def _parse_qa_json(self, text: str, answerable: bool, debug: bool = False) -> List[Dict]:
        """
        Parse Q&A pairs from model output.
        Expected format: JSON array with objects containing "question" and "answer" fields.
        
        Args:
            text: Model output text
            answerable: Whether these are answerable pairs
            debug: Enable debug output
            
        Returns:
            List of Q&A dictionaries
        """
        qa_list = []
        
        if debug:
            print(f"      [DEBUG] Raw model output ({len(text)} chars):")
            print(f"      {repr(text[:300])}...")
        
        # Try to extract JSON from the text (might have extra text before/after)
        text_clean = text.strip()
        
        # Find JSON array in the text (handle cases where model adds extra text)
        json_start = text_clean.find('[')
        json_end = text_clean.rfind(']') + 1
        
        if json_start == -1 or json_end == 0:
            if debug:
                print(f"      [DEBUG] No JSON array found in output")
            return qa_list
        
        json_text = text_clean[json_start:json_end]
        
        try:
            parsed_data = json.loads(json_text)
            
            if not isinstance(parsed_data, list):
                if debug:
                    print(f"      [DEBUG] JSON is not an array, got: {type(parsed_data)}")
                return qa_list
            
            for item in parsed_data:
                if isinstance(item, dict) and "question" in item and "answer" in item:
                    q = item["question"].strip()
                    a = item["answer"].strip()
                    
                    # Validate content
                    if q and a and len(q) > 3 and len(a) > 10:
                        qa_list.append({
                            "question": q,
                            "answer": a,
                            "answerable": bool(answerable)
                        })
            
            if debug:
                print(f"      [DEBUG] Parsed {len(qa_list)} pairs from JSON")
                if len(qa_list) > 0:
                    print(f"      [DEBUG] First parsed pair:")
                    print(f"        Q: {qa_list[0]['question'][:80]}...")
                    print(f"        A: {qa_list[0]['answer'][:80]}...")
        
        except json.JSONDecodeError as e:
            if debug:
                print(f"      [DEBUG] JSON decode error: {e}")
                print(f"      [DEBUG] Attempted to parse: {json_text[:200]}...")
        
        return qa_list
    
    def _generate_answerable(self, category: str, description: str, n: int, max_retries: int = 3) -> List[Dict]:
        """
        Generate answerable Q&A pairs with retry logic if parsing fails.
        
        Args:
            category: Category name
            description: Category description
            n: Number of pairs to generate
            max_retries: Maximum retry attempts
            
        Returns:
            List of Q&A dictionaries
        """
        for attempt in range(max_retries):
            prompt = self.ANSWERABLE_PROMPT.format(
                num_pairs=n,
                description=description,
                context=self.system_prompt[:self.CONTEXT_CHARS]
            )
            formatted_prompt = SystemPromptEngineer.format_template(prompt)
            # Load model (cached from Objective 1)
            tokenizer, model = self.inference_engine.load_model("mistralai/Mistral-7B-Instruct-v0.3")
            raw = self.inference_engine.generate_response(
                tokenizer, model, formatted_prompt,
                max_new_tokens=800,
                temperature=self.TEMPERATURE,
                top_p=self.TOP_P
            )
            parsed = self._parse_qa_json(raw, True, debug=(attempt == max_retries - 1))
            
            if len(parsed) >= n:
                return parsed[:n]
            elif len(parsed) > 0:
                print(f"      ⚠️  Got {len(parsed)}/{n} pairs (attempt {attempt + 1})")
                if attempt < max_retries - 1:
                    continue
                return parsed
        
        print(f"      ❌ Failed to generate pairs after {max_retries} attempts")
        return []
    
    def _generate_unanswerable(self, category: str, description: str, n: int, max_retries: int = 3) -> List[Dict]:
        """
        Generate unanswerable Q&A pairs with retry logic if parsing fails.
        
        Args:
            category: Category name
            description: Category description
            n: Number of pairs to generate
            max_retries: Maximum retry attempts
            
        Returns:
            List of Q&A dictionaries
        """
        for attempt in range(max_retries):
            prompt = self.UNANSWERABLE_PROMPT.format(
                num_pairs=n,
                description=description
            )
            formatted_prompt = SystemPromptEngineer.format_template(prompt)
            # Load model (cached from Objective 1)
            tokenizer, model = self.inference_engine.load_model("mistralai/Mistral-7B-Instruct-v0.3")
            raw = self.inference_engine.generate_response(
                tokenizer, model, formatted_prompt,
                max_new_tokens=600,
                temperature=self.TEMPERATURE,
                top_p=self.TOP_P
            )
            parsed = self._parse_qa_json(raw, False, debug=(attempt == max_retries - 1))
            
            if len(parsed) >= n:
                return parsed[:n]
            elif len(parsed) > 0:
                print(f"      ⚠️  Got {len(parsed)}/{n} pairs (attempt {attempt + 1})")
                if attempt < max_retries - 1:
                    continue
                return parsed
        
        print(f"      ❌ Failed to generate pairs after {max_retries} attempts")
        return []
    
    def generate_full_database(self) -> List[Dict]:
        """
        Generate complete Q&A database with all categories.
        
        Returns:
            List of Q&A dictionaries with all required fields
        """
        db = []
        
        print("\n📗 Generating answerable Q&A...")
        for cat, desc in self.QA_CATEGORIES:
            print(f"   → {cat}...")
            pairs = self._generate_answerable(cat, desc, self.PAIRS_PER_CATEGORY)
            for p in pairs:
                p["category"] = cat
            db.extend(pairs)
        
        print("\n📕 Generating unanswerable Q&A...")
        for cat, desc in self.UNANSWERABLE_TYPES:
            print(f"   → {cat}...")
            pairs = self._generate_unanswerable(cat, desc, self.UNANSWERABLE_PER_TYPE)
            for p in pairs:
                p["category"] = cat
            db.extend(pairs)
        
        print(f"\n🎉 Generated {len(db)} total pairs "
              f"({self.ANSWERABLE_TOTAL} answerable, {self.UNANSWERABLE_TOTAL} unanswerable)")
        
        self.qa_database = db
        return db
    
    def to_dataframe(self, qa_list: Optional[List[Dict]] = None) -> pd.DataFrame:
        """
        Convert Q&A list to pandas DataFrame with additional metrics.
        
        Args:
            qa_list: Q&A list (uses self.qa_database if None)
            
        Returns:
            DataFrame with Q&A data and metrics
        """
        if qa_list is None:
            qa_list = self.qa_database
        
        df = pd.DataFrame(qa_list)
        df["question_length"] = df.question.str.len()
        df["answer_length"] = df.answer.str.len()
        df["word_count"] = df.answer.str.split().str.len()
        return df
    
    def save_to_csv(self, qa_list: Optional[List[Dict]] = None, filename: str = "qa_database.csv") -> str:
        """
        Save Q&A database to CSV file.
        
        Args:
            qa_list: Q&A list (uses self.qa_database if None)
            filename: Output filename
            
        Returns:
            Path to saved file
        """
        if qa_list is None:
            qa_list = self.qa_database
        
        df = pd.DataFrame(qa_list)
        path = os.path.join(self.OUTPUT_DIR, filename)
        df.to_csv(path, index=False)
        print(f"   💾 Saved to {path}")
        return path
    
    def display_database(self, qa_list: Optional[List[Dict]] = None, max_display: Optional[int] = None):
        """
        Display Q&A pairs in a readable format.
        
        Args:
            qa_list: Q&A list (uses self.qa_database if None)
            max_display: Maximum number of pairs to display
        """
        if qa_list is None:
            qa_list = self.qa_database
        
        print("\n" + "="*70)
        print("📋 GENERATED Q&A DATABASE")
        print("="*70)
        
        if max_display:
            display_list = qa_list[:max_display]
            print(f"\nShowing first {len(display_list)} of {len(qa_list)} pairs:\n")
        else:
            display_list = qa_list
            print(f"\nAll {len(display_list)} pairs:\n")
        
        for i, pair in enumerate(display_list, 1):
            answerable_str = "✅ Answerable" if pair.get("answerable") else "❌ Unanswerable"
            category = pair.get("category", "unknown")
            print(f"\n[{i}] {answerable_str} | Category: {category}")
            print(f"    Q: {pair.get('question', 'N/A')}")
            print(f"    A: {pair.get('answer', 'N/A')[:150]}{'...' if len(pair.get('answer', '')) > 150 else ''}")
        
        if max_display and len(qa_list) > max_display:
            print(f"\n... and {len(qa_list) - max_display} more pairs")
        
        print("\n" + "="*70)
    
    def verify(self) -> bool:
        """
        Verify that Objective 2 completed successfully.
        Checks all variables, counts, structure, and files.
        
        Returns:
            True if verification passes, False otherwise
        """
        print("="*70)
        print("🔍 OBJECTIVE 2 VERIFICATION")
        print("="*70)
        
        errors = []
        warnings = []
        
        # Check if database exists
        if not self.qa_database:
            errors.append("❌ qa_database is empty")
        
        if errors:
            print("\n".join(errors))
            print("="*70)
            return False
        
        # Check count
        actual_count = len(self.qa_database)
        expected_count = self.TOTAL_PAIRS
        
        if actual_count != expected_count:
            errors.append(f"❌ Wrong count: Expected {expected_count}, got {actual_count}")
        else:
            print(f"✅ Count correct: {actual_count} pairs")
        
        # Check structure
        required_keys = ["question", "answer", "answerable", "category"]
        for i, pair in enumerate(self.qa_database):
            for key in required_keys:
                if key not in pair:
                    errors.append(f"❌ Pair {i+1} missing key: {key}")
                elif pair[key] is None:
                    errors.append(f"❌ Pair {i+1} has None value for {key}")
                elif isinstance(pair[key], str) and len(pair[key].strip()) == 0:
                    errors.append(f"❌ Pair {i+1} has empty {key}")
        
        if not errors:
            print(f"✅ Structure correct: All pairs have required keys")
        
        # Check distribution
        answerable_count = sum(1 for p in self.qa_database if p.get("answerable") == True)
        unanswerable_count = sum(1 for p in self.qa_database if p.get("answerable") == False)
        
        if answerable_count != self.ANSWERABLE_TOTAL:
            warnings.append(f"⚠️  Answerable count: Expected {self.ANSWERABLE_TOTAL}, got {answerable_count}")
        else:
            print(f"✅ Answerable pairs: {answerable_count}")
        
        if unanswerable_count != self.UNANSWERABLE_TOTAL:
            warnings.append(f"⚠️  Unanswerable count: Expected {self.UNANSWERABLE_TOTAL}, got {unanswerable_count}")
        else:
            print(f"✅ Unanswerable pairs: {unanswerable_count}")
        
        # Check file exists
        csv_path = os.path.join(self.OUTPUT_DIR, "qa_database.csv")
        if not os.path.exists(csv_path):
            errors.append(f"❌ CSV file not found: {csv_path}")
        else:
            print(f"✅ CSV file exists: {csv_path}")
            # Verify CSV content
            try:
                df_check = pd.read_csv(csv_path)
                if len(df_check) != actual_count:
                    warnings.append(f"⚠️  CSV row count: {len(df_check)} != {actual_count}")
            except Exception as e:
                warnings.append(f"⚠️  Could not verify CSV: {e}")
        
        # Print results
        if errors:
            print("\n❌ VERIFICATION FAILED:")
            print("\n".join(errors))
            if warnings:
                print("\n⚠️  WARNINGS:")
                print("\n".join(warnings))
            print("="*70)
            return False
        else:
            print("\n✅ Objective 2 Complete - All checks passed!")
            if warnings:
                print("\n⚠️  WARNINGS:")
                print("\n".join(warnings))
            print(f"   • Total Q&A pairs: {actual_count}")
            print(f"   • Answerable: {answerable_count}")
            print(f"   • Unanswerable: {unanswerable_count}")
            print(f"   • CSV file: {csv_path}")
            print("="*70)
            return True


# ============================================================================
# EXECUTION - Uses env from Objective 0, inference_engine from Objective 1
# ============================================================================

# Verify prerequisites from Objective 0 and Objective 1
if 'env' not in globals():
    raise RuntimeError("❌ 'env' not found! Please run Objective 0 (Prerequisites & Setup) first.")

if 'inference_engine' not in globals():
    raise RuntimeError("❌ 'inference_engine' not found! Please run Objective 1 first.")

if 'system_prompt' not in globals():
    raise RuntimeError("❌ 'system_prompt' not found! Please run Objective 1 first.")

print("✅ Prerequisites validated (env, inference_engine, system_prompt)")

# ============================================================================
# EXECUTION - Orchestrates Objective 2 workflow with timing
# ============================================================================

with env.timer.objective(ObjectiveNames.OBJECTIVE_2):
    print("Objective 2: Generating Q&A Database\n")
    
    # Create QADatabaseGenerator instance (reuses InferenceEngine and env!)
    qa_generator = QADatabaseGenerator(env, inference_engine, system_prompt)
    
    # Generate full Q&A database
    qa_database = qa_generator.generate_full_database()
    
    # Convert to DataFrame
    qa_df = qa_generator.to_dataframe()
    
    # Save to CSV
    qa_generator.save_to_csv()
    
    # Display database
    qa_generator.display_database()
    
    # Verify results
    print("\n")
    qa_generator.verify()
    
    # Store in globals for other objectives
    globals()['qa_database'] = qa_database
    globals()['qa_df'] = qa_df
    globals()['QADatabaseGenerator'] = QADatabaseGenerator
    globals()['qa_generator'] = qa_generator
    
    print("\n✅ Objective 2 complete - Q&A database ready for Objective 3!")

