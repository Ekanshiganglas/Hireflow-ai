"""
Semantic Embedding Model
Understands meaning of text using AI
"""

from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import os

class SemanticMatcher:
    """
    Converts text to embeddings and measures similarity
    
    Simple explanation:
    - Embeddings = Converting text to numbers
    - Similar meanings = Similar numbers
    - "Python dev" ≈ "Python programmer" (90%+ similar)
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Load the AI model
        
        Model: all-MiniLM-L6-v2
        - Fast (works on CPU)
        - Accurate enough for resume matching
        - Size: ~80MB
        """
        print(f"🔄 Loading embedding model: {model_name}...")
        print("   (This takes 10-20 seconds on first run)")
        
        # Create cache directory
        cache_dir = os.path.join(os.getcwd(), 'models', 'embeddings')
        os.makedirs(cache_dir, exist_ok=True)
        
        # Load model
        self.model = SentenceTransformer(
            model_name,
            cache_folder=cache_dir
        )
        
        print("✅ Model loaded successfully!")
    
    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Convert text to embeddings (numbers)
        
        Args:
            texts: Single text or list of texts
        
        Returns:
            Array of numbers representing the meaning
        
        Example:
            >>> matcher = SemanticMatcher()
            >>> embedding = matcher.encode("Python developer")
            >>> print(embedding.shape)
            (384,)  # 384 numbers!
        """
        if isinstance(texts, str):
            texts = [texts]
        
        embeddings = self.model.encode(
            texts,
            show_progress_bar=False,
            convert_to_numpy=True
        )
        
        return embeddings
    
    def semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate how similar two texts are (0-1)
        
        Args:
            text1: First text
            text2: Second text
        
        Returns:
            Similarity score (0=different, 1=identical)
        
        Example:
            >>> matcher = SemanticMatcher()
            >>> score = matcher.semantic_similarity(
            ...     "Python developer",
            ...     "Python programmer"
            ... )
            >>> print(f"{score:.2%}")
            92%  # Very similar!
        """
        # Convert both texts to embeddings
        emb1 = self.encode(text1)
        emb2 = self.encode(text2)
        
        # Calculate cosine similarity
        # (measures angle between vectors)
        similarity = np.dot(emb1[0], emb2[0]) / (
            np.linalg.norm(emb1[0]) * np.linalg.norm(emb2[0])
        )
        
        return float(similarity)


# Test code - only runs when you execute this file directly
if __name__ == "__main__":
    print("\n" + "="*60)
    print("TESTING SEMANTIC MATCHER")
    print("="*60 + "\n")
    
    # Initialize
    matcher = SemanticMatcher()
    
    # Test 1: Similar meanings
    print("Test 1: Similar Job Titles")
    similarity = matcher.semantic_similarity(
        "Python developer",
        "Python programmer"
    )
    print(f"  'Python developer' vs 'Python programmer'")
    print(f"  Similarity: {similarity:.2%}\n")
    
    # Test 2: Related concepts
    print("Test 2: Related Concepts")
    similarity = matcher.semantic_similarity(
        "Machine learning engineer",
        "ML specialist with AI experience"
    )
    print(f"  'Machine learning engineer' vs 'ML specialist'")
    print(f"  Similarity: {similarity:.2%}\n")
    
    # Test 3: Different concepts
    print("Test 3: Different Concepts")
    similarity = matcher.semantic_similarity(
        "Python developer",
        "Chef with cooking experience"
    )
    print(f"  'Python developer' vs 'Chef'")
    print(f"  Similarity: {similarity:.2%}\n")
    
    print("="*60)
    print("✅ All tests completed!")
    print("="*60)