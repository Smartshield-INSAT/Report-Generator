import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_groq import ChatGroq
from agents import create_agents
from tasks import create_tasks
from crewai import Crew
import pandas as pd
import json

# Load environment variables from .env file
load_dotenv()

def json_to_string(json_data):
    return json.dumps(json_data, indent=4)

def csv_to_json(csv_file):
    df = pd.read_csv(csv_file)
    return df.to_json(orient='records')

# Initialize Groq client
def get_groq_client():
    groq_api = os.getenv("GROQ_API_KEY")
    return Groq(api_key=groq_api)

def display_message(role, content):
    st.markdown(f"**{role}**: {content}")

def save_report_as_pdf(content, file_path):
    # Placeholder function - implement PDF generation logic here
    with open(file_path, "w") as f:
        f.write(content)

def main():
    client = get_groq_client()

    model = st.sidebar.selectbox(
        'Choose a model',
        ['gemma2-9b-it', 'llama-3.2-3b-preview', 'llama-3.1-70b-versatile']
    )

    llm = ChatGroq(
        temperature=0, 
        groq_api_key=os.getenv("GROQ_API_KEY"), 
        model_name=model
    )

    st.title('Cybersecurity Threat Analysis Assistant')
    st.markdown("""
    This assistant helps analyze detected cybersecurity threats by providing detailed analysis, forensic investigation, mitigation strategies, and generating comprehensive reports.
    """, unsafe_allow_html=True)

    st.subheader('Threat Analysis with Multiple Agents')
    detected_threat = st.text_input("Describe the detected threat:")
    uploaded_file = st.file_uploader("Upload CSV file containing threat data", type="csv")

    if detected_threat and uploaded_file:
        threat_data = csv_to_json(uploaded_file)
        st.json(threat_data)  
        threat_data = json_to_string(threat_data)

        print(threat_data)
        print(type(threat_data))

        agents = create_agents(llm)
        tasks = create_tasks(agents, detected_threat, threat_data)
        
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            verbose=2
        )

        placeholder = st.empty()  
        for task in crew.tasks:
            result = task.execute()
            placeholder.markdown("") 
            display_message(task.agent.role, result)

        # Save the enhanced report as a PDF
        #pdf_file_path = "cybersecurity_report.pdf"
        #save_report_as_pdf(result, pdf_file_path)
        
        #st.download_button(
        #    label="Download Cybersecurity Report",
        #    data=open(pdf_file_path, "rb").read(),
        #    file_name=pdf_file_path,
        #    mime="application/pdf"
        #)

if __name__ == "__main__":
    main()