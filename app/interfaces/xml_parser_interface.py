from abc import ABC, abstractmethod
from typing import Dict
from app.core.logging import logger

class XMLParserInterface(ABC):
    @abstractmethod
    def parse(self, xml_data: str) -> Dict:
        """Parse XML input and return structured data."""
        logger.info("Parsing XML data.")
        pass
