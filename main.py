from fastapi import FastAPI
from app.api.endpoints import xml_endpoint
from app.core.logging import logger  # Use the common logger

# Create FastAPI app
app = FastAPI(
    title="XML to JSON API",
    description="An API to convert XML data to JSON format",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.on_event("startup")
async def startup_event():
    """Executes when the FastAPI application starts."""
    logger.info("XML to JSON API has started successfully.")


@app.on_event("shutdown")
async def shutdown_event():
    """Executes when the FastAPI application shuts down."""
    logger.info("XML to JSON API is shutting down.")


@app.get("/", tags=["Health Check"])
async def home():
    """
    Health check endpoint.

    Returns:
        dict: A welcome message.
    """
    logger.info("Home endpoint accessed.")
    return {"message": "Welcome to the XML to JSON API"}


# Include router
app.include_router(xml_endpoint.router, prefix="/api")
