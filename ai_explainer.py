
from generate_report import generate_pdf
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# STEP 1: Load API key from .env
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("Groq API key not found. Check your .env file.")

# STEP 2: Connect to Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3,
    api_key=api_key
)

# STEP 3: Create an AI prompt
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an industrial machine maintenance assistant.

        Explain possible machine failure causes in simple English.

        Provide:
        1. Machine condition
        2. Possible root causes
        3. Explanation of sensor readings
        4. Recommended maintenance actions

        Do not claim that a possible cause is a confirmed root cause.
        Do not invent sensor readings or engineering limits.
        Mention when an engineer needs to inspect the machine."""
    ),
    (
        "human",
        """Machine ID: {machine_id}

        Temperature: {temperature}
        Vibration: {vibration}
        Pressure: {pressure}
        Runtime Hours: {runtime_hours}

        ML Prediction: {prediction}

        Possible Causes: {causes}

        Maintenance Suggestions: {recommendations}

        Generate a detailed investigation report."""
    )
])

# STEP 4: Create LangChain chain
chain = prompt | llm | StrOutputParser()

