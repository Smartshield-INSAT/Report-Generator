import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from langchain_groq import ChatGroq
from agents import create_agents
from tasks import create_tasks
from crewai import Crew
import json
import uuid
from fpdf import FPDF, HTMLMixin
from datetime import datetime
import markdown2
import tempfile

# Load environment variables from .env file
load_dotenv()

def json_to_string(json_data):
    data = json.load(json_data)
    return json.dumps(data)

# Initialize Groq client
def get_groq_client():
    groq_api = os.getenv("GROQ_API_KEY")
    return Groq(api_key=groq_api)

def display_message(role, content):
    st.markdown(f"**{role}**: {content}")

class CustomPDF(FPDF, HTMLMixin):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Calculate width of title and position
        self.cell(0, 10, 'Cybersecurity Threat Analysis Report', 0, 1, 'C')
        # Line break
        self.ln(10)
        
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

def save_report_as_pdf(md_text, output_pdf_path):
    """
    Convert markdown text to a well-formatted PDF file
    
    Args:
        md_text (str): Markdown formatted text
        output_pdf_path (str): Path where to save the PDF file
    """
    # Convert markdown to HTML with extra features
    html = markdown2.markdown(md_text, extras=[
        "tables",
        "code-friendly",
        "fenced-code-blocks",
        "break-on-newline"
    ])
    
    # Initialize PDF
    pdf = CustomPDF()
    
    # Set up the PDF
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add title
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, "Cybersecurity Threat Analysis Report", 0, 1, 'C')
    pdf.ln(5)
    
    # Add timestamp
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'R')
    pdf.ln(5)
    
    # Set default font for content
    pdf.set_font('Arial', '', 11)
    
    # Write the content
    try:
        pdf.write_html(html)
    except Exception as e:
        # Fallback to basic text if HTML conversion fails
        pdf.multi_cell(0, 10, md_text)
    
    # Save the PDF
    try:
        pdf.output(output_pdf_path)
    except Exception as e:
        print(f"Error saving PDF: {str(e)}")
        # Create temp directory if output path is not accessible
        temp_dir = tempfile.gettempdir()
        temp_pdf_path = os.path.join(temp_dir, os.path.basename(output_pdf_path))
        pdf.output(temp_pdf_path)
        return temp_pdf_path
    
    return output_pdf_path

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
        save_report_as_pdf(result, pdf_file_path)
        
        st.download_button(
            label="Download Cybersecurity Report",
            data=open(pdf_file_path, "rb").read(),
            file_name=pdf_file_path,
            mime="application/pdf"
        )

if __name__ == "__main__":
    main()