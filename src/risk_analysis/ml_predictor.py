import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class MLPredictor:

    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.labels = ["sql_injection","command_injection","xss","weak_random","hardcoded_credentials"]

        try:
            self.tokenizer = AutoTokenizer.from_pretrained("saved_model")
            self.model = AutoModelForSequenceClassification.from_pretrained("saved_model")
        except:
            pass

    def predict(self, code):

        if not self.model:
            return []

        inputs = self.tokenizer(code, return_tensors="pt", truncation=True)

        with torch.no_grad():
            logits = self.model(**inputs).logits

        probs = torch.sigmoid(logits)[0]

        preds = [self.labels[i] for i,p in enumerate(probs) if p > 0.5]

        return preds