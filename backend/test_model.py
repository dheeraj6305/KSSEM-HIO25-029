import pickle

# path to your model file
model_path = r"C:\Users\Monika B\Desktop\KSSEM-HIO25-029\data\model.pkl"

# load the model
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# sample input: salary, credit_score, loan_amount, tenure
X_test = [[45000, 720, 200000, 12]]

# make prediction
pred = model.predict(X_test)[0]
print("Prediction (1 = approved, 0 = rejected):", pred)

# if model supports probability, print that too
try:
    prob = model.predict_proba(X_test)[0]
    print("Confidence:", prob)
except:
    pass
