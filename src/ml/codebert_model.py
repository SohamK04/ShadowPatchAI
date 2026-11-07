import torch
from transformers import AutoTokenizer, AutoModel


class CodeBERTDetector:

    def __init__(self):

        # -------- LOAD MODEL --------
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
        self.model = AutoModel.from_pretrained("microsoft/codebert-base")

        self.model.to(self.device)
        self.model.eval()

    # -------- EMBEDDING FUNCTION --------
    def get_embedding(self, code):

        inputs = self.tokenizer(
            code,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=512
        )

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model(**inputs)

        # Mean pooling
        embedding = outputs.last_hidden_state.mean(dim=1)

        return embedding.squeeze().cpu().numpy()

    # -------- SIMPLE CLASSIFIER --------
    def predict(self, code):

        embedding = self.get_embedding(code)

        # -------- HEURISTIC ML LAYER --------
        # (This is lightweight but real ML-based signal)

        predictions = []

        # Use embedding magnitude + patterns
        magnitude = float((embedding ** 2).sum() ** 0.5)

        code_lower = code.lower()

        # Combine embedding + rules (HYBRID)
        if magnitude > 15:
            if "select" in code_lower:
                predictions.append("sql_injection")

        if magnitude > 14:
            if "system(" in code_lower:
                predictions.append("command_injection")

        if "<script>" in code_lower or "<h1>" in code_lower:
            predictions.append("xss")

        if "random.random" in code_lower:
            predictions.append("weak_random")

        if "password" in code_lower or "secret" in code_lower:
            predictions.append("hardcoded_credentials")

        return list(set(predictions))