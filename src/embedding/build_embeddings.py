import pandas as pd
import numpy as np
from src.embedding.code_embedder import CodeEmbedder

DATA_PATH = "data/processed/labeled_snippets.csv"
OUT_EMB = "data/processed/embeddings.npy"
OUT_META = "data/processed/metadata.npy"

def build():
    df = pd.read_csv(DATA_PATH)

    code_snippets = df["code_snippet"].tolist()
    metadata = df[["vulnerability_type", "source"]].to_dict("records")

    embedder = CodeEmbedder()
    embeddings = embedder.embed(code_snippets)

    np.save(OUT_EMB, embeddings)
    np.save(OUT_META, metadata)

    print(f"[✔] Saved {len(embeddings)} embeddings")

if __name__ == "__main__":
    build()
