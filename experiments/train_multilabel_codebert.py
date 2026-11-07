import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split

# LOAD DATA
df = pd.read_csv("dataset/multilabel_dataset.csv")
df["labels"] = df["labels"].apply(lambda x: x.split(","))

mlb = MultiLabelBinarizer()
y = mlb.fit_transform(df["labels"])

X_train, X_test, y_train, y_test = train_test_split(df["code"], y, test_size=0.2)

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")

def tokenize(x):
    return tokenizer(list(x), padding=True, truncation=True, return_tensors="pt")

train_enc = tokenize(X_train)
train_labels = torch.tensor(y_train).float()

model = AutoModelForSequenceClassification.from_pretrained(
    "microsoft/codebert-base",
    num_labels=len(mlb.classes_),
    problem_type="multi_label_classification"
)

optimizer = torch.optim.AdamW(model.parameters(), lr=5e-5)

for epoch in range(3):
    model.train()
    outputs = model(**train_enc, labels=train_labels)
    loss = outputs.loss
    loss.backward()
    optimizer.step()
    optimizer.zero_grad()
    print("Epoch", epoch+1, "Loss:", loss.item())

model.save_pretrained("saved_model")
tokenizer.save_pretrained("saved_model")

print("Model saved successfully")