# ============================================================================
# Prerequisites & Setup - Centralized Environment Configuration
# ============================================================================
# This cell contains a centralized EnvironmentConfig class that handles ALL
# Colab vs local environment differences. No if statements needed elsewhere!
# Run this cell FIRST before any other cells

import sys
import os
from typing import Optional, Tuple

# Import ObjectiveSupport for DRY (optional - graceful fallback)
try:
    from objective_support import ObjectiveSupport
    _support = ObjectiveSupport()
except ImportError:
    # Fallback if not available (for notebook extraction)
    _support = None

# ============================================================================
# EnvironmentConfig Class - Single Source of Truth
# ============================================================================
class EnvironmentConfig:
    """
    Centralized environment configuration that handles ALL Colab vs local differences.
    All environment-specific logic is encapsulated here - no if statements needed elsewhere!
    
    Usage:
        env = EnvironmentConfig()  # Auto-detects environment
        device = env.device  # Returns "cuda" or "cpu" automatically
        token = env.get_token()  # Works in both Colab and local
    """
    
    def __init__(self):
        """Initialize and detect environment automatically."""
        self._is_colab = self._detect_colab()
        self._has_gpu = self._detect_gpu()
        self._python_version = sys.version.split()[0]
        self._hf_token = None
        self._libraries_imported = False
        
        # Print environment info
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
        
        if self._has_gpu:
            try:
                import torch
                print(f"   ✅ GPU Available: {torch.cuda.get_device_name(0)}")
                print(f"   ✅ CUDA Version: {torch.version.cuda}")
            except:
                pass
        else:
            print("   ⚠️  GPU NOT detected (using CPU)")
            if self._is_colab:
                print("   💡 TIP: Runtime → Change runtime type → Select GPU → Save")
    
    # ========================================================================
    # Properties - No if statements needed when using these!
    # ========================================================================
    
    @property
    def is_colab(self) -> bool:
        """Check if running in Google Colab."""
        return self._is_colab
    
    @property
    def is_local(self) -> bool:
        """Check if running locally."""
        return not self._is_colab
    
    @property
    def has_gpu(self) -> bool:
        """Check if GPU is available."""
        return self._has_gpu
    
    @property
    def device(self) -> str:
        """Get device string ('cuda' or 'cpu') - no if statement needed!"""
        return "cuda" if self._has_gpu else "cpu"
    
    @property
    def device_id(self) -> int:
        """Get device ID (0 for GPU, -1 for CPU) - no if statement needed!"""
        return 0 if self._has_gpu else -1
    
    @property
    def hf_token(self) -> Optional[str]:
        """Get Hugging Face token."""
        return self._hf_token
    
    @property
    def python_version(self) -> str:
        """Get Python version."""
        return self._python_version
    
    # ========================================================================
    # Token Management - Works in both Colab and local
    # ========================================================================
    
    def _format_token_preview(self, token: str) -> str:
        """
        Format token for safe display (DRY - eliminates duplication).
        
        Args:
            token: Hugging Face token string
            
        Returns:
            Formatted preview string (e.g., "hf_abc123...xyz9")
        """
        if len(token) <= 14:
            return "****"
        return f"{token[:10]}...{token[-4:]}"
    
    def get_token(self) -> Optional[str]:
        """
        Get Hugging Face token from appropriate source (Colab or local).
        Works automatically in both environments - no if statements needed!
        """
        # Try Colab userdata first (only works in Colab, fails gracefully in local)
        if self._is_colab:
            try:
                from google.colab import userdata
                token = userdata.get('HUGGINGFACE_HUB_TOKEN')
                if token:
                    print("✅ Hugging Face token loaded from Colab userdata!")
                    print(f"   Token preview: {self._format_token_preview(token)}")
                    self._hf_token = token
                    return token
            except (ImportError, ValueError):
                pass
        
        # Try environment variable (works in both Colab and local)
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ImportError:
            pass
        
        token = os.getenv("HUGGINGFACE_HUB_TOKEN")
        if token:
            print("✅ Hugging Face token loaded from environment!")
            print(f"   Token preview: {self._format_token_preview(token)}")
            self._hf_token = token
            return token
        
        # No token found
        print("❌ Hugging Face token not found!")
        print("   Get your token from: https://huggingface.co/settings/tokens")
        
        if self._is_colab:
            print("\n   In Colab: userdata.set('HUGGINGFACE_HUB_TOKEN', 'your_token')")
        else:
            print("\n   Locally: export HUGGINGFACE_HUB_TOKEN=your_token")
            print("   Or create .env file: HUGGINGFACE_HUB_TOKEN=your_token")
        
        print("\n⚠️  Some models may require authentication!")
        return None
    
    def authenticate_hf(self, token: Optional[str] = None) -> bool:
        """
        Authenticate with Hugging Face.
        Uses stored token if none provided.
        """
        token = token or self._hf_token
        
        if not token:
            print("⚠️  No token provided, skipping authentication")
            return False
        
        try:
            from huggingface_hub import login
            login(token=token)
            print("✅ Authenticated with Hugging Face")
            return True
        except Exception as e:
            print(f"⚠️  Authentication failed: {e}")
            return False
    
    # ========================================================================
    # Package Management - Works in both environments
    # ========================================================================
    
    def install_packages(self):
        """Install required packages if not already installed."""
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
            "accelerate"
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
    
    # ========================================================================
    # Library Imports - Centralized and reusable
    # ========================================================================
    
    def import_libraries(self) -> bool:
        """
        Import all required libraries with error handling.
        Returns True if successful, False otherwise.
        """
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
            import faiss
            
            transformers_logging.set_verbosity_error()
            
            # Store imported modules for reuse
            self.pipeline = pipeline
            self.AutoModelForCausalLM = AutoModelForCausalLM
            self.AutoTokenizer = AutoTokenizer
            self.SentenceTransformer = SentenceTransformer
            self.torch = torch
            self.np = np
            self.faiss = faiss
            
            self._libraries_imported = True
            print("✅ All required libraries imported successfully!")
            return True
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("   Run: pip install transformers torch sentence-transformers faiss-cpu")
            return False
        except RuntimeError as e:
            if "register_fake" in str(e) or "torch.library" in str(e):
                print("❌ Dependency version mismatch!")
                print("   Fix: pip install --upgrade torch torchvision")
                print("   Then restart kernel and run this cell again.")
            return False
    
    @property
    def libraries_ready(self) -> bool:
        """Check if libraries are imported and ready."""
        return self._libraries_imported
    
    # ========================================================================
    # Utility Methods - Environment-agnostic helpers
    # ========================================================================
    
    def get_device_info(self) -> dict:
        """Get device information dictionary."""
        info = {
            "device": self.device,
            "device_id": self.device_id,
            "has_gpu": self._has_gpu,
            "is_colab": self._is_colab
        }
        
        if self._has_gpu and self._libraries_imported:
            try:
                info["gpu_name"] = self.torch.cuda.get_device_name(0)
                info["cuda_version"] = self.torch.version.cuda
            except:
                pass
        
        return info
    
    def print_summary(self):
        """Print configuration summary."""
        print("=" * 80)
        print("✅ PREREQUISITES & SETUP COMPLETED!")
        print("=" * 80)
        print()
        print("📌 Environment Configuration:")
        print(f"   - Environment: {'Google Colab' if self._is_colab else 'Local'}")
        print(f"   - Python: {self._python_version}")
        print(f"   - Device: {self.device.upper()} ({'GPU' if self._has_gpu else 'CPU'})")
        print(f"   - HF Token: {'✅ Set' if self._hf_token else '❌ Not set'}")
        print(f"   - Libraries: {'✅ Ready' if self._libraries_imported else '❌ Not imported'}")
        print()
        print("💡 Usage in other cells:")
        print("   - env.device  # Returns 'cuda' or 'cpu'")
        print("   - env.is_colab  # Returns True/False")
        print("   - env.has_gpu  # Returns True/False")
        print("   - env.hf_token  # Returns token or None")
        print("=" * 80)


