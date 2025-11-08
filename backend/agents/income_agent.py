# agents/income_agent.py
def evaluate_income(monthly_income: float, job_stability_months: int = 12) -> dict:
    """
    Evaluates income sufficiency and stability.
    """

    if monthly_income >= 100000:
        score = 95
        status = "PASS"
        reason = f"High stable income ₹{monthly_income}/month."
    elif 50000 <= monthly_income < 100000:
        score = 85
        status = "PASS"
        reason = f"Decent income ₹{monthly_income}/month."
    elif 30000 <= monthly_income < 50000:
        score = 60
        status = "WARN"
        reason = f"Moderate income ₹{monthly_income}/month, limited repayment capacity."
    else:
        score = 30
        status = "FAIL"
        reason = f"Low income ₹{monthly_income}/month. High risk of default."

    # Bonus for job stability
    if job_stability_months >= 24:
        score += 5
        reason += " Long-term employment stability detected."

    return {
        "agent": "Income Agent",
        "score": min(score, 100),
        "status": status,
        "reason": reason
    }
