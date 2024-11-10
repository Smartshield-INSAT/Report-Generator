from pydantic import BaseModel , Field
from src.logger.logger import get_logger
from fastapi import UploadFile
from typing import Dict , Any 



class GenerateReportRequest(BaseModel) : 
    threat : str = Field(default = "Safe" )
    threat_data : Dict[str , Any] 
    
