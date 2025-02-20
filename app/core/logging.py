import logging

# Configure global logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
)

logger = logging.getLogger(__name__)
