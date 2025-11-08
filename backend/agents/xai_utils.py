def generate_explanation(salary, credit_score, loan_amount, tenure, approved):
    """
    Generates a simple human-readable explanation for loan decision.
    """
    ratio = loan_amount / (salary * (tenure / 12))
    explanations = []

    if approved:
        explanations.append("✅ Loan approved because:")
        if salary > 30000:
            explanations.append(f"• Stable salary of ₹{salary:,}")
        if credit_score >= 700:
            explanations.append(f"• Good credit score ({credit_score})")
        if ratio <= 5:
            explanations.append("• Loan-to-income ratio within safe range")
        else:
            explanations.append("• Ratio slightly high, but acceptable")
    else:
        explanations.append("❌ Loan rejected because:")
        if credit_score < 650:
            explanations.append(f"• Credit score too low ({credit_score})")
        if ratio > 6:
            explanations.append(f"• Loan-to-income ratio too high ({ratio:.2f}x)")
        if salary < 20000:
            explanations.append("• Salary below minimum eligibility limit")

    return {
        "explanation": "\n".join(explanations),
        "factors": {
            "salary": salary,
            "credit_score": credit_score,
            "loan_amount": loan_amount,
            "tenure": tenure,
            "ratio": round(ratio, 2),
        },
    }


# Quick test
if __name__ == "__main__":
    print(generate_explanation(45000, 750, 500000, 12, approved=True))