# ============================================================================
# Objective Names - Standardized naming guide
# ============================================================================
class ObjectiveNames:
    """
    Standardized objective naming guide.
    Use these constants to ensure consistent naming across the notebook.
    
    Usage:
        with env.timer.objective(ObjectiveNames.OBJECTIVE_1):
            # Your code
            pass
    """
    OBJECTIVE_0 = "Objective 0"
    OBJECTIVE_1 = "Objective 1"
    OBJECTIVE_2 = "Objective 2"
    OBJECTIVE_3 = "Objective 3"
    OBJECTIVE_4 = "Objective 4"
    OBJECTIVE_5 = "Objective 5"
    OBJECTIVE_6 = "Objective 6"
    
    @classmethod
    def get_number(cls, objective_name: str) -> Optional[int]:
        """
        Extract objective number from name.
        
        Args:
            objective_name: Objective name (e.g., "Objective 1")
            
        Returns:
            Objective number (e.g., 1) or None if invalid
        """
        try:
            # Extract number from "Objective X" format
            parts = objective_name.split()
            if len(parts) >= 2 and parts[0].lower() == "objective":
                return int(parts[1])
        except (ValueError, IndexError):
            pass
        return None
    
    @classmethod
    def format_name(cls, number: int) -> str:
        """
        Format objective number into standardized name.
        
        Args:
            number: Objective number (e.g., 1)
            
        Returns:
            Formatted name (e.g., "Objective 1")
        """
        return f"Objective {number}"


