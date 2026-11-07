from fastapi import FastAPI
from embedding.code_embedder import CodeEmbedder

app = FastAPI()
embedder = CodeEmbedder()

@app.post("/analyze")
def analyze_code(code: str):
    embedding = embedder.embed_code(code)
    return {"status": "analyzed"}
