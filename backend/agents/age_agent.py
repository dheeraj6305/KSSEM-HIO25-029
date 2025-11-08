# agents/age_agent.py

def evaluate_age(age: int) -> dict:
    """
    Evaluates risk based on applicant's age and tenure potential.
    """
    if 25 <= age <= 40:
        score = 90
        reason = "Ideal age range for long-tenure repayment."
    elif 41 <= age <= 55:
        score = 75
        reason = "Mid-career stage. Moderate risk due to shorter tenure left."
    elif 18 <= age < 25:
        score = 60
        reason = "Young applicant. Limited credit history but long repayment runway."
    elif 56 <= age <= 65:
        score = 45
        reason = "Near retirement age. Limited repayment window."
    else:
        score = 25
        reason = "High risk due to age beyond typical lending bracket."

    status = "PASS" if score >= 80 else "WARN" if score >= 60 else "FAIL"

    return {
        "agent": "Age Agent",
        "score": score,
        "status": status,
        "reason": reason
    }
