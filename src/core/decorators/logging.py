import logging
import time
import functools

logger = logging.getLogger(__name__)

def log_execution(func):
    """Decorator to log execution of service methods."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        logger.info(f"Starting execution of {func.__name__}")
        try:
            result = func(*args, **kwargs)
            elapsed = time.time() - start
            logger.info(f"{func.__name__} executed successfully in {elapsed:.2f}s")
            return result
        except Exception as e:
            elapsed = time.time() - start
            logger.error(f"Error in {func.__name__} after {elapsed:.2f}s: {e}")
            raise
    return wrapper