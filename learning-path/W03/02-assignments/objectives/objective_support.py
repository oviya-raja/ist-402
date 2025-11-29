# ============================================================================
# OBJECTIVE SUPPORT - DRY Principle
# ============================================================================
# Common utilities for objective scripts to eliminate duplication.
# Follows KISS, YAGNI, SOLID, and DRY principles.
#
# Usage:
#     support = ObjectiveSupport()
#     support.ensure_prerequisites({'env': 'Objective 0'}, globals())
#     output_dir = support.setup_output_dir("data/rag_pipeline")
# ============================================================================

import os
from typing import Dict, Optional


class ObjectiveSupport:
    """
    Support utilities for objective scripts.
    
    Provides common functionality to eliminate code duplication across objectives:
    - Prerequisite validation
    - Output directory setup
    
    Example:
        support = ObjectiveSupport()
        support.ensure_prerequisites({
            'env': 'Objective 0 (Prerequisites & Setup)',
            'system_prompt': 'Objective 1'
        }, globals())
    """
    
    def validate_prerequisites(self, required: Dict[str, str], globals_dict: dict) -> bool:
        """
        Validate prerequisites from previous objectives (DRY).
        
        Args:
            required: Dict mapping variable name to objective description
                     e.g., {'env': 'Objective 0', 'system_prompt': 'Objective 1'}
            globals_dict: Global namespace (usually globals())
        
        Returns:
            True if all prerequisites exist, False otherwise
        
        Example:
            support = ObjectiveSupport()
            if not support.validate_prerequisites({'env': 'Objective 0'}, globals()):
                raise RuntimeError("Missing prerequisites")
        """
        missing = []
        for var_name, objective_desc in required.items():
            if var_name not in globals_dict:
                missing.append(f"{var_name} ({objective_desc})")
        
        if missing:
            print("❌ MISSING DEPENDENCIES:")
            for m in missing:
                print(f"   • {m}")
            return False
        
        return True
    
    def ensure_prerequisites(self, required: Dict[str, str], globals_dict: dict) -> None:
        """
        Ensure prerequisites exist, raising RuntimeError if missing (DRY).
        
        Args:
            required: Dict mapping variable name to objective description
            globals_dict: Global namespace (usually globals())
        
        Raises:
            RuntimeError: If any prerequisite is missing
        
        Example:
            support = ObjectiveSupport()
            support.ensure_prerequisites({
                'env': 'Objective 0 (Prerequisites & Setup)',
                'system_prompt': 'Objective 1'
            }, globals())
        """
        missing = []
        for var_name, objective_desc in required.items():
            if var_name not in globals_dict:
                missing.append(f"❌ '{var_name}' not found! Please run {objective_desc} first.")
        
        if missing:
            raise RuntimeError("\n".join(missing))
    
    def setup_output_dir(self, directory: str) -> str:
        """
        Create output directory if it doesn't exist (DRY).
        
        Args:
            directory: Directory path (e.g., "data/rag_pipeline")
        
        Returns:
            Absolute path to the created directory
        
        Example:
            support = ObjectiveSupport()
            output_dir = support.setup_output_dir("data/rag_pipeline")
        """
        os.makedirs(directory, exist_ok=True)
        return os.path.abspath(directory)


# Convenience instance for direct usage
# Usage: objective_support.ensure_prerequisites(...)
objective_support = ObjectiveSupport()

