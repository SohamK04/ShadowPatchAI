from sentence_transformers import SentenceTransformer
import numpy as np

class CodeEmbedder:
    def __init__(self, model_name="microsoft/codebert-base"):
        self.model = SentenceTransformer(model_name)

    def embed(self, code_snippets):
        """
        code_snippets: List[str]
        returns: numpy array of embeddings
        """
        embeddings = self.model.encode(
            code_snippets,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        return embeddings
