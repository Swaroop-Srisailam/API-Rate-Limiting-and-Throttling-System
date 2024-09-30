#import dependencies
from flask import Flask, request, jsonify
from rate_limiter import is_rate_limited,RATE_LIMITS
from throttling import apply_throttling
from redis_store import get_request_count


app = Flask(__name__)

throttle_attempts = {}

@app.route('/api/resource', methods=['GET'])
def api_resource():
    api_key = request.headers.get('API-Key')
    user_tier = request.headers.get('User-Tier', 'free')  

    if is_rate_limited(api_key, user_tier):
    
        if api_key not in throttle_attempts:
            throttle_attempts[api_key] = 0
        throttle_attempts[api_key] += 1

        # Applying the throttling based on the number of failed attempts 
        delay = apply_throttling(api_key, throttle_attempts[api_key])

        return jsonify({
            "error": "Too Many Requests",
            "message": "Rate limit exceeded, try again later.",
            "retry_after": delay
        }), 429
    else:
        # Reseting the throttling attempts after a successful request
        throttle_attempts[api_key] = 0
        return jsonify({"message": "Request successful!"}), 200

@app.route('/dashboard', methods=['GET'])
def dashboard():
    """Dashboard for visualizing rate-limit violations and request patterns."""
    exceeded_users = []  # List users who exceeded rate limits
    for api_key in throttle_attempts:
        request_count = get_request_count(api_key)
        if request_count > RATE_LIMITS['free']:
            exceeded_users.append({
                "api_key": api_key,
                "requests": request_count
            })

    return jsonify({
        "exceeded_users": exceeded_users,
        "total_exceeded": len(exceeded_users)
    })
    
    
if __name__ == "__main__":
    app.run(debug=True)