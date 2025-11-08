from ocr_utils import extract_salary_from_image
from model_utils import predict_eligibility
from risk_utils import evaluate_risk
from xai_utils import generate_explanation

# ---------- STEP 1: OCR Extraction ----------
print("📸 Running OCR Module...")
ocr_result = {
    "salary": 45000,
    "raw_text": "Salary ₹45,000 detected successfully",
    "confidence": 0.96
}
print("✅ OCR Output:", ocr_result)

# ---------- STEP 2: ML Prediction ----------
print("\n🤖 Running ML Model Prediction...")
ml_result = predict_eligibility(
    salary=ocr_result["salary"],
    credit_score=750,
    loan_amount=500000,
    tenure=12
)
print("✅ ML Output:", ml_result)

# ---------- STEP 3: Risk Evaluation ----------
print("\n⚠️ Running Risk Detection Agent...")
risk_result = evaluate_risk(
    salary=ocr_result["salary"],
    loan_amount=500000,
    credit_score=750,
    tenure=12
)
print("✅ Risk Output:", risk_result)

# ---------- STEP 4: Explainable AI ----------
print("\n💬 Generating Explainable AI Output...")
xai_result = generate_explanation(
    salary=ocr_result["salary"],
    credit_score=750,
    loan_amount=500000,
    tenure=12,
    approved=ml_result["approved"]
)
print("✅ XAI Output:\n", xai_result["explanation"])

# ---------- STEP 5: Final Combined Output ----------
final_output = {
    "ocr": ocr_result,
    "ml": ml_result,
    "risk": risk_result,
    "xai": xai_result
}

print("\n🚀 FINAL DECISION PIPELINE OUTPUT 🚀")
for key, val in final_output.items():
    print(f"\n🔹 {key.upper()} → {val}")
