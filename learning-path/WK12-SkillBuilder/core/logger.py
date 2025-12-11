"""
Logging Module for Skill Builder for IST Students
Handles all logging operations with proper error handling and formatting.
"""

import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional


class AppLogger:
    """
    Centralized logging system with file and console handlers.
    Implements proper error handling and log rotation.
    """
    
    def __init__(self, log_dir: str = "logs", log_level: str = "INFO"):
        """
        Initialize logger with file and console handlers.
        
        Args:
            log_dir: Directory to store log files
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger("SkillBuilder")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        
        # File handler with daily rotation
        log_file = self.log_dir / f"app_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance."""
        return self.logger
    
    def log_error(self, error: Exception, context: Optional[str] = None):
        """
        Log errors with context information.
        
        Args:
            error: Exception object
            context: Additional context about where error occurred
        """
        error_msg = f"Error: {str(error)}"
        if context:
            error_msg = f"{context} - {error_msg}"
        self.logger.error(error_msg, exc_info=True)
    
    def log_api_call(self, api_name: str, status: str, details: Optional[str] = None):
        """
        Log API calls for monitoring and debugging.
        
        Args:
            api_name: Name of the API being called
            status: Success or failure status
            details: Additional details about the call
        """
        log_msg = f"API Call - {api_name}: {status}"
        if details:
            log_msg += f" - {details}"
        self.logger.info(log_msg)
    
    # Delegate standard logger methods to underlying logger
    def debug(self, msg, *args, **kwargs):
        """Log debug message."""
        self.logger.debug(msg, *args, **kwargs)
    
    def info(self, msg, *args, **kwargs):
        """Log info message."""
        self.logger.info(msg, *args, **kwargs)
    
    def warning(self, msg, *args, **kwargs):
        """Log warning message."""
        self.logger.warning(msg, *args, **kwargs)
    
    def error(self, msg, *args, **kwargs):
        """Log error message."""
        self.logger.error(msg, *args, **kwargs)
    
    def critical(self, msg, *args, **kwargs):
        """Log critical message."""
        self.logger.critical(msg, *args, **kwargs)


# Global logger instance
_logger_instance: Optional[AppLogger] = None


def get_logger(log_dir: str = "logs", log_level: str = "INFO"):
    """
    Get or create global logger instance.
    
    Args:
        log_dir: Directory for log files
        log_level: Logging level
        
    Returns:
        AppLogger instance (acts like a logger but has additional methods)
    """
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = AppLogger(log_dir, log_level)
    return _logger_instance