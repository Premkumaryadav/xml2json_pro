from app.core.logging import logger
from app.interfaces.pricing_interface import PricingInterface

class PricingService(PricingInterface):
    """Handles pricing calculations, including markup and currency conversion."""

    def calculate_price(self, net_price: float, markup: float) -> float:
        """
        Applies a markup percentage to the net price.

        Args:
            net_price (float): The base price.
            markup (float): The percentage markup.

        Returns:
            float: The final selling price after applying markup.
        """
        selling_price = round(net_price * (1 + markup / 100), 2)
        logger.info(f"Calculated selling price: {selling_price} (Net: {net_price}, Markup: {markup}%)")
        return selling_price

    def convert_currency(self, amount: float, exchange_rate: float) -> float:
        """
        Converts an amount using an exchange rate.

        Args:
            amount (float): The original amount.
            exchange_rate (float): The exchange rate.

        Returns:
            float: The converted amount.
        """
        converted_amount = round(amount * exchange_rate, 2)
        logger.info(f"Converted {amount} at rate {exchange_rate} → {converted_amount}")
        return converted_amount
