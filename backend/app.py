from flask import Flask, render_template, jsonify
import json
from modules.api_fetcher import fetch_api
from modules.rss_fetcher import fetch_rss
from modules.web_scraper import scrape_web

app = Flask(__name__, template_folder="templates", static_folder="static")

def load_settings():
    with open("settings.json", "r") as file:
        return json.load(file)

def collect_data():
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

    with open("collected_data.json", "w", encoding="utf-8") as file:
        json.dump(collected_data, file, ensure_ascii=False, indent=4)

    return collected_data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/collect", methods=["GET"])
def collect():
    data = collect_data()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
