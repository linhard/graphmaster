import requests

API_BASE_URL = "http://95.217.205.47:8002/vectorize"  # Adjust API URL if needed


def vectorize_token(token):
    """Send the token to the vectorization API and return the resulting vector."""
    try:
        response = requests.post(
            API_BASE_URL,
            json={"text": token},
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        vector = response.json().get("vector", [])
        return vector
    except requests.RequestException as e:
        print(f"Error during vectorization: {e}")
        return []
