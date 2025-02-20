# XML2JSON Pro

## Overview
XML2JSON Pro is a FastAPI-based project designed to process XML requests, apply business logic, and return structured JSON responses. The project includes XML parsing, pricing calculations, and dynamic response generation.

## Features
- XML request parsing
- Business logic processing
- Pricing calculations with markup and currency conversion
- FastAPI-based RESTful API
- Structured response using Pydantic models

## Project Structure
```
xml2json_pro/
│── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   ├── interfaces/
│   │   ├── xml_parser_interface.py
│   │   ├── pricing_interface.py
│   ├── models/
│   │   ├── response_model.py
│   │   ├── request_model.py
│   ├── services/
│   │   ├── xml_parser.py
│   │   ├── pricing.py
│   │   ├── business_logic.py
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── availability.py
│── main.py
│── README.md
│── requirements.txt
```

## Installation
### Prerequisites
- Python 3.6+
- FastAPI
- Uvicorn

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Premkumaryadav/xml2json_pro.git
   cd xml2json_pro
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running the Project
Start the FastAPI server with Uvicorn:
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
```
http://127.0.0.1:8000
```

## API Endpoints
### Process XML Request
**Endpoint:**
```
POST /process
```
**Request Body:** (XML data in request payload)
```xml
<data>
    <currency>USD</currency>
    <nationality>US</nationality>
</data>
```
**Response Example:**
```json
{
    "id": "12345678-RESPONSE",
    "hotelCodeSupplier": "12345678",
    "market": "US",
    "price": {
        "currency": "USD",
        "net": 100.0,
        "selling_price": 110.0,
        "selling_currency": "USD",
        "markup": 10.0,
        "exchange_rate": 1.0
    }
}
```

## Logging
Logs are managed in `app/core/logging.py`. The project logs essential processing steps, including XML parsing, pricing calculations, and API requests.

## Contribution
Feel free to submit issues and pull requests to improve the project.

