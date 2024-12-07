import os
import subprocess
import sys

def install_requirements():
    """
    Install the required libraries from requirements.txt.
    """
    print("Installing required libraries...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def start_server():
    """
    Start the Flask server.
    """
    print("Starting Flask server...")
    os.system(f"{sys.executable} app.py")

if __name__ == "__main__":
    try:
        install_requirements()
        start_server()
    except Exception as e:
        print(f"An error occurred: {e}")
