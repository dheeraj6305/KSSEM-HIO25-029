import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# ✅ Change this path if your KSSEM-HIO25-029 folder is not on Desktop
csv_path = r"C:\Users\Monika B\Desktop\KSSEM-HIO25-029\data\loan_data.csv"
model_path = r"C:\Users\Monika B\Desktop\KSSEM-HIO25-029\data\model.pkl"

# Load dataset
print("Loading dataset from:", csv_path)
data = pd.read_csv(csv_path)

# Separate input features (X) and target (y)
X = data[['salary', 'credit_score', 'loan_amount', 'tenure']]
y = data['approved']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# Save model
with open(model_path, 'wb') as file:
    pickle.dump(model, file)

print("✅ Model trained and saved successfully at:", model_path)
