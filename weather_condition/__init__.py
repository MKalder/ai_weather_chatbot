__version__ = "0.0.1"
__date__ = "2025-02-15"
__author__ = "Marius Kalder"
__email__ = "aiweatherchatbot@mariuskalder.io"
__status__ = "Production"

from .weather import Weather
import logging

logging.basicConfig(
    filename='weather_query.log',  # Name of the log file
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)

logger = logging.getLogger(__name__)
logger.info(f"Starting AI Weather Chatbot v{__version__} on {__date__}")