# agents/existing_loans_agent.py

def evaluate_existing_loans(active_loans: int, total_outstanding: float, monthly_emi: float) -> dict:
    """
    Evaluates how existing loans impact repayment capacity.
    """
    if active_loans == 0:
        score = 95
        reason = "No active loans. Excellent repayment capacity."
    elif active_loans == 1 and total_outstanding < 300000:
        score = 80
        reason = "One small existing loan. Manageable risk."
    elif active_loans <= 3 and total_outstanding < 1000000:
        score = 60
        reason = f"{active_loans} active loans. Moderate liability."
    else:
        score = 30
        reason = f"{active_loans} active loans with ₹{total_outstanding} outstanding. High liability risk."

    # EMI burden check
    if monthly_emi > 0.4 * 50000:  # Assuming ₹50k average monthly income threshold
        score -= 10
        reason += " EMI burden exceeds 40% threshold."

    status = "PASS" if score >= 80 else "WARN" if score >= 60 else "FAIL"

    return {
        "agent": "Existing Loans Agent",
        "score": max(min(score, 100), 0),
        "status": status,
        "reason": reason
    }
