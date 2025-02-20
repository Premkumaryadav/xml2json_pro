import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.core.logging import logger  # Import global logger
from app.interfaces.xml_parser_interface import XMLParserInterface
from app.core.config import (
    VALID_LANGUAGES, DEFAULT_LANGUAGE,
    VALID_CURRENCIES, DEFAULT_CURRENCY,
    VALID_NATIONALITIES, DEFAULT_NATIONALITY
)

var = "__define_ocg__"

class XMLParser(XMLParserInterface):
    """Parses XML requests and extracts required data."""

    def parse(self, xml_data: str):
        """
        Parses XML data and extracts required parameters.

        Args:
            xml_data (str): The XML request as a string.

        Returns:
            dict: Extracted data with validated fields.

        Raises:
            HTTPException: If XML is malformed or required fields are missing.
        """
        try:
            root = ET.fromstring(xml_data)
            logger.info("XML data successfully parsed.")

            # Extract values with logging
            language_code = root.find(".//languageCode").text or DEFAULT_LANGUAGE
            logger.info(f"Language Code: {language_code}")

            options_quota = int(root.find(".//optionsQuota").text or 20)
            logger.info(f"Options Quota: {options_quota}")

            search_type = root.find(".//SearchType").text
            start_date = root.find(".//StartDate").text
            end_date = root.find(".//EndDate").text
            currency = root.find(".//Currency").text or DEFAULT_CURRENCY
            nationality = root.find(".//Nationality").text or DEFAULT_NATIONALITY

            # Validate Configuration Parameters
            params = root.find(".//Parameter")
            if params is None:
                logger.error("Missing Configuration->Parameters in XML.")
                raise HTTPException(status_code=400, detail="Missing Configuration->Parameters")

            password = params.get("password")
            username = params.get("username")
            company_id = params.get("CompanyID")

            if not all([password, username, company_id]):
                logger.error("Missing required authentication parameters.")
                raise HTTPException(status_code=400, detail="Missing required parameters (password, username, CompanyID)")

            # Validate Dates
            start_date_dt = datetime.strptime(start_date, "%d/%m/%Y")
            end_date_dt = datetime.strptime(end_date, "%d/%m/%Y")
            today = datetime.today()

            if start_date_dt < today + timedelta(days=2):
                logger.error("StartDate must be at least 2 days after today.")
                raise HTTPException(status_code=400, detail="StartDate must be at least 2 days after today.")
            if (end_date_dt - start_date_dt).days < 3:
                logger.error("Stay duration must be at least 3 nights.")
                raise HTTPException(status_code=400, detail="Stay duration must be at least 3 nights.")

            extracted_data = {
                "language_code": language_code if language_code in VALID_LANGUAGES else DEFAULT_LANGUAGE,
                "options_quota": options_quota,
                "search_type": search_type,
                "start_date": start_date_dt,
                "end_date": end_date_dt,
                "currency": currency if currency in VALID_CURRENCIES else DEFAULT_CURRENCY,
                "nationality": nationality if nationality in VALID_NATIONALITIES else DEFAULT_NATIONALITY,
                "password": password,
                "username": username,
                "company_id": int(company_id),
            }

            logger.info("Successfully extracted XML data.")
            return extracted_data

        except Exception as e:
            logger.exception("Error while parsing XML data.")
            raise HTTPException(status_code=400, detail=str(e))
