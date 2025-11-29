"""
Environment configuration for Job Fitment Agent.
Handles Colab vs local environment differences automatically.
"""

import os
import sys
from typing import Optional


class EnvironmentConfig:
    """
    Centralized environment configuration for Job Fitment Agent.
    Handles Colab vs local environment differences automatically.
    """
    
    def __init__(self):
        """Initialize and detect environment."""
        self._is_colab = self._detect_colab()
        self._has_gpu = False
        self._python_version = sys.version.split()[0]
        self._hf_token = None
        self._libraries_imported = False
        self._openai_api_key = None
        
        # Storage for imported modules
        self.torch = None
        self.np = None
        self.pd = None
        self.faiss = None
        self.SentenceTransformer = None
        self.pipeline = None
        self.AutoModelForCausalLM = None
        self.AutoTokenizer = None
        
        self._print_environment_info()
    
    def _detect_colab(self) -> bool:
        """Detect if running in Google Colab."""
        try:
            import google.colab
            return True
        except ImportError:
            return False
    
    def _detect_gpu(self) -> bool:
        """Detect GPU availability."""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    def _print_environment_info(self):
        """Print environment detection results."""
        print("🔍 Checking environment...")
        print(f"   Python version: {self._python_version}")
        
        if self._is_colab:
            print("   ✅ Running in Google Colab")
        else:
            print("   ✅ Running in local environment")
    
    @property
    def is_colab(self) -> bool:
        return self._is_colab
    
    @property
    def is_local(self) -> bool:
        return not self._is_colab
    
    @property
    def has_gpu(self) -> bool:
        return self._has_gpu
    
    @property
    def device(self) -> str:
        return "cuda" if self._has_gpu else "cpu"
    
    @property
    def device_id(self) -> int:
        return 0 if self._has_gpu else -1
    
    @property
    def hf_token(self) -> Optional[str]:
        return self._hf_token
    
    @property
    def openai_api_key(self) -> Optional[str]:
        return self._openai_api_key
    
    def install_packages(self):
        """Install required packages."""
        packages = [
            "transformers",
            "torch",
            "sentence-transformers",
            "python-dotenv",
            "faiss-cpu",
            "huggingface_hub",
            "numpy",
            "pandas",
            "bert-score",
            "openai",
            "requests",
            "beautifulsoup4",
            "aiohttp"
        ]
        
        print("📦 Installing required packages...")
        for package in packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"   ✅ {package} already installed")
            except ImportError:
                print(f"   ⏳ Installing {package}...")
                os.system(f"pip install -q {package}")
                print(f"   ✅ {package} installed")
    
    def import_libraries(self) -> bool:
        """Import all required libraries."""
        try:
            from transformers import (
                pipeline, 
                AutoModelForCausalLM, 
                AutoTokenizer, 
                logging as transformers_logging
            )
            from sentence_transformers import SentenceTransformer
            import torch
            import numpy as np
            import pandas as pd
            import faiss
            
            transformers_logging.set_verbosity_error()
            
            self.pipeline = pipeline
            self.AutoModelForCausalLM = AutoModelForCausalLM
            self.AutoTokenizer = AutoTokenizer
            self.SentenceTransformer = SentenceTransformer
            self.torch = torch
            self.np = np
            self.pd = pd
            self.faiss = faiss
            
            self._has_gpu = torch.cuda.is_available()
            self._libraries_imported = True
            
            if self._has_gpu:
                print(f"   ✅ GPU Available: {torch.cuda.get_device_name(0)}")
            else:
                print("   ⚠️  GPU NOT detected (using CPU)")
            
            print("✅ All required libraries imported successfully!")
            return True
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            return False
    
    def get_token(self, token_name: str = "HUGGINGFACE_HUB_TOKEN") -> Optional[str]:
        """Get API token from environment."""
        if self._is_colab:
            try:
                from google.colab import userdata
                token = userdata.get(token_name)
                if token:
                    print(f"✅ {token_name} loaded from Colab userdata!")
                    return token
            except (ImportError, ValueError):
                pass
        
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        
        token = os.getenv(token_name)
        if token:
            print(f"✅ {token_name} loaded from environment!")
            if token_name == "HUGGINGFACE_HUB_TOKEN":
                self._hf_token = token
            elif token_name == "OPENAI_API_KEY":
                self._openai_api_key = token
            return token
        
        print(f"⚠️  {token_name} not found in environment")
        return None
    
    def authenticate_hf(self, token: Optional[str] = None) -> bool:
        """Authenticate with Hugging Face."""
        token = token or self._hf_token
        if not token:
            return False
        
        try:
            from huggingface_hub import login
            login(token=token)
            print("✅ Authenticated with Hugging Face")
            return True
        except Exception as e:
            print(f"⚠️  Authentication failed: {e}")
            return False
    
    def print_summary(self):
        """Print configuration summary."""
        print("=" * 80)
        print("✅ JOB FITMENT AGENT SETUP COMPLETE!")
        print("=" * 80)
        print(f"   - Environment: {'Google Colab' if self._is_colab else 'Local'}")
        print(f"   - Python: {self._python_version}")
        print(f"   - Device: {self.device.upper()}")
        print(f"   - HF Token: {'✅ Set' if self._hf_token else '❌ Not set'}")
        print(f"   - OpenAI Key: {'✅ Set' if self._openai_api_key else '❌ Not set'}")
        print("=" * 80)

