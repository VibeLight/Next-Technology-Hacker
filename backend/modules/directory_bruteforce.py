import requests

def brute_force_directories(url, wordlist):
    found = []
    for word in wordlist:
        test_url = f"{url}/{word}"
        response = requests.get(test_url)
        if response.status_code == 200:
            found.append(test_url)
    return found
