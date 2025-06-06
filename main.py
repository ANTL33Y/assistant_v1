"""
Entry point for launching the React web interface.
Running this script starts the Vite dev server and opens the UI.
"""
from pathlib import Path
import subprocess
import webbrowser

DEV_URL = "http://localhost:5173"


def main() -> None:
    web_dir = Path(__file__).parent / "web"
    subprocess.Popen(["npm", "run", "dev"], cwd=web_dir)
    webbrowser.open(DEV_URL)


if __name__ == "__main__":
    main()
