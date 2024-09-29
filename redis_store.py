
import redis

# Connecting to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def track_request(api_key: str, window: int) -> int:
    """Tracks API request count for the given API key and window."""
    key = f"api_usage:{api_key}"
    redis_client.incr(key)  
    redis_client.expire(key, window)  
    return int(redis_client.get(key))  

def get_request_count(api_key: str) -> int:
    """Returns the current request count for the API key."""
    key = f"api_usage:{api_key}"
    count = redis_client.get(key)
    return int(count) if count else 0
