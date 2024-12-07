from flask import Flask, jsonify, render_template, request
import requests
import socket
import whois
import hashlib
import os
import time
import json
from scapy.all import sniff
from threading import Thread
import random
import string

app = Flask(__name__)

# === 情報収集用の設定ファイルのパス ===
CONFIG_FILE = "config.json"

# === 初期化関数 ===
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {"apis": [], "rss_feeds": [], "websites": []}

def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

config = load_config()

# === 情報収集ツール ===
def collect_data():
    data = {"api_results": {}, "rss_results": {}, "website_results": {}}

    # APIデータ収集
    for api_url in config["apis"]:
        try:
            response = requests.get(api_url)
            data["api_results"][api_url] = response.json()
        except Exception as e:
            data["api_results"][api_url] = str(e)

    # RSSフィード収集
    for rss_url in config["rss_feeds"]:
        try:
            response = requests.get(rss_url)
            data["rss_results"][rss_url] = response.text
        except Exception as e:
            data["rss_results"][rss_url] = str(e)

    # Webスクレイピング
    for website in config["websites"]:
        try:
            response = requests.get(website)
            data["website_results"][website] = response.text[:500]  # HTMLの先頭500文字を取得
        except Exception as e:
            data["website_results"][website] = str(e)

    return data

# === セキュリティツール ===
def port_scan(ip, start=1, end=1024):
    open_ports = []
    for port in range(start, end + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((ip, port)) == 0:
                    open_ports.append(port)
        except Exception as e:
            return {"error": str(e)}
    return {"open_ports": open_ports}

def dns_lookup(domain):
    try:
        return {"ip": socket.gethostbyname(domain)}
    except Exception as e:
        return {"error": str(e)}

def whois_lookup(domain):
    try:
        whois_info = whois.whois(domain)
        return dict(whois_info)
    except Exception as e:
        return {"error": str(e)}

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(length))

def hash_sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

# === フラスクのルート ===
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run_tool/<tool>", methods=["GET", "POST"])
def run_tool(tool):
    try:
        if tool == "collect_data":
            result = collect_data()
        elif tool == "port_scan":
            ip = request.args.get("ip", "127.0.0.1")
            result = port_scan(ip)
        elif tool == "dns_lookup":
            domain = request.args.get("domain", "example.com")
            result = dns_lookup(domain)
        elif tool == "whois_lookup":
            domain = request.args.get("domain", "example.com")
            result = whois_lookup(domain)
        elif tool == "password_generator":
            length = int(request.args.get("length", 12))
            result = {"password": generate_password(length)}
        elif tool == "sha256_encrypt":
            data = request.args.get("data", "example")
            result = {"hash": hash_sha256(data)}
        else:
            result = {"error": "Unknown tool"}
    except Exception as e:
        result = {"error": str(e)}

    return jsonify(result)

@app.route("/config", methods=["GET", "POST"])
def manage_config():
    if request.method == "POST":
        new_config = request.json
        save_config(new_config)
        global config
        config = load_config()
        return jsonify({"status": "success"})
    else:
        return jsonify(config)

# === メイン ===
if __name__ == "__main__":
    app.run(debug=True)
