"""
LLM Fundamentals Support Module

Shared utility classes and functions following DRY, KISS, YAGNI, and SOLID principles.
All code reuse is centralized here.
"""

import sys
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
from abc import ABC, abstractmethod


class DeviceDetector:
    """Single responsibility: Detect available compute device."""
    
    @staticmethod
    def detect() -> str:
        """Detect available device (cuda, mps, or cpu)."""
        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return "mps"
            return "cpu"
        except ImportError:
            return "cpu"


class DependencyChecker:
    """Single responsibility: Check for required dependencies."""
    
    @staticmethod
    def check(required: List[str]) -> Tuple[bool, List[str]]:
        """Check if required packages are installed."""
        missing = []
        for package in required:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        return len(missing) == 0, missing


class ModelLoader:
    """Single responsibility: Load models and tokenizers."""
    
    DEFAULT_MODEL = "gpt2"
    
    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self._tokenizer = None
        self._model = None
    
    def load_tokenizer(self, from_globals: Optional[dict] = None):
        """Load tokenizer, reusing from globals if available."""
        if from_globals and 'tokenizer' in from_globals:
            self._tokenizer = from_globals['tokenizer']
            return self._tokenizer
        
        try:
            from transformers import AutoTokenizer
            self._tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            return self._tokenizer
        except ImportError:
            raise ImportError("transformers library not installed. Install with: pip install transformers")
    
    def load_model(self, from_globals: Optional[dict] = None):
        """Load model, reusing from globals if available."""
        if from_globals and 'model' in from_globals:
            self._model = from_globals['model']
            return self._model
        
        try:
            from transformers import AutoModel
            self._model = AutoModel.from_pretrained(self.model_name)
            return self._model
        except ImportError:
            raise ImportError("transformers library not installed. Install with: pip install transformers")
    
    def load_both(self, from_globals: Optional[dict] = None):
        """Load both tokenizer and model."""
        tokenizer = self.load_tokenizer(from_globals)
        model = self.load_model(from_globals)
        return tokenizer, model
    
    @property
    def tokenizer(self):
        """Get tokenizer."""
        return self._tokenizer
    
    @property
    def model(self):
        """Get model."""
        return self._model


