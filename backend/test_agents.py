# test_agents.py
from agents import cibil_agent, income_agent, dti_agent

def run_all_tests():
    print("🧠 Testing CIBIL Agent...")
    print(cibil_agent.evaluate_cibil(720))
    print(cibil_agent.evaluate_cibil(640))
    print()

    print("💰 Testing Income Agent...")
    print(income_agent.evaluate_income(60000, 18))
    print(income_agent.evaluate_income(25000, 6))
    print()

    print("💸 Testing DTI Agent...")
    print(dti_agent.evaluate_dti(monthly_income=60000, existing_emis=5000, loan_amount=500000, tenure_months=24))
    print(dti_agent.evaluate_dti(monthly_income=30000, existing_emis=15000, loan_amount=800000, tenure_months=36))
    print()

if __name__ == "__main__":
    run_all_tests()
