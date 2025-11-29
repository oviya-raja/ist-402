from typing import List, Dict, Any
from .environment import EnvironmentConfig
from .config import OUTPUT_DIR

class JobFitmentVectorDB:
    """
    FAISS vector database for semantic job matching.
    Converts text to embeddings and enables similarity search.
    """
    
    EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
    EMBEDDING_DIM = 384
    TOP_K = 5
    
    def __init__(self, env: EnvironmentConfig):
        self.env = env
        self.embedding_model = None
        self.faiss_index = None
        self.embeddings = None
        self.documents = []
    
    def load_embedding_model(self):
        """Load the sentence transformer model."""
        if self.env.SentenceTransformer is None:
            raise RuntimeError("SentenceTransformer not available. Ensure environment is properly initialized.")
        
        print(f"   Loading embedding model: {self.EMBEDDING_MODEL}")
        self.embedding_model = self.env.SentenceTransformer(self.EMBEDDING_MODEL)
        if self.embedding_model is not None:
            print(f"   ✅ Model loaded (dim: {self.embedding_model.get_sentence_embedding_dimension()})")
        return self.embedding_model
    
    def generate_embeddings(self, texts: List[str]) -> 'np.ndarray':
        """Generate embeddings for texts."""
        if not self.embedding_model:
            self.load_embedding_model()
        
        if self.embedding_model is None:
            raise RuntimeError("Embedding model not loaded. Cannot generate embeddings.")
        
        embeddings = self.embedding_model.encode(
            texts, 
            show_progress_bar=True, 
            convert_to_numpy=True
        )
        return embeddings.astype('float32')
    
    def build_index(self, documents: List[Dict[str, Any]], text_key: str = "question"):
        """Build FAISS index from documents."""
        print("🗄️  Building FAISS index...")
        
        if self.env.faiss is None:
            raise RuntimeError("FAISS not available. Ensure environment is properly initialized.")
        
        self.documents = documents
        texts = [doc.get(text_key, "") + " " + doc.get("answer", "") for doc in documents]
        
        # Generate embeddings
        self.embeddings = self.generate_embeddings(texts)
        
        # Create FAISS index
        dimension = self.embeddings.shape[1]
        self.faiss_index = self.env.faiss.IndexFlatL2(dimension)
        self.faiss_index.add(self.embeddings)
        
        print(f"   ✅ Index built: {self.faiss_index.ntotal} vectors, {dimension} dimensions")
        return self.faiss_index
    
    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Search for similar documents."""
        if top_k is None:
            top_k = self.TOP_K
        
        if self.embedding_model is None:
            raise RuntimeError("Embedding model not loaded. Cannot search.")
        
        if self.faiss_index is None:
            raise RuntimeError("FAISS index not built. Call build_index() first.")
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(
            [query], 
            convert_to_numpy=True
        ).astype('float32')
        
        # Search FAISS
        distances, indices = self.faiss_index.search(query_embedding, top_k)
        
        # Get results with scores
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.documents):
                doc = self.documents[idx].copy()
                doc['similarity_score'] = float(1 / (1 + dist))
                doc['distance'] = float(dist)
                results.append(doc)
        
        return results
    
    def embed_query(self, query: str) -> 'np.ndarray':
        """Convert query to embedding vector."""
        if not self.embedding_model:
            self.load_embedding_model()
        
        if self.embedding_model is None:
            raise RuntimeError("Embedding model not loaded. Cannot embed query.")
        
        return self.embedding_model.encode([query], convert_to_numpy=True).astype('float32')[0]
    
    def save_index(self, filename: str = "job_fitment.faiss"):
        """Save FAISS index to file."""
        if self.faiss_index is None:
            raise RuntimeError("FAISS index not built. Nothing to save.")
        
        if self.env.faiss is None or self.env.np is None:
            raise RuntimeError("FAISS or NumPy not available. Ensure environment is properly initialized.")
        
        if self.embeddings is None:
            raise RuntimeError("Embeddings not generated. Nothing to save.")
        
        filepath = OUTPUT_DIR / filename
        self.env.faiss.write_index(self.faiss_index, str(filepath))
        print(f"✅ Saved: {filepath}")
        
        # Save embeddings
        emb_path = OUTPUT_DIR / "embeddings.npy"
        self.env.np.save(emb_path, self.embeddings)
        print(f"✅ Saved: {emb_path}")
        
        return str(filepath)

