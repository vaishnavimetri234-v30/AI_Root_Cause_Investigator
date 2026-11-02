
import pandas as pd
import joblib

# STEP 1: Load the trained ML model
model = joblib.load("models/failure_model.pkl")

print("======================================")
print(" AI POWERED ROOT CAUSE INVESTIGATOR")
print("======================================")

# STEP 2: Get machine sensor readings
machine_id = input("\nEnter Machine ID: ")

temperature = float(input("Enter Temperature: "))
vibration = float(input("Enter Vibration: "))
pressure = float(input("Enter Pressure: "))
runtime_hours = float(input("Enter Runtime Hours: "))

# STEP 3: Prepare input data
machine_data = pd.DataFrame([{
    "temperature": temperature,
    "vibration": vibration,
    "pressure": pressure,
    "runtime_hours": runtime_hours
}])

# STEP 4: Predict machine failure
prediction = model.predict(machine_data)[0]

print("\n======================================")
print(" MACHINE FAILURE PREDICTION")
print("======================================")

if prediction == 1:
    print("WARNING: Machine Failure Predicted!")
else:
    print("Machine Failure Not Predicted.")

# STEP 5: Investigate possible root causes
possible_causes = []
recommendations = []

if temperature >= 90:
    possible_causes.append("High operating temperature")
    recommendations.append("Inspect the cooling system.")

if vibration >= 0.80:
    possible_causes.append("Excessive machine vibration")
    recommendations.append("Inspect bearings and rotating components.")

if pressure >= 45:
    possible_causes.append("High operating pressure")
    recommendations.append("Inspect pressure control and valves.")

if runtime_hours >= 300:
    possible_causes.append("High accumulated runtime")
    recommendations.append("Review maintenance and servicing history.")

# STEP 6: Display investigation results
print("\n======================================")
print(" ROOT CAUSE INVESTIGATION")
print("======================================")

if possible_causes:
    for cause in possible_causes:
        print("Possible Cause:", cause)

    print("\nMAINTENANCE RECOMMENDATIONS")

    for recommendation in recommendations:
        print("-", recommendation)

else:
    print("No sensor conditions crossed the configured investigation thresholds.")

# STEP 7: Final report
print("\n======================================")
print(" INVESTIGATION REPORT")
print("======================================")

print("Machine ID:", machine_id)
print("Temperature:", temperature)
print("Vibration:", vibration)
print("Pressure:", pressure)
print("Runtime:", runtime_hours)

print("\nInvestigation Completed!")
