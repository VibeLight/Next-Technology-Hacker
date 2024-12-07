from flask import Flask, jsonify, render_template
import json
from modules.api_fetcher import fetch_api
from modules.rss_fetcher import fetch_rss
from modules.web_scraper import scrape_web
from modules.port_scanner import scan_ports
from modules.dns_lookup import dns_lookup
from modules.whois_lookup import get_whois
from modules.password_generator import generate_password

app = Flask(__name__, template_folder="templates", static_folder="static")

def load_settings():
    """
    Load API, RSS, and Web scraping configurations from settings.json.
    """
    with open("settings.json", "r") as file:
        return json.load(file)

def collect_data():
    """
    Collect data from APIs, RSS feeds, and web scraping configurations.
    """
    settings = load_settings()
    collected_data = {"api": [], "rss": [], "web": []}

    for api_config in settings["api_sources"]:
        result = fetch_api(api_config)
        if result:
            collected_data["api"].append(result)

    for rss_url in settings["rss_feeds"]:
        result = fetch_rss(rss_url)
        if result:
            collected_data["rss"].extend(result)

    for web_config in settings["web_scraping"]:
        result = scrape_web(web_config)
        if result:
            collected_data["web"].extend(result)

    # Save collected data to a file
    with open("collected_data.json", "w", encoding="utf-8") as file:
        json.dump(collected_data, file, ensure_ascii=False, indent=4)

    return collected_data

@app.route("/")
def index():
    """
    Render the main HTML page.
    """
    return render_template("index.html")

@app.route("/run_tool/<tool>")
def run_tool(tool):
    """
    Handle requests for specific tools.
    """
    if tool == "collect_data":
        result = collect_data()
    elif tool == "port_scan":
        result = scan_ports("127.0.0.1", range(1, 1025))
    elif tool == "dns_lookup":
        result = dns_lookup("example.com")
    elif tool == "whois_lookup":
        result = str(get_whois("example.com"))
    elif tool == "password_generator":
        result = generate_password()
    else:
        result = {"error": "Unknown tool"}

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
