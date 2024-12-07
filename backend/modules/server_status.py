import requests

def check_status(url):
    try:
        response = requests.get(url)
        return response.status_code
    except Exception as e:
        return str(e)