# ============================================================================
# ObjectiveTimingManager - Track execution time for each objective
# ============================================================================
class ObjectiveTimingManager:
    """
    Track and store execution time for each objective.
    Compares first-time vs subsequent runs.
    
    Usage:
        with env.timer.objective("Objective 1"):
            # Your code here
            pass
        
        # View timing history
        env.timer.print_summary()
        env.timer.get_stats("Objective 1")
    """
    
    def __init__(self, storage_file: str = "objective_timings.csv", support=None):
        """Initialize timing manager with persistent CSV storage."""
        import csv
        import time
        import pandas as pd
        from datetime import datetime
        from pathlib import Path
        
        self.csv = csv
        self.pd = pd
        self.time = time
        self.datetime = datetime
        self.Path = Path
        self.support = support
        
        # Use ObjectiveSupport for output directory setup if available (DRY)
        storage_path = Path(storage_file)
        if self.support:
            # Setup parent directory if needed
            if storage_path.parent != Path('.'):
                self.support.setup_output_dir(str(storage_path.parent))
        else:
            # Fallback: create parent directory manually
            storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.storage_file = storage_path
        self.timings = self._load_timings()
        self.current_objective = None
        self.start_time = None
    
    def _load_timings(self) -> dict:
        """Load timing history from CSV file."""
        if not self.storage_file.exists():
            return {}
        
        try:
            df = self.pd.read_csv(self.storage_file)
            
            # Convert CSV back to internal dict structure
            timings = {}
            for _, row in df.iterrows():
                obj_name = row['objective_name']
                if obj_name not in timings:
                    timings[obj_name] = {
                        "first_run": None,
                        "runs": [],
                        "total_runs": 0,
                        "average_time": None,
                        "min_time": None,
                        "max_time": None
                    }
                
                # Add this run
                timings[obj_name]["runs"].append({
                    "time": row['time'],
                    "timestamp": row['timestamp'],
                    "run_number": row['run_number']
                })
                
                # CRITICAL: Set first_run from CSV's first_run column for THIS objective only
                # This ensures each objective compares against its own first_run, not another objective's
                if timings[obj_name]["first_run"] is None:
                    # Use the first_run value from CSV (same for all rows of same objective)
                    first_run_value = row.get('first_run')
                    if self.pd.notna(first_run_value):
                        timings[obj_name]["first_run"] = float(first_run_value)
                        timings[obj_name]["first_run_timestamp"] = row.get('first_run_timestamp', row['timestamp'])
            
            # Recalculate statistics
            for obj_name in timings:
                data = timings[obj_name]
                data["total_runs"] = len(data["runs"])
                if data["runs"]:
                    times = [r["time"] for r in data["runs"]]
                    data["average_time"] = sum(times) / len(times)
                    data["min_time"] = min(times)
                    data["max_time"] = max(times)
            
            return timings
        except Exception as e:
            print(f"⚠️  Could not load timings: {e}")
            return {}
    
    def _save_timings(self):
        """Save timing history to CSV file."""
        try:
            self.storage_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Convert internal dict structure to CSV rows
            rows = []
            for obj_name, data in self.timings.items():
                for run in data["runs"]:
                    rows.append({
                        'objective_name': obj_name,
                        'run_number': run['run_number'],
                        'time': run['time'],
                        'timestamp': run['timestamp'],
                        'first_run': data.get('first_run'),
                        'first_run_timestamp': data.get('first_run_timestamp', '')
                    })
            
            if rows:
                df = self.pd.DataFrame(rows)
                # Sort by objective name and run number
                df = df.sort_values(['objective_name', 'run_number'])
                df.to_csv(self.storage_file, index=False)
        except Exception as e:
            print(f"⚠️  Could not save timings: {e}")
    
    def objective(self, objective_name: str):
        """
        Context manager for timing an objective.
        
        Usage:
            with env.timer.objective("Objective 1"):
                # Your code
                pass
        """
        return ObjectiveTimer(self, objective_name)
    
    def record_time(self, objective_name: str, elapsed_time: float):
        """Record execution time for an objective."""
        if objective_name not in self.timings:
            self.timings[objective_name] = {
                "first_run": None,
                "runs": [],
                "total_runs": 0,
                "average_time": None,
                "min_time": None,
                "max_time": None
            }
        
        timing_data = self.timings[objective_name]
        timing_data["runs"].append({
            "time": elapsed_time,
            "timestamp": self.datetime.now().isoformat(),
            "run_number": timing_data["total_runs"] + 1
        })
        
        # Store first run separately
        if timing_data["first_run"] is None:
            timing_data["first_run"] = elapsed_time
            timing_data["first_run_timestamp"] = self.datetime.now().isoformat()
        
        # Update statistics
        timing_data["total_runs"] = len(timing_data["runs"])
        times = [r["time"] for r in timing_data["runs"]]
        timing_data["average_time"] = sum(times) / len(times)
        timing_data["min_time"] = min(times)
        timing_data["max_time"] = max(times)
        
        # Save to file
        self._save_timings()
    
    def get_stats(self, objective_name: str) -> Optional[dict]:
        """
        Get statistics for a specific objective.
        CRITICAL: Only returns stats for the specified objective_name - ensures comparison is within objective.
        """
        if objective_name not in self.timings:
            return None
        
        # Get data for THIS specific objective only (filters by objective_name)
        data = self.timings[objective_name]
        
        # Verify we're getting the right objective's data
        if not data.get("runs"):
            return None
        
        return {
            "first_run": data.get("first_run"),  # This is THIS objective's first_run only
            "first_run_timestamp": data.get("first_run_timestamp"),
            "first_run_number": 1,  # Always 1 for first run
            "last_run": data["runs"][-1]["time"] if data["runs"] else None,
            "average_time": data.get("average_time"),
            "min_time": data.get("min_time"),
            "max_time": data.get("max_time"),
            "total_runs": data.get("total_runs", 0),
            "improvement": self._calculate_improvement(data)
        }
    
    def get_first_run_info(self, objective_name: str) -> Optional[dict]:
        """
        Get first run information for an objective (easier access).
        
        Args:
            objective_name: Name of objective (e.g., "Objective 1")
            
        Returns:
            Dict with first_run info or None if not found:
            {
                "time": float,  # First run time in seconds
                "formatted_time": str,  # Human-readable time
                "timestamp": str,  # ISO timestamp
                "run_number": int,  # Always 1
                "objective_number": Optional[int]  # Extracted number (e.g., 1)
            }
        """
        stats = self.get_stats(objective_name)
        if not stats or stats.get("first_run") is None:
            return None
        
        # Extract objective number (use ObjectiveNames directly - it's in same cell)
        obj_number = ObjectiveNames.get_number(objective_name)
        
        return {
            "time": stats["first_run"],
            "formatted_time": self._format_time(stats["first_run"]),
            "timestamp": stats.get("first_run_timestamp", "Unknown"),
            "run_number": 1,
            "objective_number": obj_number
        }
    
    def _calculate_improvement(self, data: dict) -> Optional[float]:
        """Calculate improvement percentage from first to average."""
        if data.get("first_run") and data.get("average_time"):
            first = data["first_run"]
            avg = data["average_time"]
            if first > 0:
                improvement = ((first - avg) / first) * 100
                return improvement
        return None
    
    def print_summary(self):
        """Print summary of all objective timings."""
        if not self.timings:
            print("📊 No timing data recorded yet.")
            print("   Use: with env.timer.objective('Objective 1'): ...")
            return
        
        print("=" * 80)
        print("📊 OBJECTIVE TIMING SUMMARY")
        print("=" * 80)
        print()
        
        for obj_name in sorted(self.timings.keys()):
            stats = self.get_stats(obj_name)
            if not stats:
                continue
            
            print(f"🎯 {obj_name}:")
            print(f"   First Run:  {self._format_time(stats['first_run'])}")
            if stats['total_runs'] > 1:
                print(f"   Last Run:   {self._format_time(stats['last_run'])}")
                print(f"   Average:    {self._format_time(stats['average_time'])}")
                print(f"   Min:        {self._format_time(stats['min_time'])}")
                print(f"   Max:        {self._format_time(stats['max_time'])}")
                print(f"   Total Runs: {stats['total_runs']}")
                if stats['improvement']:
                    sign = "↓" if stats['improvement'] > 0 else "↑"
                    print(f"   Improvement: {sign}{abs(stats['improvement']):.1f}% vs first run")
            print()
        
        print("=" * 80)
    
    def _format_time(self, seconds: Optional[float]) -> str:
        """Format time in human-readable format."""
        if seconds is None:
            return "N/A"
        
        if seconds < 60:
            return f"{seconds:.2f}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes}m {secs:.2f}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = seconds % 60
            return f"{hours}h {minutes}m {secs:.2f}s"
    
    def compare_first_vs_subsequent(self, objective_name: str):
        """Compare first run vs subsequent runs for an objective."""
        if objective_name not in self.timings:
            print(f"❌ No data for {objective_name}")
            return
        
        data = self.timings[objective_name]
        if data["total_runs"] < 2:
            print(f"⚠️  Need at least 2 runs to compare. Current: {data['total_runs']}")
            return
        
        first = data.get("first_run")
        if first is None or not isinstance(first, (int, float)):
            print(f"❌ No first run data for {objective_name}")
            return
        
        # Type assertion: first is guaranteed to be float here
        first_float: float = float(first)
        
        # Extract subsequent run times, ensuring they are floats
        subsequent_times: list[float] = [float(r["time"]) for r in data["runs"][1:] if r.get("time") is not None]
        if not subsequent_times:
            print(f"⚠️  No subsequent runs to compare")
            return
        
        # Calculate average - both values are guaranteed to be float
        total_time: float = sum(subsequent_times)
        count: int = len(subsequent_times)
        avg_subsequent: float = total_time / count
        
        print(f"📊 {objective_name} - First vs Subsequent Runs:")
        print(f"   First Run:     {self._format_time(first_float)}")
        print(f"   Avg Subsequent: {self._format_time(avg_subsequent)}")
        
        if first_float > 0:
            # Both first_float and avg_subsequent are guaranteed to be float here
            improvement: float = ((first_float - avg_subsequent) / first_float) * 100
            print(f"   Improvement:  {improvement:+.1f}%")
        
        print()
    
    def clear_objective(self, objective_name: str) -> bool:
        """
        Clear timing data for a specific objective.
        
        Args:
            objective_name: Name of objective to clear
            
        Returns:
            True if cleared, False if objective not found
        """
        if objective_name not in self.timings:
            print(f"⚠️  No data found for '{objective_name}'")
            return False
        
        del self.timings[objective_name]
        self._save_timings()
        print(f"✅ Cleared timing data for '{objective_name}'")
        return True
    
    def clear_all(self, confirm: bool = False) -> bool:
        """
        Clear all timing data and delete CSV file.
        
        Args:
            confirm: If True, clears without asking. If False, prints warning but doesn't clear.
                    Use clear_all(confirm=True) to actually clear.
            
        Returns:
            True if cleared, False if not confirmed
        """
        if not confirm:
            print("⚠️  WARNING: This will delete ALL timing data!")
            print(f"   File: {self.storage_file}")
            print(f"   Current objectives: {list(self.timings.keys())}")
            print()
            print("   To confirm, use: env.timer.clear_all(confirm=True)")
            return False
        
        # Clear in-memory data
        self.timings = {}
        
        # Delete CSV file
        if self.storage_file.exists():
            try:
                self.storage_file.unlink()
                print(f"✅ Deleted timing file: {self.storage_file}")
            except Exception as e:
                print(f"⚠️  Could not delete file: {e}")
        
        print("✅ All timing data cleared!")
        return True
    
    def reset_objective(self, objective_name: str) -> bool:
        """
        Reset timing data for a specific objective (keeps file, removes objective).
        Same as clear_objective() - provided for clarity.
        
        Args:
            objective_name: Name of objective to reset
            
        Returns:
            True if reset, False if objective not found
        """
        return self.clear_objective(objective_name)


