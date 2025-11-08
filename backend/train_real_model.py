import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle, os

# Paths
DATA_PATH = "sample_data/real_data/train.csv"
OUT_DIR = "sample_data/real_data"

# Load dataset
df = pd.read_csv(DATA_PATH)
print(f"Loaded dataset with {len(df)} rows and {len(df.columns)} columns")

# Drop any non-numeric columns (like Loan_ID)
df = df.select_dtypes(include=["number"])
print(f"Using {len(df.columns)} numeric columns for training: {list(df.columns)}")

# Identify target column (last one) and features
target = df.columns[-1]
X = df.iloc[:, :-1]
y = df[target]

# Handle missing values
X = X.fillna(X.mean())
y = y.fillna(0)

# Split and train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save trained model and cleaned data
os.makedirs(OUT_DIR, exist_ok=True)

with open(os.path.join(OUT_DIR, "model.pkl"), "wb") as f:
    pickle.dump(model, f)

df.to_csv(os.path.join(OUT_DIR, "loan_real_cleaned.csv"), index=False)

with open(os.path.join(OUT_DIR, "model_info.txt"), "w") as f:
    f.write(f"RandomForest trained on {len(df)} records with {len(X.columns)} numeric features.")

print("✅ Model trained and saved successfully.")
