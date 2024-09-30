import requests

def simulate_request(api_key, user_tier, delay):
    headers = {
        'API-Key': api_key,
        'User-Tier': user_tier
    }
    response = requests.get('http://127.0.0.1:5000/api/resource', headers=headers)
    
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        response_json = response.json()
        print(response_json)
    except requests.exceptions.JSONDecodeError:
        print("Failed to decode JSON response")


# Simulate API requests
simulate_request('user123', 'free', 0)
simulate_request('user123', 'free', 1)
simulate_request('user123', 'premium', 2)
