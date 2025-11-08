def evaluate_risk(salary, loan_amount, credit_score, tenure):
    """
    Simple rule-based Risk/Fraud Detection Agent.
    Returns dict with risk_level and reasons.
    """
    reasons = []
    risk_level = "Normal"

    if salary <= 0:
        return {"risk_level": "Invalid", "reasons": ["Salary not detected"]}

    # Loan-to-income ratio per year
    ratio = loan_amount / (salary * (tenure / 12))

    if ratio > 8:
        risk_level = "High Risk"
        reasons.append("Loan-to-income ratio exceeds safe range (8x annual income)")
    elif ratio > 5:
        risk_level = "Moderate Risk"
        reasons.append("Loan slightly above safe range (5–8x annual income)")

    if credit_score < 600:
        risk_level = "High Risk"
        reasons.append("Very low credit score (<600)")
    elif credit_score < 700 and risk_level != "High Risk":
        risk_level = "Moderate Risk"
        reasons.append("Fair credit score (<700)")

    if not reasons:
        reasons.append("All inputs within safe range")

    return {"risk_level": risk_level, "reasons": reasons}


# Quick test
if __name__ == "__main__":
    print(evaluate_risk(45000, 500000, 750, 12))
