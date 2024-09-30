from redis_store import track_request

# Defining rate limits for different user tiers as provided in document
RATE_LIMITS = {
    "free": 50,     
    "premium": 200  
}

def is_rate_limited(api_key: str, user_tier: str) -> bool:
    """Checks if the API key has exceeded its rate limit."""
    window = 60  #1 minute
    limit = RATE_LIMITS[user_tier]  
    request_count = track_request(api_key, window)  
    
    
    return request_count > limit