class ObjectiveTimer:
    """
    Context manager for timing a single objective execution.
    
    Usage:
        # Using standardized name (recommended):
        with env.timer.objective(ObjectiveNames.OBJECTIVE_1):
            # Your code
            pass
        
        # Or using string directly:
        with env.timer.objective("Objective 1"):
            # Your code
            pass
    """
    
    def __init__(self, manager: ObjectiveTimingManager, objective_name: str):
        self.manager = manager
        self.objective_name = objective_name
        self.start_time = None
        # Extract objective number for better display
        self.objective_number = self._extract_number(objective_name)
    
    def _extract_number(self, name: str) -> Optional[int]:
        """Extract objective number from name."""
        try:
            parts = name.split()
            if len(parts) >= 2 and parts[0].lower() == "objective":
                return int(parts[1])
        except (ValueError, IndexError):
            pass
        return None
    
    def __enter__(self):
        self.start_time = self.manager.time.time()
        # Show objective number and run count
        stats = self.manager.get_stats(self.objective_name)
        run_number = (stats['total_runs'] + 1) if stats else 1
        print(f"⏱️  Starting: {self.objective_name} (Run #{run_number})")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Ensure start_time is set (should always be set by __enter__)
        if self.start_time is None:
            print(f"⚠️  Warning: start_time was not set for {self.objective_name}")
            return False
        
        # Calculate elapsed time - both values are guaranteed to be float now
        current_time: float = self.manager.time.time()
        start_time: float = self.start_time
        elapsed: float = current_time - start_time
        
        self.manager.record_time(self.objective_name, elapsed)
        
        # Get stats for THIS specific objective only (filters by objective_name)
        stats = self.manager.get_stats(self.objective_name)
        is_first = stats and stats["total_runs"] == 1
        
        # Get first run info for easier display
        first_run_info = self.manager.get_first_run_info(self.objective_name)
        
        print(f"✅ Completed: {self.objective_name}")
        print(f"   Time: {self.manager._format_time(elapsed)}")
        
        if is_first:
            print(f"   📝 First run recorded (Run #1)")
        else:
            # CRITICAL: Compare only with THIS objective's first run (not other objectives)
            if stats is None or first_run_info is None:
                print(f"   ⚠️  No stats available for {self.objective_name}")
            else:
                # Use first_run_info for cleaner display
                first_float: float = float(first_run_info["time"])
                diff: float = elapsed - first_float
                pct: float = ((elapsed - first_float) / first_float) * 100 if first_float > 0 else 0.0
                sign = "+" if diff > 0 else ""
                
                # Enhanced display with run number and first run info
                run_number = stats["total_runs"]
                first_run_display = first_run_info["formatted_time"]
                
                # Show comparison - explicitly shows it's comparing within the same objective
                print(f"   📊 Run #{run_number} vs First Run (Run #1, {first_run_display}): {sign}{self.manager._format_time(abs(diff))} ({sign}{pct:.1f}%)")
                
                # Show when first run happened (if available)
                if first_run_info.get("timestamp") and first_run_info["timestamp"] != "Unknown":
                    try:
                        from datetime import datetime
                        first_dt = datetime.fromisoformat(first_run_info["timestamp"].replace('Z', '+00:00'))
                        print(f"   📅 First run: {first_dt.strftime('%Y-%m-%d %H:%M:%S')}")
                    except:
                        pass
        
        print()
        return False  # Don't suppress exceptions

