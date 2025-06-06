"""
Entry point for launching the React web interface.
Running this script starts the Vite dev server and opens the UI.
"""
from pathlib import Path
import subprocess
import webbrowser
import os

DEV_URL = "http://localhost:5173"


def main() -> None:
    web_dir = Path(__file__).parent / "web"
    npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
    # Install front-end dependencies if node_modules is missing
    if not (web_dir / "node_modules").exists():
        subprocess.run([npm_cmd, "install"], cwd=web_dir, check=True)

    subprocess.Popen([npm_cmd, "run", "dev"], cwd=web_dir)
    webbrowser.open(DEV_URL)


if __name__ == "__main__":
    main()
