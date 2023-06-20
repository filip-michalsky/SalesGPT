import logging
import time
from functools import wraps

logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()
log_filename = "output.log"
file_handler = logging.FileHandler(filename=log_filename)
handlers = [stream_handler, file_handler]


class TimeFilter(logging.Filter):
    def filter(self, record):
        return "Running" in record.getMessage()


logger.addFilter(TimeFilter())

# Configure the logging module
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s %(asctime)s - %(levelname)s - %(message)s",
    handlers=handlers,
)


def time_logger(func):
    """Decorator function to log time taken by any function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start time before function execution
        result = func(*args, **kwargs)  # Function execution
        end_time = time.time()  # End time after function execution
        execution_time = end_time - start_time  # Calculate execution time
        logger.info(f"Running {func.__name__}: --- {execution_time} seconds ---")
        return result

    return wrapper
