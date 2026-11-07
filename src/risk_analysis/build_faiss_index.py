import numpy as np
from src.risk_analysis.faiss_index import RiskSignatureIndex

EMB_PATH = "data/processed/embeddings.npy"

def build_index():
    embeddings = np.load(EMB_PATH)
    dim = embeddings.shape[1]

    index = RiskSignatureIndex(dim)
    index.add_embeddings(embeddings)

    print(f"[✔] FAISS index built with {index.index.ntotal} vectors")
    return index

if __name__ == "__main__":
    build_index()
