
import joblib
import pandas as pd

from ai_explainer import chain

# Load the trained machine failure model
model = joblib.load("models/failure_model.pkl")

print("\n====================================")
print(" AI POWERED ROOT CAUSE INVESTIGATOR")
print("====================================")

# Get machine details
machine_id = input("Enter Machine ID: ")

temperature = float(input("Enter Temperature: "))
vibration = float(input("Enter Vibration: "))
pressure = float(input("Enter Pressure: "))
runtime_hours = float(input("Enter Runtime Hours: "))

# Prepare sensor readings for ML model
machine_data = pd.DataFrame([{
    "temperature": temperature,
    "vibration": vibration,
    "pressure": pressure,
    "runtime_hours": runtime_hours
}])

# Predict machine failure
prediction = model.predict(machine_data)[0]

if prediction == 1:
    prediction_text = "Potential machine failure detected"
else:
    prediction_text = "No failure predicted by the model"

# Identify possible causes using demo rules
causes = []
recommendations = []

if temperature >= 90:
    causes.append("High operating temperature")
    recommendations.append("Inspect the cooling system")

if vibration >= 0.80:
    causes.append("Excessive vibration")
    recommendations.append("Inspect bearings and rotating components")

if pressure >= 45:
    causes.append("High operating pressure")
    recommendations.append("Inspect pressure control systems")

if runtime_hours >= 300:
    causes.append("High accumulated runtime")
    recommendations.append("Review maintenance history")

if not causes:
    causes.append("No abnormal readings identified by the demo rules")
    recommendations.append("Continue routine monitoring and maintenance")

# Display ML prediction
print("\nML PREDICTION:", prediction_text)

print("\nPOSSIBLE CAUSES:")
for cause in causes:
    print("-", cause)

print("\nMAINTENANCE SUGGESTIONS:")
for recommendation in recommendations:
    print("-", recommendation)

# Generate AI investigation report
print("\nGenerating AI investigation report...")

response = chain.invoke({
    "machine_id": machine_id,
    "temperature": temperature,
    "vibration": vibration,
    "pressure": pressure,
    "runtime_hours": runtime_hours,
    "prediction": prediction_text,
    "causes": ", ".join(causes),
    "recommendations": ", ".join(recommendations)
})

print("\n====================================")
print(" AI GENERATED INVESTIGATION REPORT")
print("====================================")
print(response)

print("\nInvestigation Completed!")
