from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import zipfile, os, tempfile, time, uuid, pandas as pd
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# === Import all AI Agents ===
from agents import (
    cibil_agent,
    income_agent,
    dti_agent,
    employment_agent,
    existing_loans_agent,
    age_agent
)

# === Import Two-Layer Security Modules ===
from agents.security_layer1 import verify_access_token
from agents.security_layer2 import verify_signature

# === Initialize FastAPI ===
app = FastAPI(title="AI Loan Risk Analyzer (Secure Bank Edition)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "status": "✅ Running",
        "version": "3.0",
        "mode": "Bank-Oriented (Secure)",
        "description": "Bulk loan eligibility evaluator with 2-Layer Security and OCR for salary slips."
    }


# === BULK EVALUATE ENDPOINT (now secured) ===
@app.post("/bulk_evaluate")
async def bulk_evaluate(
    file: UploadFile = File(...),
    token: str = "",
    signature: str = ""
):
    """
    Secure enterprise-grade bulk evaluation:
      • Requires valid token & digital signature.
      • Accepts ZIP with salary slips (.jpg/.png/.pdf) or CSVs.
      • Runs OCR + 6 Agentic AIs (CIBIL, Income, DTI, Employment, Existing Loans, Age).
    """

    # 🔐 Layer 1 — Authentication
    if not verify_access_token(token):
        return JSONResponse(
            {"error": "❌ Invalid or expired token. Access denied."},
            status_code=401
        )

    # 🔐 Layer 2 — Signature Verification
    if not verify_signature(signature):
        return JSONResponse(
            {"error": "❌ Invalid signature. Possible tampering detected."},
            status_code=403
        )

    # 🧩 Proceed after successful security verification
    start_time = time.time()
    temp_dir = tempfile.mkdtemp()
    results = []
    processed_files = 0

    # 1️⃣ Extract ZIP
    try:
        with zipfile.ZipFile(file.file, "r") as z:
            z.extractall(temp_dir)
    except Exception as e:
        return JSONResponse({"error": f"Invalid ZIP file: {e}"}, status_code=400)

    # 2️⃣ Iterate through extracted files
    for root, _, files in os.walk(temp_dir):
        for fname in files:
            fpath = os.path.join(root, fname)
            ext = fname.lower().split(".")[-1]

            # --- OCR for salary slips (images) ---
            if ext in ["jpg", "jpeg", "png"]:
                try:
                    img = Image.open(fpath)
                    raw_text = pytesseract.image_to_string(img)
                    digits = "".join(ch if ch.isdigit() else " " for ch in raw_text)
                    numbers = [int(x) for x in digits.split() if x.isdigit()]
                    if numbers:
                        salary = max(numbers)
                        res = {
                            "applicant": fname,
                            "ocr_text": raw_text.strip(),
                            "salary_detected": salary,
                            "cibil": cibil_agent.evaluate_cibil(750),
                            "income": income_agent.evaluate_income(salary, 24),
                            "dti": dti_agent.evaluate_dti(salary, 0, 200000, 12),
                            "employment": employment_agent.evaluate_employment("salaried", 2),
                            "existing": existing_loans_agent.evaluate_existing_loans(0, 0, 0),
                            "age": age_agent.evaluate_age(30),
                        }
                        res["avg_score"] = round(sum(v["score"] for v in res.values() if isinstance(v, dict)) / 6, 2)
                        results.append(res)
                        processed_files += 1
                except Exception as e:
                    print(f"OCR error in {fname}: {e}")

            # --- Structured CSV Data ---
            elif ext == "csv":
                df = pd.read_csv(fpath)
                for _, row in df.iterrows():
                    salary = float(row.get("salary", 0))
                    age = int(row.get("age", 30))
                    cibil = int(row.get("cibil_score", 700))
                    emp_type = str(row.get("employment_type", "salaried"))
                    active_loans = int(row.get("active_loans", 0))
                    total_outstanding = float(row.get("total_outstanding", 0))
                    emis = float(row.get("existing_emis", 0))
                    loan_amount = float(row.get("loan_amount", 100000))
                    tenure = int(row.get("tenure_months", 12))
                    stability = int(row.get("job_stability", 24))

                    res = {
                        "applicant": row.get("name", fname),
                        "cibil": cibil_agent.evaluate_cibil(cibil),
                        "income": income_agent.evaluate_income(salary, stability),
                        "dti": dti_agent.evaluate_dti(salary, emis, loan_amount, tenure),
                        "employment": employment_agent.evaluate_employment(emp_type, stability // 12),
                        "existing": existing_loans_agent.evaluate_existing_loans(active_loans, total_outstanding, emis),
                        "age": age_agent.evaluate_age(age),
                    }
                    res["avg_score"] = round(sum(v["score"] for v in res.values()) / 6, 2)
                    results.append(res)
                    processed_files += 1

    # 3️⃣ Handle empty or invalid ZIPs
    if not results:
        debug_files = []
        for root, _, files in os.walk(temp_dir):
            for f in files:
                debug_files.append(os.path.join(root, f))
        return JSONResponse(
            {"error": "No valid files processed.", "debug_files": debug_files, "count_seen": processed_files},
            status_code=400,
        )

    # 4️⃣ Summary Analytics
    avg_total = sum(r["avg_score"] for r in results) / len(results)
    top_candidates = sorted(results, key=lambda x: x["avg_score"], reverse=True)[:10]
    pass_count = sum(1 for r in results if r["avg_score"] >= 80)
    warn_count = sum(1 for r in results if 60 <= r["avg_score"] < 80)
    fail_count = len(results) - pass_count - warn_count

    # 5️⃣ Final Secure Response
    return JSONResponse(
        {
            "batch_id": str(uuid.uuid4()),
            "total_records": len(results),
            "average_score": round(avg_total, 2),
            "distribution": {"PASS": pass_count, "WARN": warn_count, "FAIL": fail_count},
            "top_candidates": top_candidates,
            "processing_time_seconds": round(time.time() - start_time, 2),
            "status": "✅ Secure bulk evaluation completed successfully"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agents.main:app", host="0.0.0.0", port=8000, reload=True)
