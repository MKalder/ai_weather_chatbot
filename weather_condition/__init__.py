__version__ = "1.0.0"
__date__ = "2025-02-15"
__author__ = "Marius Kalder"
__email__ = "aiweatherchatbot@mariuskalder.io"
__status__ = "Production"

import logging

from .weather import Weather
from .dialog_handler import DialogHandler
from .date_handler import DateHandler
from .precipitation import condition_emojis

logging.basicConfig(
    filename='weather_query.log',  # Name of the log file
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)

logger = logging.getLogger(__name__)
logger.info(f"Starting AI Weather Chatbot v{__version__} on {__date__}")