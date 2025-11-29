import json
from typing import List, Dict, Any
from .environment import EnvironmentConfig
from .config import OUTPUT_DIR

class KnowledgeBaseGenerator:
    """
    Generate knowledge base for job fitment analysis.
    Creates Q&A pairs, skill mappings, and company information.
    """
    
    def __init__(self, env: EnvironmentConfig):
        self.env = env
        self.knowledge_base = []
        
        # Skill categories
        self.skill_categories = {
            "programming_languages": [
                "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", 
                "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala"
            ],
            "frameworks": [
                "React", "Angular", "Vue.js", "Node.js", "Django", "Flask",
                "Spring Boot", "FastAPI", ".NET", "Express.js", "Next.js"
            ],
            "cloud_platforms": [
                "AWS", "Azure", "Google Cloud", "Kubernetes", "Docker",
                "Terraform", "Jenkins", "CI/CD", "Serverless"
            ],
            "data_skills": [
                "SQL", "NoSQL", "MongoDB", "PostgreSQL", "Redis", "Kafka",
                "Spark", "Hadoop", "ETL", "Data Warehousing"
            ],
            "ai_ml": [
                "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
                "NLP", "Computer Vision", "MLOps", "Data Science", "LLMs"
            ],
            "soft_skills": [
                "Communication", "Leadership", "Problem Solving", "Teamwork",
                "Time Management", "Critical Thinking", "Adaptability"
            ]
        }
        
        # Experience level mappings
        self.experience_levels = {
            "Entry": {"years": (0, 2), "keywords": ["junior", "entry", "graduate", "associate"]},
            "Mid": {"years": (2, 5), "keywords": ["mid", "intermediate", "developer", "engineer"]},
            "Senior": {"years": (5, 10), "keywords": ["senior", "lead", "staff", "principal"]},
            "Executive": {"years": (10, 20), "keywords": ["director", "vp", "head", "chief"]}
        }
    
    def generate_skill_qa_pairs(self) -> List[Dict[str, Any]]:
        """Generate Q&A pairs for skill-related queries."""
        qa_pairs = []
        
        for category, skills in self.skill_categories.items():
            for skill in skills:
                qa_pairs.append({
                    "question": f"What is {skill} and why is it important?",
                    "answer": f"{skill} is a key technology in {category.replace('_', ' ')}. "
                             f"It is highly valued in tech industry for building scalable solutions.",
                    "category": category,
                    "skill": skill,
                    "answerable": True
                })
                
                qa_pairs.append({
                    "question": f"How can I learn {skill}?",
                    "answer": f"To learn {skill}, start with official documentation, "
                             f"take online courses (Coursera, Udemy, Pluralsight), "
                             f"practice with hands-on projects, and contribute to open source.",
                    "category": "learning",
                    "skill": skill,
                    "answerable": True
                })
        
        return qa_pairs
    
    def generate_company_qa_pairs(self) -> List[Dict[str, Any]]:
        """Generate Q&A pairs for company-related queries."""
        qa_pairs = []
        
        company_info = {
            "Google": {"focus": "Search, AI, Cloud", "culture": "Innovation-driven, data-focused"},
            "Amazon": {"focus": "E-commerce, AWS, AI", "culture": "Customer obsession, bias for action"},
            "Apple": {"focus": "Consumer electronics, Software", "culture": "Design excellence, privacy-focused"},
            "Microsoft": {"focus": "Cloud, Enterprise, Gaming", "culture": "Growth mindset, inclusive"},
            "Meta": {"focus": "Social media, VR/AR, AI", "culture": "Move fast, be bold"},
            "Tesla": {"focus": "EVs, Clean energy, AI", "culture": "Mission-driven, intense"},
            "Cisco": {"focus": "Networking, Security, Collaboration", "culture": "Inclusive, tech-forward"},
            "SAP": {"focus": "Enterprise software, Cloud", "culture": "Customer success, innovation"},
            "NVIDIA": {"focus": "GPUs, AI hardware, Gaming", "culture": "Engineering excellence"},
            "Intel": {"focus": "Semiconductors, Computing", "culture": "Technology leadership"},
            "Netflix": {"focus": "Streaming, Content", "culture": "Freedom and responsibility"},
            "IBM": {"focus": "Enterprise AI, Cloud, Consulting", "culture": "Trust, transformation"}
        }
        
        for company, info in company_info.items():
            qa_pairs.append({
                "question": f"What does {company} focus on?",
                "answer": f"{company} focuses on {info['focus']}. Their culture is characterized by {info['culture']}.",
                "category": "company",
                "company": company,
                "answerable": True
            })
        
        return qa_pairs
    
    def generate_fitment_qa_pairs(self) -> List[Dict[str, Any]]:
        """Generate Q&A pairs for fitment-related queries."""
        qa_pairs = [
            {
                "question": "How is fitment score calculated?",
                "answer": "Fitment score is calculated using weighted criteria: Skills Match (40%), "
                         "Experience Match (25%), Education Match (20%), Location Match (10%), "
                         "and Culture Fit (5%). Each factor is scored 0-100 and combined.",
                "category": "fitment",
                "answerable": True
            },
            {
                "question": "What is a good fitment score?",
                "answer": "A fitment score above 70% indicates strong alignment. "
                         "80%+ is excellent and suggests high interview chances. "
                         "Below 50% indicates significant gaps that need addressing.",
                "category": "fitment",
                "answerable": True
            },
            {
                "question": "How can I improve my fitment score?",
                "answer": "Improve fitment by: 1) Acquiring missing technical skills, "
                         "2) Gaining relevant project experience, 3) Obtaining industry certifications, "
                         "4) Tailoring resume to job requirements, 5) Building portfolio projects.",
                "category": "fitment",
                "answerable": True
            }
        ]
        
        return qa_pairs
    
    def generate_unanswerable_qa_pairs(self) -> List[Dict[str, Any]]:
        """Generate unanswerable Q&A pairs for testing."""
        return [
            {
                "question": "What is the exact salary for this position?",
                "answer": "I cannot provide specific salary information as it varies by location, "
                         "experience, and negotiation. I recommend checking Glassdoor, Levels.fyi, "
                         "or the company's career page for salary ranges.",
                "category": "salary",
                "answerable": False
            },
            {
                "question": "Will I definitely get this job?",
                "answer": "I cannot predict hiring outcomes as they depend on many factors including "
                         "competition, interviewer preferences, and company needs. I can help you "
                         "improve your chances through better preparation.",
                "category": "prediction",
                "answerable": False
            },
            {
                "question": "What questions will they ask in the interview?",
                "answer": "I cannot know exact interview questions as they vary. However, I can help "
                         "you prepare for common technical and behavioral questions based on "
                         "the role and company patterns.",
                "category": "interview",
                "answerable": False
            }
        ]
    
    def generate_full_knowledge_base(self) -> List[Dict[str, Any]]:
        """Generate complete knowledge base."""
        print("📚 Generating Knowledge Base...")
        
        self.knowledge_base = []
        self.knowledge_base.extend(self.generate_skill_qa_pairs())
        self.knowledge_base.extend(self.generate_company_qa_pairs())
        self.knowledge_base.extend(self.generate_fitment_qa_pairs())
        self.knowledge_base.extend(self.generate_unanswerable_qa_pairs())
        
        print(f"   ✅ Generated {len(self.knowledge_base)} Q&A pairs")
        print(f"   • Skill Q&A: {len(self.generate_skill_qa_pairs())} pairs")
        print(f"   • Company Q&A: {len(self.generate_company_qa_pairs())} pairs")
        print(f"   • Fitment Q&A: {len(self.generate_fitment_qa_pairs())} pairs")
        
        return self.knowledge_base
    
    def save_knowledge_base(self, filename: str = "knowledge_base.json") -> str:
        """Save knowledge base to JSON file."""
        filepath = OUTPUT_DIR / filename
        with open(filepath, 'w') as f:
            json.dump(self.knowledge_base, f, indent=2)
        print(f"✅ Saved: {filepath}")
        return str(filepath)

