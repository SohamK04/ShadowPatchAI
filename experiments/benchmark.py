from src.risk_analysis.risk_predictor import RiskPredictor

predictor = RiskPredictor()

test_cases = [
    "SELECT * FROM users WHERE id = " + "user",
    "os.system(user_input)",
    "random.random()",
    "<h1>" + "user" + "</h1>",
]

print("\n===== BENCHMARK =====")

for code in test_cases:
    result = predictor.predict(code)
    print("\nCode:", code)
    print("Prediction:", result)