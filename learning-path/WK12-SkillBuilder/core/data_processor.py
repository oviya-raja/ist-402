"""
Data Preprocessing Module
Handles ingestion and preprocessing of real-world data (CSV, text files).
"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import pandas as pd

from core.logger import get_logger

logger = get_logger()


class DataProcessor:
    """
    Processes various data formats and prepares them for GenAI consumption.
    Handles CSV, JSON, and text file formats with proper error handling.
    """
    
    def __init__(self):
        """Initialize data processor."""
        self.logger = logger
        self.processed_data: List[Dict[str, Any]] = []
    
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Load and validate CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            DataFrame with loaded data
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is invalid or empty
        """
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise FileNotFoundError(f"CSV file not found: {file_path}")
            
            self.logger.info(f"Loading CSV file: {file_path}")
            # Use proper CSV parsing with quote handling for fields with commas
            # Try with error handling for malformed CSV
            try:
                df = pd.read_csv(file_path, quotechar='"', escapechar='\\')
            except pd.errors.ParserError:
                # If that fails, try with Python engine (more lenient)
                try:
                    df = pd.read_csv(file_path, quotechar='"', on_bad_lines='skip', engine='python')
                except Exception:
                    # Last resort: try with basic settings and Python engine
                    df = pd.read_csv(file_path, engine='python', sep=',', quotechar='"', doublequote=True)
            
            if df.empty:
                raise ValueError(f"CSV file is empty: {file_path}")
            
            self.logger.info(f"Successfully loaded {len(df)} rows from CSV")
            return df
            
        except pd.errors.EmptyDataError:
            self.logger.error(f"CSV file is empty: {file_path}")
            raise ValueError(f"CSV file is empty: {file_path}")
        except pd.errors.ParserError as e:
            self.logger.error(f"Error parsing CSV: {str(e)}")
            raise ValueError(f"Invalid CSV format: {str(e)}")
        except Exception as e:
            self.logger.log_error(e, f"Error loading CSV file: {file_path}")
            raise
    
    def load_text_file(self, file_path: str) -> str:
        """
        Load text file content.
        
        Args:
            file_path: Path to text file
            
        Returns:
            File content as string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            UnicodeDecodeError: If file encoding is invalid
        """
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                raise FileNotFoundError(f"Text file not found: {file_path}")
            
            self.logger.info(f"Loading text file: {file_path}")
            
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    self.logger.info(f"Successfully loaded text file with {len(content)} characters")
                    return content
                except UnicodeDecodeError:
                    continue
            
            raise UnicodeDecodeError(f"Could not decode file with any supported encoding: {file_path}")
            
        except Exception as e:
            self.logger.log_error(e, f"Error loading text file: {file_path}")
            raise
    
    def preprocess_dataframe(self, df: pd.DataFrame, 
                            text_columns: Optional[List[str]] = None,
                            remove_na: bool = True) -> List[Dict[str, Any]]:
        """
        Preprocess DataFrame for GenAI consumption.
        
        Args:
            df: Input DataFrame
            text_columns: Columns to extract as text (default: all string columns)
            remove_na: Whether to remove rows with NA values
            
        Returns:
            List of dictionaries with processed data
        """
        try:
            self.logger.info(f"Preprocessing DataFrame with {len(df)} rows")
            
            # Remove NA if requested
            if remove_na:
                initial_len = len(df)
                df = df.dropna()
                removed = initial_len - len(df)
                if removed > 0:
                    self.logger.info(f"Removed {removed} rows with NA values")
            
            # Identify text columns
            if text_columns is None:
                text_columns = df.select_dtypes(include=['object']).columns.tolist()
            
            # Convert to list of dictionaries
            processed = []
            for idx, row in df.iterrows():
                record = {
                    'id': idx,
                    'text_content': self._extract_text_content(row, text_columns),
                    'metadata': {col: str(row[col]) for col in df.columns if col not in text_columns}
                }
                processed.append(record)
            
            self.processed_data = processed
            self.logger.info(f"Successfully preprocessed {len(processed)} records")
            return processed
            
        except Exception as e:
            self.logger.log_error(e, "Error preprocessing DataFrame")
            raise
    
    def _extract_text_content(self, row: pd.Series, text_columns: List[str]) -> str:
        """
        Extract and combine text content from specified columns.
        
        Args:
            row: DataFrame row
            text_columns: Columns to extract text from
            
        Returns:
            Combined text content
        """
        text_parts = []
        for col in text_columns:
            if col in row and pd.notna(row[col]):
                text_parts.append(str(row[col]))
        return " ".join(text_parts)
    
    def chunk_text(self, text: str, chunk_size: int = 1000, 
                   overlap: int = 200) -> List[str]:
        """
        Split text into chunks for processing.
        
        Args:
            text: Input text
            chunk_size: Maximum chunk size in characters
            overlap: Overlap between chunks in characters
            
        Returns:
            List of text chunks
        """
        try:
            if len(text) <= chunk_size:
                return [text]
            
            chunks = []
            start = 0
            while start < len(text):
                end = start + chunk_size
                chunk = text[start:end]
                chunks.append(chunk)
                start = end - overlap  # Overlap for context preservation
            
            self.logger.info(f"Split text into {len(chunks)} chunks")
            return chunks
            
        except Exception as e:
            self.logger.log_error(e, "Error chunking text")
            raise
    
    def validate_data(self, data: Any) -> bool:
        """
        Validate data before processing.
        
        Args:
            data: Data to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            if data is None:
                self.logger.warning("Data is None")
                return False
            
            if isinstance(data, (list, dict)):
                if len(data) == 0:
                    self.logger.warning("Data is empty")
                    return False
            
            if isinstance(data, pd.DataFrame):
                if data.empty:
                    self.logger.warning("DataFrame is empty")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.log_error(e, "Error validating data")
            return False
    
    def load_ist_concepts(self, file_path: str = "data/ist_concepts.csv") -> pd.DataFrame:
        """
        Load IST concepts knowledge base.
        
        Args:
            file_path: Path to IST concepts CSV file
            
        Returns:
            DataFrame with IST concepts
        """
        try:
            return self.load_csv(file_path)
        except Exception as e:
            self.logger.log_error(e, f"Error loading IST concepts from {file_path}")
            raise
    
    def get_concepts_by_week(self, df: pd.DataFrame, week: str) -> pd.DataFrame:
        """
        Filter concepts by week.
        
        Args:
            df: IST concepts DataFrame
            week: Week identifier (e.g., "W00", "W01")
            
        Returns:
            Filtered DataFrame
        """
        return df[df['week'].str.upper() == week.upper()]
    
    def get_concept_info(self, df: pd.DataFrame, concept_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a specific concept.
        
        Args:
            df: IST concepts DataFrame
            concept_name: Name of the concept
            
        Returns:
            Dictionary with concept information or None
        """
        concept = df[df['concept_name'].str.lower() == concept_name.lower()]
        if not concept.empty:
            return concept.iloc[0].to_dict()
        return None