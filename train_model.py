
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import joblib
from pathlib import Path

# STEP 1: Load cleaned dataset
df = pd.read_csv("data/cleaned_machine_data.csv")

print("Dataset Loaded Successfully")
print(df.head())

# STEP 2: Select input features
X = df[["temperature", "vibration", "pressure", "runtime_hours"]]

# STEP 3: Select target column
y = df["failure"]

# STEP 4: Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
    stratify=y
)

print("\nTraining Records:", len(X_train))
print("Testing Records:", len(X_test))

# STEP 5: Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# STEP 6: Train the model
model.fit(X_train, y_train)

print("\nModel Training Completed!")

# STEP 7: Make predictions
y_pred = model.predict(X_test)

# STEP 8: Evaluate the model
accuracy = accuracy_score(y_test, y_pred)

print("\nMODEL ACCURACY:")
print(accuracy)

print("\nCLASSIFICATION REPORT:")
print(classification_report(y_test, y_pred, zero_division=0))

print("\nCONFUSION MATRIX:")
print(confusion_matrix(y_test, y_pred))

# STEP 9: Display feature importance
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

print("\nFEATURE IMPORTANCE:")
print(importance.sort_values(by="Importance", ascending=False))

# STEP 10: Save trained model
Path("models").mkdir(exist_ok=True)

joblib.dump(model, "models/failure_model.pkl")

print("\nTrained model saved successfully!")
