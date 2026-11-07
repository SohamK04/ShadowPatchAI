import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class RiskAnalyzer:
    def __init__(self, risk_embeddings, threshold=0.75):
        self.risk_embeddings = risk_embeddings
        self.threshold = threshold

    def analyze(self, code_embedding):
        sims = cosine_similarity(
            [code_embedding], self.risk_embeddings
        )[0]

        max_score = np.max(sims)
        is_risky = max_score > self.threshold

        return {
            "risk_score": float(max_score),
            "is_risky": is_risky
        }
