import requests

def fetch_api(api_config):
    try:
        response = requests.get(api_config["url"], params=api_config["params"])
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}
