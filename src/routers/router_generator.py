from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from src.logger.logger import get_logger
from src.config.settings import get_settings
from src.schemas.schema_generator import GenerateReportRequest
from src.services.service_generator import agenerate_report
import os
import io

settings = get_settings()
logger = get_logger(__file__)

router = APIRouter(prefix="/generator")

@router.post(path="/generate-report")
async def generate_report(generate_report_request: GenerateReportRequest):
    """Generates a PDF report based on the provided threat and threat data, and returns it as a streaming response.
    
    Args:
        generate_report_request (GenerateReportRequest): An object containing the threat and threat data required for report generation.
    
    Returns:
        StreamingResponse: A streaming response containing the generated PDF report.
    
    Raises:
        HTTPException: If report generation fails (500), if the report file is not found (404), or if any other error occurs during the process (500).
    """
    try:
        threat = generate_report_request.threat
        threat_data = generate_report_request.threat_data

        report_pdf_file_path = await agenerate_report(threat, threat_data)
        if report_pdf_file_path is None:
            logger.error("Report generation failed, no path returned.")
            raise HTTPException(status_code=500, detail="Failed to generate report")
        if not os.path.exists(report_pdf_file_path):
            logger.error(f"Report PDF file not found at path: {report_pdf_file_path}")
            raise HTTPException(status_code=404, detail="Report not found")

        with open(report_pdf_file_path, "rb") as report_file:
            pdf_content = io.BytesIO(report_file.read())

        # Return the PDF content as a StreamingResponse
        pdf_content.seek(0)
        return StreamingResponse(
            pdf_content,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=report.pdf"}
        )
    
    except Exception as e:
        logger.error(f"Critical Error occurred in router_generator.generate_report: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the report")
