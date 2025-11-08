# agents/dti_agent.py
def calculate_emi(principal: float, annual_rate_percent: float, tenure_months: int) -> float:
    """Standard EMI calculation."""
    r = annual_rate_percent / 12 / 100
    n = tenure_months
    if r == 0:
        return principal / n
    emi = principal * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return emi


def evaluate_dti(monthly_income: float, existing_emis: float, loan_amount: float, tenure_months: int) -> dict:
    """
    Evaluates Debt-To-Income ratio for credit risk.
    """
    new_emi = calculate_emi(loan_amount, annual_rate_percent=10.0, tenure_months=tenure_months)
    total_emi = existing_emis + new_emi
    dti = total_emi / monthly_income

    if dti <= 0.35:
        score = 95
        status = "PASS"
        reason = f"DTI ratio {dti:.2f} is healthy. Low debt burden."
    elif 0.35 < dti <= 0.45:
        score = 75
        status = "WARN"
        reason = f"DTI ratio {dti:.2f} is moderate. Manageable risk."
    elif 0.45 < dti <= 0.6:
        score = 50
        status = "WARN"
        reason = f"DTI ratio {dti:.2f} is high. Monitor closely."
    else:
        score = 20
        status = "FAIL"
        reason = f"DTI ratio {dti:.2f} is too high. Likely over-leveraged."

    return {
        "agent": "DTI Agent",
        "score": score,
        "status": status,
        "reason": reason,
        "raw": {
            "monthly_income": monthly_income,
            "existing_emis": existing_emis,
            "new_emi": round(new_emi, 2),
            "total_emi": round(total_emi, 2),
            "dti_ratio": round(dti, 2)
        }
    }