class TextProcessor:
    """Single responsibility: Process text (tokenize, encode, decode)."""
    
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
    
    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into tokens."""
        return self.tokenizer.tokenize(text)
    
    def encode(self, text: str, return_tensors: Optional[str] = None):
        """Encode text to token IDs."""
        return self.tokenizer.encode(text, return_tensors=return_tensors)
    
    def decode(self, token_ids) -> str:
        """Decode token IDs to text."""
        if hasattr(self.tokenizer, 'decode'):
            return self.tokenizer.decode(token_ids, skip_special_tokens=True)
        return self.tokenizer.decode(token_ids)
    
    def get_token_info(self, text: str) -> Dict[str, Any]:
        """Get comprehensive token information."""
        tokens = self.tokenize(text)
        token_ids = self.encode(text, return_tensors=None)
        return {
            'text': text,
            'tokens': tokens,
            'token_ids': token_ids,
            'num_tokens': len(tokens),
            'num_chars': len(text),
            'ratio': len(tokens) / len(text) if len(text) > 0 else 0
        }


class EmbeddingExtractor:
    """Single responsibility: Extract embeddings from models."""
    
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.processor = TextProcessor(tokenizer)
    
    def get_embeddings(self, text: str):
        """Get embeddings for text."""
        import torch
        token_ids = self.processor.encode(text, return_tensors="pt")
        
        with torch.no_grad():
            outputs = self.model(token_ids)
            return outputs.last_hidden_state
    
    def get_embedding_stats(self, embeddings) -> Dict[str, float]:
        """Get statistics about embeddings."""
        return {
            'mean': float(embeddings.mean().item()),
            'std': float(embeddings.std().item()),
            'min': float(embeddings.min().item()),
            'max': float(embeddings.max().item())
        }


class Formatter:
    """Single responsibility: Format output consistently."""
    
    @staticmethod
    def header(title: str, width: int = 80) -> str:
        """Create header."""
        return "=" * width + f"\n{title}\n" + "=" * width
    
    @staticmethod
    def section(title: str, width: int = 80) -> str:
        """Create section divider."""
        return "\n" + "-" * width + f"\n{title}\n" + "-" * width
    
    @staticmethod
    def learning_intro(concept: str, description: str, what_we_learn: List[str], 
                      what_we_do: List[str], hands_on: List[str]) -> str:
        """Create learning introduction section."""
        lines = [
            f"\n📖 CONCEPT: {concept}",
            f"\n📝 Description: {description}",
            "\n🎯 What You'll Learn:",
        ]
        for i, item in enumerate(what_we_learn, 1):
            lines.append(f"   {i}. {item}")
        lines.append("\n🔧 What We're Doing:")
        for i, item in enumerate(what_we_do, 1):
            lines.append(f"   {i}. {item}")
        lines.append("\n💻 Hands-On Code:")
        for i, item in enumerate(hands_on, 1):
            lines.append(f"   {i}. {item}")
        lines.append("")
        return "\n".join(lines)
    
    @staticmethod
    def output_summary(what_we_saw: List[str]) -> str:
        """Create output summary section."""
        lines = ["\n📊 What We Observed:"]
        for i, item in enumerate(what_we_saw, 1):
            lines.append(f"   {i}. {item}")
        return "\n".join(lines)
    
    @staticmethod
    def summary(title: str, takeaways: List[str], next_obj: Optional[str] = None) -> str:
        """Create summary section."""
        lines = ["\n" + "=" * 80, f"✅ {title}", "=" * 80, "\n📚 Key Takeaways:"]
        for i, takeaway in enumerate(takeaways, 1):
            lines.append(f"  {i}. {takeaway}")
        if next_obj:
            lines.append(f"\n➡️  Next: {next_obj}")
        return "\n".join(lines)


class StateManager:
    """Single responsibility: Manage global state between objectives."""
    
    @staticmethod
    def save_to_globals(globals_dict: dict, **items):
        """Save items to global namespace."""
        for key, value in items.items():
            globals_dict[key] = value
    
    @staticmethod
    def load_from_globals(globals_dict: dict, *keys) -> dict:
        """Load items from global namespace."""
        return {key: globals_dict.get(key) for key in keys}


class LLMFundamentalsSupport:
    """
    Main support class that composes all utilities.
    Follows composition over inheritance (SOLID).
    """
    
    def __init__(self):
        """Initialize support utilities."""
        self.device_detector = DeviceDetector()
        self.dependency_checker = DependencyChecker()
        self.formatter = Formatter()
        self.state_manager = StateManager()
        self._print_info()
    
    def _print_info(self):
        """Print environment information."""
        print(f"🔧 Python: {sys.version.split()[0]}")
        print(f"🔧 Device: {self.device_detector.detect()}")
    
    @property
    def device(self) -> str:
        """Get the detected device."""
        return self.device_detector.detect()
    
    @property
    def python_version(self) -> str:
        """Get Python version."""
        return sys.version.split()[0]
    
    def check_dependencies(self, required: List[str]) -> bool:
        """Check if required packages are installed."""
        success, missing = self.dependency_checker.check(required)
        if not success:
            print(f"⚠️  Missing packages: {', '.join(missing)}")
        return success


def create_output_dir(base_dir: Optional[Path] = None) -> Path:
    """Create output directory for objective results."""
    if base_dir is None:
        base_dir = Path(__file__).parent
    output_dir = base_dir / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


def save_results(data: dict, filename: str, output_dir: Optional[Path] = None):
    """Save objective results to file."""
    output_dir = create_output_dir(output_dir)
    filepath = output_dir / filename
    
    import json
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"💾 Results saved to: {filepath}")
