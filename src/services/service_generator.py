from langchain_groq import ChatGroq
from crewai import Crew
import uuid
import os
from fastapi.responses import FileResponse
from typing import Dict 
from src.config.settings import get_settings
from src.logger.logger import get_logger
from src.services.service_crewai.agents import create_agents
from src.services.service_crewai.tasks import create_tasks
from src.services.service_crewai.utils import * 

settings = get_settings()
logger = get_logger(__file__)


async def agenerate_report(threat : str , threat_data : Dict ) : 
    try : 
        client = get_groq_client()
        llm = ChatGroq(
            temperature=0, 
            groq_api_key=settings.GROQ_API_KEY, 
            model_name=settings.MODEL
        )
        agents = create_agents(llm)
        tasks = create_tasks(agents, threat, threat_data)
        crew = Crew(
                agents=list(agents.values()),
                tasks=tasks,
                verbose=2
        )
        for task in crew.tasks:
            result = task.execute()

        path_prefix = r"C:\\Users\\"
        pdf_file_name = r"cybersecurity_report" + str(uuid.uuid4()) + ".pdf" 
        pdf_file_path = path_prefix + pdf_file_name
        print("PDF file path :", pdf_file_path)
        html_report = generate_html_report(result, client)
        print(html_report)
        html_to_pdf(html_report, pdf_file_path)
        print("HTML to PDF conversion done")

        return pdf_file_path


    except Exception as e :
        logger.error(f"Error occured in service_report_generator.generate_report : {e}")