# ============================================================================
# Global Environment Instance - Use this everywhere!
# ============================================================================

print("=" * 80)
print("OBJECTIVE 0: PREREQUISITES & SETUP")
print("=" * 80)
print()

# ============================================================================
# OPTIONAL: Clear timing data to start fresh
# ============================================================================
# Uncomment the line below if you want to reset all timing data:
# RESET_TIMINGS = True
# Otherwise, timing data will accumulate (recommended to track history)
RESET_TIMINGS = False

# Start timing Objective 0
import time
objective0_start = time.time()

# Create global environment configuration instance
env = EnvironmentConfig()
print()

# Install packages
env.install_packages()
print()

# Import libraries
if env.import_libraries():
    # Get and authenticate token
    env.get_token()
    if env.hf_token:
        env.authenticate_hf()
    print()
    env.print_summary()
    
    # Initialize timing manager and attach to env
    # Pass _support for DRY output directory setup
    timer = ObjectiveTimingManager(storage_file="data/objective_timings.csv", support=_support)
    env.timer = timer
    
    # Optional: Clear all timing data if RESET_TIMINGS is True
    if RESET_TIMINGS:
        env.timer.clear_all(confirm=True)
        print()
    
    # Make env and classes globally available
    globals()['env'] = env
    globals()['EnvironmentConfig'] = EnvironmentConfig
    globals()['ObjectiveTimingManager'] = ObjectiveTimingManager
    globals()['ObjectiveNames'] = ObjectiveNames  # For standardized objective naming
    
    # Backward compatibility - set old global variables
    globals()['IN_COLAB'] = env.is_colab
    globals()['HAS_GPU'] = env.has_gpu
    globals()['hf_token'] = env.hf_token
    
    # Record Objective 0 execution time
    objective0_elapsed = time.time() - objective0_start
    env.timer.record_time("Objective 0", objective0_elapsed)
    
    print("💡 Timing system ready! Use: with env.timer.objective('Objective 1'): ...")
    print()
    print(f"✅ Objective 0 completed in {env.timer._format_time(objective0_elapsed)}")
    print()
else:
    print("❌ Setup incomplete. Please fix errors above.")