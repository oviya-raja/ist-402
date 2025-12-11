"""
Data Preprocessing Module
Handles ingestion and preprocessing of real-world data (CSV, text files).
Includes vector search functionality using OpenAI embeddings.
"""

import csv
import json
import os
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np

from core.logger import get_logger

logger = get_logger()

# Try to import FAISS for vector storage
try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS not installed. Install with: pip install faiss-cpu")

# Try to import OpenAI for embeddings
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI not installed. Install with: pip install openai")


class DataProcessor:
    """
    Processes various data formats and prepares them for GenAI consumption.
    Handles CSV, JSON, and text file formats with proper error handling.
    Includes vector search functionality using OpenAI embeddings and FAISS.
    """
    
    def __init__(self):
        """Initialize data processor."""
        self.logger = logger
        self.processed_data: List[Dict[str, Any]] = []
        self.vector_store = None
        self.text_chunks = []
        self.metadata = []
        self.embeddings_model = None
        
        # Initialize OpenAI client for embeddings if available
        if OPENAI_AVAILABLE:
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                try:
                    self.embeddings_model = OpenAI(api_key=api_key)
                    self.logger.info("OpenAI embeddings client initialized")
                except Exception as e:
                    self.logger.warning(f"Could not initialize OpenAI client: {str(e)}")
            else:
                self.logger.warning("OPENAI_API_KEY not found. Vector search will not be available.")
    
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
    
    def create_embeddings(self, texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
        """
        Create embeddings for a list of texts using OpenAI.
        
        Args:
            texts: List of text strings to embed
            model: OpenAI embedding model to use (default: text-embedding-3-small)
            
        Returns:
            List of embedding vectors
        """
        if not self.embeddings_model:
            raise ValueError("OpenAI client not initialized. Please set OPENAI_API_KEY.")
        
        try:
            self.logger.info(f"Creating embeddings for {len(texts)} texts using {model}")
            # OpenAI embeddings API
            response = self.embeddings_model.embeddings.create(
                model=model,
                input=texts
            )
            
            embeddings = [item.embedding for item in response.data]
            self.logger.info(f"Created {len(embeddings)} embeddings of dimension {len(embeddings[0]) if embeddings else 0}")
            return embeddings
            
        except Exception as e:
            self.logger.log_error(e, "Error creating embeddings")
            raise
    
    def build_vector_store(self, chunks: List[str], metadata: Optional[List[Dict]] = None, model: str = "text-embedding-3-small"):
        """
        Build a vector store from text chunks using OpenAI embeddings and FAISS.
        
        Args:
            chunks: List of text chunks to embed and store
            metadata: Optional metadata for each chunk
            model: OpenAI embedding model to use
        """
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS not available. Install with: pip install faiss-cpu")
        
        if not self.embeddings_model:
            raise ValueError("OpenAI client not initialized. Please set OPENAI_API_KEY.")
        
        try:
            self.logger.info(f"Building vector store from {len(chunks)} chunks")
            
            # Create embeddings
            embeddings = self.create_embeddings(chunks, model)
            
            # Convert to numpy array
            embeddings_array = np.array(embeddings).astype('float32')
            dimension = embeddings_array.shape[1]
            
            # Create FAISS index (L2 distance)
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings_array)
            
            # Store index, chunks, and metadata
            self.vector_store = index
            self.text_chunks = chunks
            self.metadata = metadata if metadata else [{"chunk_id": i} for i in range(len(chunks))]
            
            self.logger.info(f"Vector store created with {index.ntotal} vectors of dimension {dimension}")
            
        except Exception as e:
            self.logger.log_error(e, "Error building vector store")
            raise
    
    def search_vectors(self, query: str, k: int = 5, model: str = "text-embedding-3-small") -> List[Dict[str, Any]]:
        """
        Search the vector store for similar chunks.
        
        Args:
            query: Search query text
            k: Number of results to return
            model: OpenAI embedding model to use
            
        Returns:
            List of dictionaries with 'chunk', 'score', and 'metadata' keys
        """
        if not self.vector_store:
            raise ValueError("Vector store not built. Call build_vector_store() first.")
        
        if not self.embeddings_model:
            raise ValueError("OpenAI client not initialized. Please set OPENAI_API_KEY.")
        
        try:
            # Create embedding for query
            query_embedding = self.create_embeddings([query], model)[0]
            query_vector = np.array([query_embedding]).astype('float32')
            
            # Search
            k = min(k, self.vector_store.ntotal)  # Don't search for more than available
            distances, indices = self.vector_store.search(query_vector, k)
            
            # Format results
            results = []
            for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
                results.append({
                    'chunk': self.text_chunks[idx],
                    'score': float(distance),
                    'similarity': float(1 / (1 + distance)),  # Convert distance to similarity
                    'metadata': self.metadata[idx] if idx < len(self.metadata) else {},
                    'rank': i + 1
                })
            
            self.logger.info(f"Found {len(results)} results for query: {query[:50]}...")
            return results
            
        except Exception as e:
            self.logger.log_error(e, "Error searching vector store")
            raise
    
    def save_vector_store(self, file_path: str):
        """Save vector store to disk."""
        if not self.vector_store:
            raise ValueError("No vector store to save.")
        
        try:
            save_data = {
                'vector_store': self.vector_store,
                'text_chunks': self.text_chunks,
                'metadata': self.metadata
            }
            
            with open(file_path, 'wb') as f:
                pickle.dump(save_data, f)
            
            self.logger.info(f"Vector store saved to {file_path}")
            
        except Exception as e:
            self.logger.log_error(e, "Error saving vector store")
            raise
    
    def load_vector_store(self, file_path: str):
        """Load vector store from disk."""
        try:
            with open(file_path, 'rb') as f:
                save_data = pickle.load(f)
            
            self.vector_store = save_data['vector_store']
            self.text_chunks = save_data['text_chunks']
            self.metadata = save_data.get('metadata', [])
            
            self.logger.info(f"Vector store loaded from {file_path}")
            
        except Exception as e:
            self.logger.log_error(e, "Error loading vector store")
            raise