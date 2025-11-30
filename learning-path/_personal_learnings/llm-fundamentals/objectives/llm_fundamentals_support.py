"""
LLM Fundamentals Support Module

Shared utility functions for LLM fundamentals objectives.
"""

import sys
import os
from pathlib import Path
from typing import Optional, Tuple


class LLMFundamentalsSupport:
    """
    Support class for LLM fundamentals objectives.
    Provides common utilities and environment detection.
    """
    
    def __init__(self):
        """Initialize support utilities."""
        self._python_version = sys.version.split()[0]
        self._device = self._detect_device()
        self._print_info()
    
    def _detect_device(self) -> str:
        """Detect available device (cuda, mps, or cpu)."""
        try:
            import torch
            if torch.cuda.is_available():
                return "cuda"
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        except ImportError:
            return "cpu"
    
    def _print_info(self):
        """Print environment information."""
        print(f"🔧 Python: {self._python_version}")
        print(f"🔧 Device: {self._device}")
    
    @property
    def device(self) -> str:
        """Get the detected device."""
        return self._device
    
    @property
    def python_version(self) -> str:
        """Get Python version."""
        return self._python_version
    
    def check_dependencies(self, required: list) -> bool:
        """Check if required packages are installed."""
        missing = []
        for package in required:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        if missing:
            print(f"⚠️  Missing packages: {', '.join(missing)}")
            return False
        return True


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

