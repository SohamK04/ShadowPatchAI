import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt


# -------- LOAD DATA --------
df = pd.read_csv("dataset/code_vuln_dataset.csv")

labels = list(df["label"].unique())
label_map = {l:i for i,l in enumerate(labels)}

df["label_id"] = df["label"].map(label_map)

train_texts, test_texts, train_labels, test_labels = train_test_split(
    df["code"], df["label_id"], test_size=0.2
)

# -------- TOKENIZER --------
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")

def tokenize(texts):
    return tokenizer(
        list(texts),
        padding=True,
        truncation=True,
        return_tensors="pt"
    )

train_encodings = tokenize(train_texts)
test_encodings = tokenize(test_texts)

train_labels = torch.tensor(train_labels.values)
test_labels = torch.tensor(test_labels.values)

# -------- MODEL --------
model = AutoModelForSequenceClassification.from_pretrained(
    "microsoft/codebert-base",
    num_labels=len(labels)
)

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

# -------- TRAIN --------
epochs = 3
losses = []

for epoch in range(epochs):

    model.train()
    outputs = model(**train_encodings, labels=train_labels)

    loss = outputs.loss
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()

    losses.append(loss.item())

    print(f"Epoch {epoch+1} Loss:", loss.item())

# -------- EVAL --------
model.eval()
with torch.no_grad():
    outputs = model(**test_encodings)

preds = torch.argmax(outputs.logits, dim=1)

accuracy = accuracy_score(test_labels, preds)
precision = precision_score(test_labels, preds, average="weighted")
recall = recall_score(test_labels, preds, average="weighted")
f1 = f1_score(test_labels, preds, average="weighted")

print("\n===== METRICS =====")
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)

# -------- GRAPH --------
plt.plot(losses)
plt.title("Training Loss")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.show()