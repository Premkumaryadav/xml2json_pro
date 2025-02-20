import random
import app.core.config as config  # Import central config
from app.core.logging import logger  # Import common logger
from app.models.response_model import HotelResponse, Price
from app.interfaces.xml_parser_interface import XMLParserInterface
from app.interfaces.pricing_interface import PricingInterface


class BusinessLogic:
    def __init__(self, xml_parser: XMLParserInterface, pricing_service: PricingInterface):
        self.xml_parser = xml_parser
        self.pricing_service = pricing_service
        logger.info("BusinessLogic initialized with XMLParser and PricingService.")

    def generate_random_code(self) -> str:
        hotel_code = str(random.randint(10000000, 99999999))
        logger.debug(f"Generated random hotel code: {hotel_code}")
        return hotel_code

    def get_dynamic_values(self, currency: str, nationality: str):
        """Fetch exchange rate, markup, and net price with fallback defaults."""
        exchange_rate = config.EXCHANGE_RATES.get(currency, config.DEFAULT_EXCHANGE_RATE)
        markup = config.MARKUP_RATES.get(nationality, config.DEFAULT_MARKUP)
        net_price = config.DEFAULT_NET_PRICE
        
        logger.info(
            f"Fetching dynamic values -> Currency: {currency}, Nationality: {nationality}, "
            f"Exchange Rate: {exchange_rate}, Markup: {markup}, Net Price: {net_price}"
        )
        return exchange_rate, markup, net_price

    def process_xml_request(self, xml_data: str) -> HotelResponse:
        """Processes XML and returns structured JSON response with fallback defaults."""
        logger.info("Processing XML request.")
        
        # Parse XML data
        data = self.xml_parser.parse(xml_data)
        logger.debug(f"Parsed XML data: {data}")

        hotel_code = self.generate_random_code()
        response_id = f"{hotel_code}-RESPONSE"

        # Fetch dynamic values with fallback
        exchange_rate, markup, net_price = self.get_dynamic_values(
            data.get("currency", config.DEFAULT_CURRENCY), 
            data.get("nationality", config.DEFAULT_NATIONALITY)
        )

        # Calculate selling price and convert currency
        selling_price = self.pricing_service.calculate_price(net_price, markup)
        converted_price = self.pricing_service.convert_currency(selling_price, exchange_rate)
        
        logger.info(
            f"Hotel {hotel_code} | Net Price: {net_price}, Selling Price: {selling_price}, "
            f"Converted Price: {converted_price}, Exchange Rate: {exchange_rate}"
        )
        
        response = HotelResponse(
            id=response_id,
            hotelCodeSupplier=hotel_code,
            market=data.get("market", config.DEFAULT_MARKET),
            price=Price(
                minimumSellingPrice=None,
                currency=data.get("currency", config.DEFAULT_CURRENCY),
                net=net_price,
                selling_price=converted_price,
                selling_currency=data.get("currency", config.DEFAULT_CURRENCY),
                markup=markup,
                exchange_rate=exchange_rate,
            ),
        )
        
        logger.info(f"Generated hotel response: {response}")
        return response
