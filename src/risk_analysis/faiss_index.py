import faiss
import numpy as np

class RiskSignatureIndex:
    def __init__(self, embedding_dim):
        self.index = faiss.IndexFlatIP(embedding_dim)

    def add_embeddings(self, embeddings):
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings)

    def search(self, query_embedding, top_k=5):
        faiss.normalize_L2(query_embedding)
        scores, indices = self.index.search(query_embedding, top_k)
        return scores[0], indices[0]
