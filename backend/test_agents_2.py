# test_agents_2.py
from agents import employment_agent, existing_loans_agent, age_agent

def run_tests():
    print("👔 Testing Employment Agent...")
    print(employment_agent.evaluate_employment("salaried", 6))
    print(employment_agent.evaluate_employment("contract", 1))
    print()

    print("💳 Testing Existing Loans Agent...")
    print(existing_loans_agent.evaluate_existing_loans(1, 200000, 12000))
    print(existing_loans_agent.evaluate_existing_loans(4, 1200000, 30000))
    print()

    print("👶 Testing Age Agent...")
    print(age_agent.evaluate_age(28))
    print(age_agent.evaluate_age(58))

if __name__ == "__main__":
    run_tests()
