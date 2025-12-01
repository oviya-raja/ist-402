"""
LLM Fundamentals Support Module

Shared utility classes and functions following DRY, KISS, YAGNI, and SOLID principles.
All code reuse is centralized here.
"""

import sys
import os
import csv
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any
from abc import ABC, abstractmethod
from datetime import datetime


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
    """Single responsibility: Load models and tokenizers with caching."""
    
    # Modern fully open-source LLM (2025) - Qwen 2.5 by Alibaba
    # Fully open: weights, architecture, training methodology
    # Qwen 2.5 is the latest version with improved performance
    # Alternative options:
    # - "Qwen/Qwen2.5-7B" - Larger, more powerful
    # - "Qwen/Qwen2.5-3B" - Medium size
    # - "microsoft/Phi-3-mini-4k-instruct" - Microsoft's modern model
    # - "google/gemma-2-2b" - Google's Gemma model
    DEFAULT_MODEL = "Qwen/Qwen2.5-1.5B"  # Latest Qwen 2.5 (2025), fully open-source, great for learning
    
    def __init__(self, model_name: str = DEFAULT_MODEL, cache_dir: Optional[str] = None):
        """
        Initialize model loader.
        
        Args:
            model_name: Hugging Face model identifier
            cache_dir: Optional cache directory. If None, uses default HF cache.
        """
        self.model_name = model_name
        self._tokenizer = None
        self._model = None
        # Use explicit cache directory if provided, otherwise default to user's cache
        if cache_dir is not None:
            cache = cache_dir
        else:
            # Default to user's specified cache location
            user_cache = "/Users/rajasoun/.cache/huggingface"
            if os.path.exists(user_cache):
                cache = user_cache
            else:
                default_cache = self._get_default_cache_dir()
                cache = default_cache or "~/.cache/huggingface"
        # Expand user path if needed
        self._cache_dir = os.path.expanduser(cache) if isinstance(cache, str) else str(cache)
        self._cache_verified = False
    
    @staticmethod
    def _get_default_cache_dir() -> Optional[str]:
        """Get default Hugging Face cache directory."""
        try:
            from huggingface_hub import default_cache_path
            return str(default_cache_path())
        except (ImportError, AttributeError):
            # Fallback to standard location
            import os
            return os.path.expanduser("~/.cache/huggingface")
    
    def get_cache_dir(self) -> str:
        """Get the cache directory being used."""
        return str(self._cache_dir)
    
    def verify_cache(self) -> bool:
        """Verify cache directory exists and is writable."""
        if self._cache_verified:
            return True
        
        try:
            cache_path = Path(self._cache_dir)
            cache_path.mkdir(parents=True, exist_ok=True)
            
            # Test write permissions
            test_file = cache_path / ".cache_test"
            test_file.write_text("test")
            test_file.unlink()
            
            self._cache_verified = True
            return True
        except Exception as e:
            print(f"⚠️  Cache verification failed: {e}")
            return False
    
    def is_cached(self) -> Tuple[bool, bool]:
        """
        Check if model and tokenizer are cached.
        
        Returns:
            Tuple of (model_cached, tokenizer_cached)
        """
        try:
            cache_path = Path(self._cache_dir)
            model_cached = False
            tokenizer_cached = False
            
            # Model name in cache format: "Qwen/Qwen2.5-1.5B" -> "models--Qwen--Qwen2.5-1.5B"
            model_name_safe = self.model_name.replace('/', '--')
            model_dir_pattern = f"models--{model_name_safe}*"
            
            # Check in hub subdirectory (newer HF cache structure)
            hub_cache = cache_path / "hub"
            if hub_cache.exists():
                model_dirs = list(hub_cache.glob(model_dir_pattern))
                if model_dirs:
                    model_dir = model_dirs[0]
                    # Check for model files - need both config AND weights
                    config_files = list(model_dir.rglob("config.json"))
                    # Check for actual model weight files (safetensors or pytorch_model.bin)
                    weight_files = list(model_dir.rglob("model.safetensors")) + list(model_dir.rglob("pytorch_model.bin"))
                    if config_files and weight_files:
                        model_cached = True
                    # Check for tokenizer files
                    tokenizer_files = list(model_dir.rglob("tokenizer*.json"))
                    if tokenizer_files:
                        tokenizer_cached = True
                    # Also check for tokenizer_config.json
                    if not tokenizer_cached:
                        tokenizer_config = list(model_dir.rglob("tokenizer_config.json"))
                        if tokenizer_config:
                            tokenizer_cached = True
            
            # Also check in root cache directory (older/alternative structure)
            if not model_cached:
                model_dirs = list(cache_path.glob(model_dir_pattern))
                if model_dirs:
                    model_dir = model_dirs[0]
                    # Check for model files - need both config AND weights
                    config_files = list(model_dir.rglob("config.json"))
                    # Check for actual model weight files (safetensors or pytorch_model.bin)
                    weight_files = list(model_dir.rglob("model.safetensors")) + list(model_dir.rglob("pytorch_model.bin"))
                    if config_files and weight_files:
                        model_cached = True
                    # Check for tokenizer files
                    tokenizer_files = list(model_dir.rglob("tokenizer*.json"))
                    if tokenizer_files:
                        tokenizer_cached = True
                    if not tokenizer_cached:
                        tokenizer_config = list(model_dir.rglob("tokenizer_config.json"))
                        if tokenizer_config:
                            tokenizer_cached = True
            
            # Final check: Try to actually load config/tokenizer locally (most reliable)
            # Only do this if file-based check didn't find them
            if not model_cached or not tokenizer_cached:
                try:
                    from transformers import AutoConfig, AutoTokenizer
                    # Try to load config locally (but config alone doesn't mean model is cached)
                    # We need the actual model weights, so we check for config but don't rely on it alone
                    if not model_cached:
                        try:
                            config = AutoConfig.from_pretrained(
                                self.model_name,
                                cache_dir=self._cache_dir,
                                local_files_only=True
                            )
                            # Config exists, but we still need to verify weights exist
                            # Don't set model_cached=True here - let the file check above handle it
                        except:
                            pass
                    
                    # Try to load tokenizer locally
                    if not tokenizer_cached:
                        try:
                            tokenizer = AutoTokenizer.from_pretrained(
                                self.model_name,
                                cache_dir=self._cache_dir,
                                local_files_only=True
                            )
                            tokenizer_cached = True
                        except:
                            pass
                except:
                    pass
            
            return model_cached, tokenizer_cached
        except Exception:
            return False, False
    
    def load_tokenizer(self, from_globals: Optional[dict] = None, use_cache: bool = True):
        """
        Load tokenizer, reusing from globals if available.
        
        Args:
            from_globals: Global namespace to check for cached tokenizer
            use_cache: Whether to use Hugging Face cache (default: True)
        """
        if from_globals and 'tokenizer' in from_globals:
            self._tokenizer = from_globals['tokenizer']
            print(f"⚡ Using tokenizer from global cache: {self.model_name}")
            return self._tokenizer
        
        try:
            from transformers import AutoTokenizer
            
            # Verify cache before loading
            local_files_only = False
            if use_cache:
                self.verify_cache()
                model_cached, tokenizer_cached = self.is_cached()
                if tokenizer_cached:
                    print(f"💾 Loading tokenizer from cache: {self.model_name}")
                    print(f"   Cache location: {self._cache_dir}")
                    local_files_only = True  # Use local files only to avoid download
                else:
                    print(f"⚠️  Tokenizer not found in cache: {self.model_name}")
                    print(f"   Cache location: {self._cache_dir}")
                    print(f"   Attempting download (if online)...")
                    local_files_only = False
            
            # Load with explicit cache directory and local_files_only flag
            try:
                self._tokenizer = AutoTokenizer.from_pretrained(
                    self.model_name,
                    cache_dir=self._cache_dir if use_cache else None,
                    local_files_only=local_files_only
                )
                if local_files_only:
                    print(f"✅ Successfully loaded tokenizer from cache (offline mode)")
                return self._tokenizer
            except Exception as e:
                if local_files_only:
                    # If local_files_only failed, try without it (fallback)
                    print(f"⚠️  Failed to load from cache, trying with download enabled...")
                    self._tokenizer = AutoTokenizer.from_pretrained(
                        self.model_name,
                        cache_dir=self._cache_dir if use_cache else None,
                        local_files_only=False
                    )
                    return self._tokenizer
                else:
                    raise
        except ImportError:
            raise ImportError("transformers library not installed. Install with: pip install transformers")
    
    def load_model(self, from_globals: Optional[dict] = None, use_cache: bool = True, allow_download: bool = False):
        """
        Load model, reusing from globals if available.
        
        Args:
            from_globals: Global namespace to check for cached model
            use_cache: Whether to use Hugging Face cache (default: True)
            allow_download: Whether to allow downloading if model not in cache (default: False)
        """
        if from_globals and 'model' in from_globals:
            self._model = from_globals['model']
            print(f"⚡ Using model from global cache: {self.model_name}")
            return self._model
        
        try:
            from transformers import AutoModel
            
            # Verify cache before loading
            local_files_only = False
            if use_cache:
                self.verify_cache()
                model_cached, _ = self.is_cached()
                if model_cached:
                    print(f"💾 Loading model from cache: {self.model_name}")
                    print(f"   Cache location: {self._cache_dir}")
                    local_files_only = True  # Use local files only to avoid download
                else:
                    if allow_download:
                        print(f"⚠️  Model not found in cache: {self.model_name}")
                        print(f"   Cache location: {self._cache_dir}")
                        print(f"   Attempting download (if online)...")
                        local_files_only = False
                    else:
                        raise FileNotFoundError(
                            f"Model {self.model_name} not found in cache and downloads are disabled. "
                            f"Cache location: {self._cache_dir}\n"
                            f"To download the model, set allow_download=True or ensure the model is cached."
                        )
            
            # Load with explicit cache directory and local_files_only flag
            try:
                self._model = AutoModel.from_pretrained(
                    self.model_name,
                    cache_dir=self._cache_dir if use_cache else None,
                    local_files_only=local_files_only
                )
                if local_files_only:
                    print(f"✅ Successfully loaded model from cache (offline mode)")
                return self._model
            except Exception as e:
                if local_files_only:
                    # If local_files_only failed, only try download if allowed
                    if allow_download:
                        print(f"⚠️  Failed to load from cache (model weights may be missing or incomplete)")
                        print(f"   Error: {str(e)[:100]}...")
                        print(f"   Attempting to download/complete model files...")
                        self._model = AutoModel.from_pretrained(
                            self.model_name,
                            cache_dir=self._cache_dir if use_cache else None,
                            local_files_only=False
                        )
                        return self._model
                    else:
                        raise FileNotFoundError(
                            f"Failed to load model {self.model_name} from cache. "
                            f"Model weights may be missing or incomplete.\n"
                            f"Error: {str(e)}\n"
                            f"Cache location: {self._cache_dir}\n"
                            f"To download the model, set allow_download=True."
                        ) from e
                else:
                    raise
        except ImportError:
            raise ImportError("transformers library not installed. Install with: pip install transformers")
    
    def load_both(self, from_globals: Optional[dict] = None, use_cache: bool = True, allow_download: bool = False):
        """Load both tokenizer and model."""
        tokenizer = self.load_tokenizer(from_globals, use_cache=use_cache)
        model = self.load_model(from_globals, use_cache=use_cache, allow_download=allow_download)
        return tokenizer, model
    
    @staticmethod
    def list_local_models(cache_dir: Optional[str] = None, output_csv: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all models available in the local cache directory.
        
        Args:
            cache_dir: Cache directory to scan. If None, uses default cache.
            output_csv: Optional path to CSV file to save results. If None, prints to console.
        
        Returns:
            List of dictionaries containing model information.
        """
        # Determine cache directory
        if cache_dir is None:
            user_cache = "/Users/rajasoun/.cache/huggingface"
            if os.path.exists(user_cache):
                cache_dir = user_cache
            else:
                cache_dir = ModelLoader._get_default_cache_dir() or "~/.cache/huggingface"
        
        cache_path = Path(cache_dir).expanduser()
        models = []
        
        if not cache_path.exists():
            print(f"⚠️  Cache directory does not exist: {cache_path}")
            return models
        
        # Scan both hub subdirectory and root cache directory
        search_paths = [
            cache_path / "hub",
            cache_path
        ]
        
        for search_path in search_paths:
            if not search_path.exists():
                continue
            
            # Find all model directories (pattern: models--*)
            model_dirs = list(search_path.glob("models--*"))
            
            for model_dir in model_dirs:
                try:
                    # Convert cache name back to model name: "models--Qwen--Qwen2.5-1.5B" -> "Qwen/Qwen2.5-1.5B"
                    model_name_cache = model_dir.name
                    model_name = model_name_cache.replace("models--", "").replace("--", "/")
                    
                    # Check if this is a valid model directory
                    config_files = list(model_dir.rglob("config.json"))
                    if not config_files:
                        continue
                    
                    # Get model details
                    model_info = {
                        'model_name': model_name,
                        'cache_name': model_name_cache,
                        'cache_location': str(model_dir),
                        'has_config': len(config_files) > 0,
                        'has_tokenizer': len(list(model_dir.rglob("tokenizer*.json"))) > 0 or 
                                       len(list(model_dir.rglob("tokenizer_config.json"))) > 0,
                        'last_modified': datetime.fromtimestamp(model_dir.stat().st_mtime).isoformat(),
                    }
                    
                    # Calculate total size
                    total_size = 0
                    file_count = 0
                    model_files = []
                    
                    for file_path in model_dir.rglob("*"):
                        if file_path.is_file():
                            try:
                                size = file_path.stat().st_size
                                total_size += size
                                file_count += 1
                                # Track important files
                                if file_path.name in ['config.json', 'tokenizer_config.json', 'vocab.json', 
                                                      'pytorch_model.bin', 'model.safetensors', 'model.bin']:
                                    model_files.append(file_path.name)
                            except:
                                pass
                    
                    model_info['total_size_bytes'] = total_size
                    model_info['total_size_mb'] = round(total_size / (1024 * 1024), 2)
                    model_info['total_size_gb'] = round(total_size / (1024 * 1024 * 1024), 2)
                    model_info['file_count'] = file_count
                    model_info['key_files'] = ', '.join(sorted(set(model_files)))
                    
                    # Try to load config for additional details (all from core-concepts.md)
                    try:
                        from transformers import AutoConfig
                        config = AutoConfig.from_pretrained(
                            model_name,
                            cache_dir=str(cache_path),
                            local_files_only=True
                        )
                        
                        # Core configuration details (from core-concepts.md section "Retrieving Model Configuration")
                        # 1. Vocabulary size
                        model_info['vocab_size'] = getattr(config, 'vocab_size', None)
                        
                        # 2. Hidden size
                        model_info['hidden_size'] = getattr(config, 'hidden_size', None)
                        
                        # 3. Number of layers
                        model_info['num_layers'] = getattr(config, 'num_hidden_layers', 
                                                          getattr(config, 'num_layers', None))
                        
                        # 4. Number of attention heads
                        model_info['num_attention_heads'] = getattr(config, 'num_attention_heads', None)
                        
                        # 5. Max position embeddings (context length)
                        model_info['max_position_embeddings'] = getattr(config, 'max_position_embeddings', None)
                        
                        # 6. Embedding size (usually same as hidden_size, but some models have separate)
                        model_info['embedding_size'] = getattr(config, 'embedding_size', 
                                                               getattr(config, 'embedding_dim', 
                                                                      model_info['hidden_size']))
                        
                        # 7. Activation function
                        model_info['activation_function'] = getattr(config, 'activation_function', 
                                                                   getattr(config, 'hidden_act', None))
                        
                        # 8. Positional embedding type
                        model_info['position_embedding_type'] = getattr(config, 'position_embedding_type', None)
                        
                        # 9. Attention variant/type
                        model_info['attention_type'] = getattr(config, 'attention_type', 
                                                              getattr(config, 'attn_implementation', None))
                        
                        # Additional useful details
                        model_info['model_type'] = getattr(config, 'model_type', None)
                        model_info['architectures'] = ', '.join(getattr(config, 'architectures', []))
                        
                        # Intermediate size (feedforward dimension)
                        model_info['intermediate_size'] = getattr(config, 'intermediate_size', 
                                                                 getattr(config, 'ffn_dim', None))
                        
                        # Number of key-value heads (for grouped query attention)
                        model_info['num_key_value_heads'] = getattr(config, 'num_key_value_heads', None)
                        
                        # Head dimension
                        if model_info['hidden_size'] and model_info['num_attention_heads']:
                            model_info['head_dim'] = model_info['hidden_size'] // model_info['num_attention_heads']
                        else:
                            model_info['head_dim'] = getattr(config, 'head_dim', None)
                        
                        # Try to estimate parameter count from config (approximate)
                        try:
                            if model_info['num_layers'] and model_info['hidden_size']:
                                # Rough estimate: 12 * num_layers * hidden_size^2
                                # This is a simplified estimate, actual count varies by architecture
                                estimated_params = 12 * model_info['num_layers'] * (model_info['hidden_size'] ** 2)
                                model_info['estimated_parameters'] = int(estimated_params)
                                model_info['estimated_parameters_billions'] = round(estimated_params / 1e9, 2)
                            else:
                                model_info['estimated_parameters'] = None
                                model_info['estimated_parameters_billions'] = None
                        except:
                            model_info['estimated_parameters'] = None
                            model_info['estimated_parameters_billions'] = None
                        
                    except Exception as e:
                        model_info['config_error'] = str(e)[:100]  # Truncate long errors
                        # Set all config fields to None
                        for field in ['vocab_size', 'hidden_size', 'num_layers', 'num_attention_heads', 
                                     'max_position_embeddings', 'embedding_size', 'activation_function',
                                     'position_embedding_type', 'attention_type', 'model_type', 'architectures',
                                     'intermediate_size', 'num_key_value_heads', 'head_dim', 
                                     'estimated_parameters', 'estimated_parameters_billions']:
                            model_info[field] = None
                    
                    models.append(model_info)
                    
                except Exception as e:
                    print(f"⚠️  Error processing {model_dir}: {e}")
                    continue
        
        # Remove duplicates (same model in hub and root)
        seen = set()
        unique_models = []
        for model in models:
            key = model['model_name']
            if key not in seen:
                seen.add(key)
                unique_models.append(model)
        
        models = unique_models
        
        # Sort by model name
        models.sort(key=lambda x: x['model_name'])
        
        # Output to CSV if requested
        if output_csv:
            try:
                output_path = Path(output_csv)
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                if models:
                    # Define CSV columns - includes all details from core-concepts.md
                    fieldnames = [
                        # Basic info
                        'model_name', 'model_type', 'architectures',
                        # Core components (from core-concepts.md)
                        'vocab_size',           # 1. Tokens - vocabulary size
                        'embedding_size',       # 2. Embeddings - embedding dimension
                        'hidden_size',          # Hidden dimension
                        'num_attention_heads',  # 3. Attention - number of heads
                        'attention_type',       # 3. Attention - variant/type
                        'num_layers',           # 4. Layers - number of transformer layers
                        'intermediate_size',    # 4. Layers - feedforward dimension
                        'head_dim',            # Attention head dimension
                        'num_key_value_heads', # Grouped query attention
                        'estimated_parameters', # 6. Parameters - estimated count
                        'estimated_parameters_billions', # Parameters in billions
                        'max_position_embeddings', # Context length
                        'activation_function',  # Activation function
                        'position_embedding_type', # Positional embedding type
                        # File info
                        'total_size_gb', 'total_size_mb', 'total_size_bytes', 
                        'file_count', 'has_config', 'has_tokenizer',
                        'key_files', 'last_modified', 'cache_location'
                    ]
                    
                    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
                        writer.writeheader()
                        writer.writerows(models)
                    
                    print(f"✅ Exported {len(models)} models to CSV: {output_path}")
                else:
                    print(f"⚠️  No models found to export")
            except Exception as e:
                print(f"❌ Error writing CSV file: {e}")
        else:
            # Print to console with all details from core-concepts.md
            if models:
                print(f"\n📋 Found {len(models)} cached model(s):\n")
                for model in models:
                    print(f"  Model: {model['model_name']}")
                    
                    # Core Components (from core-concepts.md)
                    print(f"    📊 Core Components:")
                    if model.get('vocab_size'):
                        print(f"      1️⃣  Tokens: vocab_size = {model['vocab_size']:,}")
                    if model.get('embedding_size') or model.get('hidden_size'):
                        emb_size = model.get('embedding_size') or model.get('hidden_size')
                        print(f"      2️⃣  Embeddings: size = {emb_size}")
                    if model.get('num_attention_heads'):
                        attn_info = f"heads = {model['num_attention_heads']}"
                        if model.get('attention_type'):
                            attn_info += f", type = {model['attention_type']}"
                        if model.get('head_dim'):
                            attn_info += f", head_dim = {model['head_dim']}"
                        print(f"      3️⃣  Attention: {attn_info}")
                    if model.get('num_layers'):
                        layer_info = f"layers = {model['num_layers']}"
                        if model.get('intermediate_size'):
                            layer_info += f", intermediate_size = {model['intermediate_size']}"
                        print(f"      4️⃣  Layers: {layer_info}")
                    if model.get('estimated_parameters_billions'):
                        print(f"      6️⃣  Parameters: ~{model['estimated_parameters_billions']}B")
                    
                    # Additional Configuration Details
                    if model.get('hidden_size') or model.get('max_position_embeddings') or model.get('activation_function'):
                        print(f"    🔍 Configuration Details:")
                        if model.get('hidden_size'):
                            print(f"      Hidden Size: {model['hidden_size']}")
                        if model.get('max_position_embeddings'):
                            print(f"      Max Position Embeddings: {model['max_position_embeddings']:,}")
                        if model.get('activation_function'):
                            print(f"      Activation Function: {model['activation_function']}")
                        if model.get('position_embedding_type'):
                            print(f"      Position Embedding Type: {model['position_embedding_type']}")
                        if model.get('num_key_value_heads'):
                            print(f"      Key-Value Heads: {model['num_key_value_heads']}")
                    
                    # File Info
                    print(f"    💾 File Info:")
                    print(f"      Size: {model['total_size_gb']} GB ({model['total_size_mb']} MB)")
                    print(f"      Files: {model['file_count']}")
                    print(f"      Has Config: {model['has_config']}")
                    print(f"      Has Tokenizer: {model['has_tokenizer']}")
                    if model.get('model_type'):
                        print(f"      Type: {model['model_type']}")
                    if model.get('architectures'):
                        print(f"      Architectures: {model['architectures']}")
                    print(f"      Location: {model['cache_location']}")
                    print()
            else:
                print("⚠️  No cached models found")
        
        return models
    
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
    
    def get_tokenizer_type_info(self) -> Dict[str, Any]:
        """Get information about the tokenizer type and algorithm."""
        info = {
            'class_name': type(self.tokenizer).__name__,
            'module': type(self.tokenizer).__module__,
            'tokenizer_type': None,
            'algorithm': None,
            'is_fast': 'Fast' in type(self.tokenizer).__name__,
        }
        
        # Get tokenizer algorithm from backend
        if hasattr(self.tokenizer, 'backend_tokenizer'):
            backend = self.tokenizer.backend_tokenizer
            if hasattr(backend, 'model'):
                model_type = type(backend.model).__name__
                info['algorithm'] = model_type
                # Map to common names
                algorithm_map = {
                    'BPE': 'Byte Pair Encoding',
                    'WordPiece': 'WordPiece',
                    'Unigram': 'Unigram',
                    'SentencePiece': 'SentencePiece',
                }
                if model_type in algorithm_map:
                    info['algorithm'] = algorithm_map[model_type]
        
        # Get tokenizer class from config
        if hasattr(self.tokenizer, 'tokenizer_config'):
            config = self.tokenizer.tokenizer_config
            if 'tokenizer_class' in config:
                info['tokenizer_type'] = config['tokenizer_class']
        
        # Fallback: infer from class name
        if not info['tokenizer_type']:
            class_name = info['class_name']
            # Remove 'Fast' suffix if present
            base_name = class_name.replace('TokenizerFast', '').replace('Tokenizer', '')
            info['tokenizer_type'] = base_name if base_name else 'Unknown'
        
        return info


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
        
        # Show cache information
        try:
            cache_dir = ModelLoader._get_default_cache_dir()
            if cache_dir and Path(cache_dir).exists():
                print(f"💾 HF Cache: {cache_dir}")
            else:
                print(f"💾 HF Cache: {cache_dir} (will be created on first download)")
        except Exception:
            pass
    
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
