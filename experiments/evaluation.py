import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

from src.embedding.code_embedder import CodeEmbedder
from src.risk_analysis.risk_predictor import RiskPredictor
from src.patch_generation.patch_generator import PatchGenerator
from src.validation.patch_validator import PatchValidator


# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/processed/labeled_snippets.csv")

# ---------------- SPLIT ----------------
train_df = df.sample(frac=0.7, random_state=42)
test_df = df.drop(train_df.index)

print(f"Train samples: {len(train_df)}")
print(f"Test samples: {len(test_df)}")

# ---------------- EMBEDDINGS ----------------
embedder = CodeEmbedder()
train_embeddings = embedder.embed(train_df["code_snippet"].tolist())
train_metadata = train_df[["vulnerability_type", "source"]].to_dict("records")

# ---------------- INIT ----------------
predictor = RiskPredictor(train_embeddings, train_metadata)
patcher = PatchGenerator(mode="mock")
validator = PatchValidator()

classes = df["vulnerability_type"].unique()

# ---------------- METRICS STORAGE ----------------
conf_matrix = defaultdict(lambda: defaultdict(int))
risk_scores = []
validation_scores = []

correct = 0
total = len(test_df)

# ---------------- EVALUATION ----------------
for _, row in test_df.iterrows():
    code = row["code_snippet"]
    true_label = row["vulnerability_type"]

    result = predictor.predict(code)
    pred_label = result["predicted_vulnerability"]

    risk_scores.append(result["risk_score"])

    # Confusion matrix update
    conf_matrix[true_label][pred_label] += 1

    if pred_label == true_label:
        correct += 1

    # Patch validation
    patched = patcher.generate_patch(code, pred_label)
    val = validator.validate(patched, pred_label)
    validation_scores.append(val["score"])


# ---------------- BASIC METRICS ----------------
accuracy = correct / total if total > 0 else 0

print("\n===== OVERALL METRICS =====")
print("Accuracy:", round(accuracy, 3))
print("Avg Risk Score:", round(np.mean(risk_scores), 3))
print("Avg Validation Score:", round(np.mean(validation_scores), 3))


# ---------------- PRECISION / RECALL / F1 ----------------
print("\n===== CLASS-WISE METRICS =====")

for cls in classes:
    tp = conf_matrix[cls][cls]
    fp = sum(conf_matrix[other][cls] for other in classes if other != cls)
    fn = sum(conf_matrix[cls][other] for other in classes if other != cls)

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0

    print(f"\nClass: {cls}")
    print("Precision:", round(precision, 3))
    print("Recall:", round(recall, 3))
    print("F1 Score:", round(f1, 3))


# ---------------- CONFUSION MATRIX PRINT ----------------
print("\n===== CONFUSION MATRIX =====")
for true_cls in classes:
    print(f"{true_cls} -> {dict(conf_matrix[true_cls])}")


# ---------------- FALSE POSITIVE RATE (IMPORTANT) ----------------
print("\n===== FALSE POSITIVE RATE =====")

for cls in classes:
    fp = sum(conf_matrix[other][cls] for other in classes if other != cls)
    tn = sum(
        conf_matrix[o1][o2]
        for o1 in classes for o2 in classes
        if o1 != cls and o2 != cls
    )

    fpr = fp / (fp + tn) if (fp + tn) else 0
    print(f"{cls} FPR:", round(fpr, 3))


# ---------------- PLOTS ----------------

# Risk Score Distribution
plt.figure()
plt.hist(risk_scores)
plt.title("Risk Score Distribution")
plt.xlabel("Risk Score")
plt.ylabel("Frequency")
plt.savefig("risk_distribution.png")

# Validation Score Distribution
plt.figure()
plt.hist(validation_scores)
plt.title("Validation Score Distribution")
plt.xlabel("Validation Score")
plt.ylabel("Frequency")
plt.savefig("validation_distribution.png")

# Confusion Matrix Heatmap (simple)
matrix = []
for t in classes:
    row = []
    for p in classes:
        row.append(conf_matrix[t][p])
    matrix.append(row)

plt.figure()
plt.imshow(matrix)
plt.title("Confusion Matrix")
plt.colorbar()
plt.xticks(range(len(classes)), classes, rotation=45)
plt.yticks(range(len(classes)), classes)
plt.savefig("confusion_matrix.png")

print("\nGraphs saved: risk_distribution.png, validation_distribution.png, confusion_matrix.png")