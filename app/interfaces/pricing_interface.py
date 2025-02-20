from abc import ABC, abstractmethod
from app.core.logging import logger

class PricingInterface(ABC):
    @abstractmethod
    def calculate_price(self, net_price: float, markup: float) -> float:
        """Calculates selling price from net price and markup."""
        logger.info(f"Calculating price: Net Price = {net_price}, Markup = {markup}")
        pass
