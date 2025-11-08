# agents/cibil_agent.py
def evaluate_cibil(cibil_score: int) -> dict:
    """
    Evaluates the applicant's credit score and returns a risk rating.
    """

    if cibil_score >= 750:
        return {
            "agent": "CIBIL Agent",
            "score": 95,
            "status": "PASS",
            "reason": f"Excellent CIBIL score ({cibil_score}). Low credit risk."
        }
    elif 700 <= cibil_score < 750:
        return {
            "agent": "CIBIL Agent",
            "score": 80,
            "status": "WARN",
            "reason": f"Good CIBIL score ({cibil_score}). Slight caution advised."
        }
    elif 650 <= cibil_score < 700:
        return {
            "agent": "CIBIL Agent",
            "score": 55,
            "status": "WARN",
            "reason": f"Moderate CIBIL score ({cibil_score}). Needs close review."
        }
    else:
        return {
            "agent": "CIBIL Agent",
            "score": 20,
            "status": "FAIL",
            "reason": f"Poor CIBIL score ({cibil_score}). High default probability."
        }
