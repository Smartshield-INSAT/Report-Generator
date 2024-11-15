import streamlit as st
import markdown2
import tempfile
import pdfkit
import json
import os
from fpdf import FPDF, HTMLMixin
from datetime import datetime
from groq import Groq
import os 
def html_to_pdf(html_text, output_pdf_path):
    options = {
        'page-size': 'A3',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': 'UTF-8',
        'no-outline': None,
        'enable-local-file-access': None,
        'dpi': 300,
        'zoom': 1.0,
        'enable-smart-shrinking': True,
        'print-media-type': True
    }
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(html_text, output_pdf_path,options=options, configuration=config)

def generate_html_report(data, client):
    chat_completion = client.chat.completions.create(
        messages = [
            {
                "role": "user",
                "content": (
                    data + "\n Convert this report into a professional, visually appealing HTML page designed for a cybersecurity threat detection report. Maintain the exact content without any alterations. Use CSS to create a modern and polished design, prioritizing readability, organized layout, and aesthetic appeal. Implement distinct sections, headers, and subheaders, and use color schemes appropriate for cybersecurity contexts (such as dark and red). Include icons or styling for important elements to highlight key information. Return only the HTML content without additional text or explanations."
                ),
            }
        ],
        model="mixtral-8x7b-32768",
    )
    return chat_completion.choices[0].message.content

def json_to_string(json_data):
    data = json.load(json_data)
    return json.dumps(data)

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