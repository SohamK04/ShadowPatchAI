import numpy as np

from src.risk_analysis.risk_predictor import RiskPredictor
from src.patch_generation.patch_generator import PatchGenerator
from src.explainability.explanation_engine import ExplanationEngine
from src.validation.patch_validator import PatchValidator


# Load embeddings
embeddings = np.load("data/processed/embeddings.npy", allow_pickle=True)
metadata = np.load("data/processed/metadata.npy", allow_pickle=True)


# Initialize modules
predictor = RiskPredictor(embeddings, metadata)
patcher = PatchGenerator(mode="mock")
explainer = ExplanationEngine()
validator = PatchValidator()


# Test vulnerable code
test_code = """
String query = "SELECT * FROM users WHERE id = " + userInput;
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(query);
"""


# STEP 1: Risk prediction
result = predictor.predict(test_code)
print("Risk Analysis:", result)


# STEP 2: Patch generation
patched = patcher.generate_patch(
    test_code,
    result["predicted_vulnerability"]
)

print("\nGenerated Patch:\n", patched)


# STEP 3: Validation
validation = validator.validate(
    patched,
    result["predicted_vulnerability"]
)

print("\nValidation Result:", validation)


# STEP 4: Explanation
explanation = explainer.explain(result["predicted_vulnerability"])
print("\nExplanation:\n", explanation)
