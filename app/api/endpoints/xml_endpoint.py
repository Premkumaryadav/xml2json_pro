from fastapi import APIRouter, HTTPException, Depends, Body
from app.services.xml_parser import XMLParser
from app.services.pricing import PricingService
from app.services.business_logic import BusinessLogic
from app.models.response_model import HotelResponse
from app.core.logging import logger  # Import logger

router = APIRouter()

# Dependency injection
def get_business_logic():
    xml_parser = XMLParser()
    pricing_service = PricingService()
    return BusinessLogic(xml_parser, pricing_service)

@router.post("/process", response_model=HotelResponse, summary="Process XML Availability Request")
async def process_availability_request(
    xml_data: str = Body(..., media_type="application/xml"),
    business_logic: BusinessLogic = Depends(get_business_logic)
):
    """
    **Processes the XML availability request and returns a structured response.**
    
    - Parses XML request
    - Validates input data
    - Applies business logic
    - Calculates dynamic pricing
    - Returns structured JSON response
    """
    logger.info("Received XML availability request.")
    try:
        response = business_logic.process_xml_request(xml_data)
        logger.info("Successfully processed XML request.")
        return response
    except HTTPException as e:
        logger.error(f"HTTP Exception: {e.detail}")
        raise e  # Preserve FastAPI HTTPException details
    except Exception as e:
        logger.exception("Unexpected error occurred while processing XML request.")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
