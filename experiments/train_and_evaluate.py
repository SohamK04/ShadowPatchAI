import random
from src.risk_analysis.risk_predictor import RiskPredictor

predictor = RiskPredictor()

# -------- DATASET --------
dataset = [
    ("SELECT * FROM users WHERE id = " + "user", "sql_injection"),
    ("os.system(user_input)", "command_injection"),
    ("random.random()", "weak_random"),
    ("password = '1234'", "hardcoded_credentials"),
    ("<h1>" + "user" + "</h1>", "xss"),
    ("print('hello')", "safe"),
] * 50  # 🔥 expand dataset

random.shuffle(dataset)

train = dataset[:200]
test = dataset[200:]

# -------- EVAL --------
correct = 0

for code, label in test:
    pred = predictor.predict(code)["predicted_vulnerability"]

    if label in pred or (label == "safe" and "safe" in pred):
        correct += 1

accuracy = correct / len(test)

print("\n===== FINAL RESULTS =====")
print("Accuracy:", round(accuracy, 2))