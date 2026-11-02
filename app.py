
import streamlit as st
import joblib

from langgraph_workflow import app as langgraph_app
from generate_report import generate_pdf


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="AI Root Cause Investigator",
    page_icon="🏭",
    layout="wide"
)


# --------------------------------
# DASHBOARD TITLE
# --------------------------------

st.title("🏭 AI-Powered Root Cause Investigator")

st.write(
    "An AI-based system to predict machine failures "
    "and investigate possible root causes using LangGraph."
)

st.divider()


# --------------------------------
# MACHINE SENSOR INPUTS
# --------------------------------

st.header("Enter Machine Details")

col1, col2 = st.columns(2)

with col1:

    machine_id = st.text_input(
        "Machine ID",
        value="M011"
    )

    temperature = st.number_input(
        "Temperature",
        min_value=0.0,
        value=100.0
    )

    vibration = st.number_input(
        "Vibration",
        min_value=0.0,
        value=0.95
    )


with col2:

    pressure = st.number_input(
        "Pressure",
        min_value=0.0,
        value=50.0
    )

    runtime_hours = st.number_input(
        "Runtime Hours",
        min_value=0.0,
        value=350.0
    )


# --------------------------------
# INVESTIGATION BUTTON
# --------------------------------

if st.button("🔍 Investigate Machine", type="primary"):

    if not machine_id.strip():

        st.error("Please enter a Machine ID.")

    else:

        try:

            with st.spinner("Investigating machine using LangGraph..."):

                # Step 1: Prepare initial workflow state

                initial_state = {
                    "machine_id": machine_id,
                    "temperature": temperature,
                    "vibration": vibration,
                    "pressure": pressure,
                    "runtime_hours": runtime_hours,
                    "prediction": "",
                    "possible_causes": [],
                    "recommendations": [],
                    "ai_report": ""
                }


                # Step 2: Execute LangGraph workflow

                result = langgraph_app.invoke(initial_state)


                # Step 3: Extract workflow results

                prediction_text = result["prediction"]

                causes = result["possible_causes"]

                recommendations = result["recommendations"]

                response = result["ai_report"]


                # Step 4: Convert prediction for dashboard display

                prediction = (
                    1 if prediction_text == "Failure Risk Detected" else 0
                )


                # Step 5: Generate PDF report

                pdf_path = generate_pdf(
                    machine_id,
                    temperature,
                    vibration,
                    pressure,
                    runtime_hours,
                    prediction_text,
                    causes,
                    recommendations,
                    response
                )


            # --------------------------------
            # DISPLAY RESULTS
            # --------------------------------

            st.success("Machine investigation completed!")

            st.subheader("Machine Prediction")

            if prediction == 1:

                st.error(prediction_text)

            else:

                st.success(prediction_text)


            st.subheader("Possible Root Causes")

            for cause in causes:

                st.write("🔸", cause)


            st.subheader("Maintenance Recommendations")

            for recommendation in recommendations:

                st.write("🔧", recommendation)


            st.subheader("AI Investigation Report")

            st.write(response)


            # --------------------------------
            # DOWNLOAD PDF
            # --------------------------------

            with open(pdf_path, "rb") as pdf_file:

                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_file.read(),
                    file_name=f"{machine_id}_investigation_report.pdf",
                    mime="application/pdf"
                )


            # --------------------------------
            # SAFETY INFORMATION
            # --------------------------------

            st.info(
                "This is a preliminary AI-assisted investigation. "
                "Predictions and possible causes require verification "
                "by a qualified maintenance engineer."
            )


        except Exception as e:

            st.error("An error occurred during machine investigation.")

            st.exception(e)
