# agents/employment_agent.py

def evaluate_employment(employment_type: str, years_experience: int) -> dict:
    """
    Evaluates applicant’s employment stability and risk.
    employment_type: 'salaried' or 'self-employed' or 'contract'
    """
    emp_type = employment_type.lower().strip()

    if emp_type == "salaried":
        base_score = 90
        reason = "Salaried employment offers stable income."
    elif emp_type == "self-employed":
        base_score = 70
        reason = "Self-employed applicant. Income stability depends on business continuity."
    elif emp_type == "contract":
        base_score = 50
        reason = "Contract-based employment detected. Limited job security."
    else:
        base_score = 40
        reason = f"Unknown employment type: {employment_type}"

    # Experience adds confidence
    if years_experience >= 5:
        base_score += 10
        reason += " +5 years experience adds reliability."
    elif years_experience < 1:
        base_score -= 10
        reason += " Less than 1 year experience increases risk."

    status = "PASS" if base_score >= 80 else "WARN" if base_score >= 60 else "FAIL"

    return {
        "agent": "Employment Agent",
        "score": min(max(base_score, 0), 100),
        "status": status,
        "reason": reason
    }
