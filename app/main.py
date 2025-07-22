import subprocess
import threading
import sys

def run_flask():
    subprocess.run([sys.executable, "flask_api.py"])

def run_streamlit():
    subprocess.run([
        "streamlit", "run", "streamlit_app.py",
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ])

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    run_streamlit()
