import pickle

# Path to your new model
model_path = r"C:\Users\Monika B\Desktop\KSSEM-HIO25-029\backend\sample_data\real_data\model.pkl"

# Load the model
model = pickle.load(open(model_path, "rb"))

# Test with a realistic input [salary, credit_score, loan_amount, tenure]
X_test = [[45000, 750, 200000, 12]]
prediction = model.predict(X_test)[0]

print("Prediction (1 = approved, 0 = rejected):", prediction)
