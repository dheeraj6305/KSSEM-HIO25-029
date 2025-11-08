from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# --- Import your modules ---
from ocr_utils import extract_salary_from_image
from model_utils import predict_eligibility
from risk_utils import evaluate_risk
from xai_utils import generate_explanation

# --- Initialize FastAPI app ---
app = FastAPI(title="KSSEM HACKATHON: Nexus Loan AI", version="1.0")

# --- Enable CORS for frontend (Dheeraj's part) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Test route ---
@app.get("/")
def home():
    return {"message": "🚀 Backend is running successfully!"}


# --- OCR route ---
@app.post("/ocr")
async def ocr_endpoint(file: UploadFile):
    try:
        contents = await file.read()
        temp_path = "temp_image.jpg"
        with open(temp_path, "wb") as f:
            f.write(contents)

        result = extract_salary_from_image(temp_path)
        os.remove(temp_path)
        return {"status": "success", "ocr_result": result}

    except Exception as e:
        return {"status": "error", "message": str(e)}


# --- Predict route ---
@app.post("/predict")
async def predict_endpoint(
    salary: float = Form(...),
    credit_score: int = Form(...),
    loan_amount: float = Form(...),
    tenure: int = Form(...),
):
    result = predict_eligibility(salary, credit_score, loan_amount, tenure)
    return {"status": "success", "prediction": result}


# --- Risk detection route ---
@app.post("/risk")
async def risk_endpoint(
    salary: float = Form(...),
    credit_score: int = Form(...),
    loan_amount: float = Form(...),
    tenure: int = Form(...),
):
    result = evaluate_risk(salary, loan_amount, credit_score, tenure)
    return {"status": "success", "risk_analysis": result}


# --- XAI route ---
@app.post("/xai")
async def xai_endpoint(
    salary: float = Form(...),
    credit_score: int = Form(...),
    loan_amount: float = Form(...),
    tenure: int = Form(...),
    approved: int = Form(...),
):
    result = generate_explanation(salary, credit_score, loan_amount, tenure, approved)
    return {"status": "success", "explanation": result}


# --- Master route: /process_application ---
@app.post("/process_application")
async def process_application(
    file: UploadFile,
    credit_score: int = Form(...),
    loan_amount: float = Form(...),
    tenure: int = Form(...),
):
    """
    Complete pipeline → OCR + ML + Risk + XAI
    """

    # Step 1: OCR
    temp_path = "temp_image.jpg"
    contents = await file.read()
    with open(temp_path, "wb") as f:
        f.write(contents)
    ocr_result = extract_salary_from_image(temp_path)
    os.remove(temp_path)

    # Step 2: ML Prediction
    ml_result = predict_eligibility(
        salary=ocr_result["salary"],
        credit_score=credit_score,
        loan_amount=loan_amount,
        tenure=tenure
    )

    # Step 3: Risk Detection
    risk_result = evaluate_risk(
        salary=ocr_result["salary"],
        loan_amount=loan_amount,
        credit_score=credit_score,
        tenure=tenure
    )

    # Step 4: Explainable AI
    xai_result = generate_explanation(
        salary=ocr_result["salary"],
        credit_score=credit_score,
        loan_amount=loan_amount,
        tenure=tenure,
        approved=ml_result["approved"]
    )

    # Combine all results
    return {
        "ocr": ocr_result,
        "ml": ml_result,
        "risk": risk_result,
        "xai": xai_result
    }


# --- Run app ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
