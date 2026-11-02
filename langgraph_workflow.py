
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# Step 1: Define the information shared between workflow nodes
class MachineState(TypedDict):
    machine_id: str
    temperature: float
    vibration: float
    pressure: float
    runtime_hours: float
    prediction: str
    possible_causes: list
    recommendations: list
    ai_report: str


# Step 2: Load the trained machine failure model
import joblib
import pandas as pd

model = joblib.load("models/failure_model.pkl")


# Step 3: Create the prediction node
def predict_failure(state: MachineState):

    # Get sensor readings from workflow state
    readings = pd.DataFrame([{
        "temperature": state["temperature"],
        "vibration": state["vibration"],
        "pressure": state["pressure"],
        "runtime_hours": state["runtime_hours"]
    }])

    # Predict machine failure
    prediction = model.predict(readings)[0]

    # Convert prediction into readable text
    if prediction == 1:
        result = "Failure Risk Detected"
    else:
        result = "No Failure Risk Detected"

    # Return updated workflow state
    return {
        "prediction": result
    }


# Step 4: Create the root cause identification node
def identify_causes(state: MachineState):

    causes = []
    recommendations = []

    # Check machine temperature
    if state["temperature"] >= 90:
        causes.append("High operating temperature")
        recommendations.append("Inspect the cooling system")

    # Check machine vibration
    if state["vibration"] >= 0.80:
        causes.append("Excessive machine vibration")
        recommendations.append("Inspect bearings and rotating components")

    # Check machine pressure
    if state["pressure"] >= 45:
        causes.append("High operating pressure")
        recommendations.append("Inspect pressure control systems")

    # Check machine runtime
    if state["runtime_hours"] >= 300:
        causes.append("High accumulated runtime")
        recommendations.append("Review maintenance history")

    # Return possible causes and recommendations
    return {
        "possible_causes": causes,
        "recommendations": recommendations
    }



# Step 5: Import the existing Groq AI chain
from ai_explainer import chain


# Step 6: Create the AI explanation node
def generate_ai_report(state: MachineState):

    # Send all required information to Groq
    ai_report = chain.invoke({

        "machine_id": str(state["machine_id"]),

        "temperature": str(state["temperature"]),

        "vibration": str(state["vibration"]),

        "pressure": str(state["pressure"]),

        "runtime_hours": str(state["runtime_hours"]),

        "prediction": str(state["prediction"]),

        "causes": ", ".join(state["possible_causes"]),

        "recommendations": ", ".join(state["recommendations"])
    })

    # Return the AI-generated report
    return {
        "ai_report": ai_report
    }


# Step 7: Create the LangGraph workflow
workflow = StateGraph(MachineState)


# Step 8: Add nodes to the workflow
workflow.add_node("predict_failure", predict_failure)

workflow.add_node("identify_causes", identify_causes)

workflow.add_node("generate_ai_report", generate_ai_report)


# Step 9: Connect the nodes in order
workflow.add_edge(START, "predict_failure")

workflow.add_edge("predict_failure", "identify_causes")

workflow.add_edge("identify_causes", "generate_ai_report")

workflow.add_edge("generate_ai_report", END)


# Step 10: Compile the workflow
app = workflow.compile()


print("LangGraph workflow created successfully!")


# Step 11: Provide machine sensor readings
if __name__ == "__main__":

    initial_state = {
        "machine_id": "M011",
        "temperature": 100.0,
        "vibration": 0.95,
        "pressure": 50.0,
        "runtime_hours": 350.0,
        "prediction": "",
        "possible_causes": [],
        "recommendations": [],
        "ai_report": ""
    }

    result = app.invoke(initial_state)

    print("\n===== MACHINE INVESTIGATION REPORT =====")
    print("\nMachine ID:", result["machine_id"])
    print("\nML Prediction:", result["prediction"])

    print("\nPossible Causes:")
    for cause in result["possible_causes"]:
        print("-", cause)

    print("\nRecommendations:")
    for recommendation in result["recommendations"]:
        print("-", recommendation)

    print("\nAI Generated Report:")
    print(result["ai_report"])