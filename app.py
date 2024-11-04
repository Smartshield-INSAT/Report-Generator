from utils import *
from langchain_groq import ChatGroq
from agents import create_agents
from dotenv import load_dotenv
from tasks import create_tasks
from crewai import Crew
import streamlit as st
import uuid
import os

# Load environment variables from .env file
load_dotenv()

def main():
    client = get_groq_client()

    model = st.sidebar.selectbox(
        'Choose a model',
        ['mixtral-8x7b-32768', 'llama3-70b-8192', 'gemma2-9b-it']
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
    uploaded_file = st.file_uploader("Upload JSON file containing threat data", type="json")

    if detected_threat and uploaded_file:
        threat_data = json_to_string(uploaded_file)

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
        pdf_file_path = "cybersecurity_report" + str(uuid.uuid4()) + ".pdf" 
        #save_report_as_pdf(result, pdf_file_path)
        html_report = generate_html_report(result, client)
        print(html_report)
        html_to_pdf(html_report, pdf_file_path)
        
        st.download_button(
            label="Download Cybersecurity Report",
            data=open(pdf_file_path, "rb").read(),
            file_name=pdf_file_path,
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()