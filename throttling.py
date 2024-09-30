import time

def exponential_backoff(attempts: int) -> int:
    """Calculates the backoff delay based on the number of attempts."""
    delay = 2 ** attempts  # Exponential backoff 
    return delay

def apply_throttling(api_key: str, attempts: int):
    """Applies throttling by delaying the response based on failed attempts."""
    delay = exponential_backoff(attempts)
    time.sleep(delay)  
    return delay
