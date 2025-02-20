from pydantic import BaseModel
from typing import Optional

class Price(BaseModel):
    minimumSellingPrice: Optional[float]
    currency: str
    net: float
    selling_price: float
    selling_currency: str
    markup: float
    exchange_rate: float

class HotelResponse(BaseModel):
    id: str
    hotelCodeSupplier: str
    market: str
    price: Price
