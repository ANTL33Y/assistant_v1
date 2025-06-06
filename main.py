import argparse
import os
import subprocess
import sys
import time
import webbrowser
from pathlib import Path
import requests
import venv
import shutil

FRONTEND_DIR = Path('frontend')
VENV_DIR = Path('.venv')

BACKEND_CMD_DEV = ['uvicorn', 'backend.assistant_api:app', '--reload', '--port', '8000']
BACKEND_CMD_PROD = ['uvicorn', 'backend.assistant_api:app', '--host', '0.0.0.0', '--port', '8000']


def ensure_venv():
    if not VENV_DIR.exists():
        print('Creating virtualenv...')
        venv.EnvBuilder(with_pip=True).create(str(VENV_DIR))
        pip = VENV_DIR / ('Scripts' if os.name == 'nt' else 'bin') / 'pip'
        subprocess.check_call([str(pip), 'install', 'fastapi', 'uvicorn', 'python-multipart'])


def npm_install_once():
    if not (FRONTEND_DIR / 'node_modules').exists():
        subprocess.check_call(['npm', 'install'], cwd=FRONTEND_DIR)
        subprocess.check_call(['npm', 'run', 'build'], cwd=FRONTEND_DIR)
        static_dir = Path('backend') / 'static'
        if static_dir.exists():
            shutil.rmtree(static_dir)
        shutil.copytree(FRONTEND_DIR / 'dist', static_dir)


def wait_for(url: str, timeout=60):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = requests.get(url)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def run_dev():
    ensure_venv()
    npm_install_once()
    python = VENV_DIR / ('Scripts' if os.name == 'nt' else 'bin') / 'python'
    uvicorn = VENV_DIR / ('Scripts' if os.name == 'nt' else 'bin') / 'uvicorn'
    backend = subprocess.Popen([str(uvicorn), *BACKEND_CMD_DEV[1:]])
    frontend = subprocess.Popen(['npm', 'run', 'dev'], cwd=FRONTEND_DIR)

    if wait_for('http://127.0.0.1:8000/health') and wait_for('http://localhost:5173'):
        webbrowser.open('http://localhost:5173')

    try:
        while True:
            if backend.poll() is not None or frontend.poll() is not None:
                break
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        backend.terminate()
        frontend.terminate()
        backend.wait()
        frontend.wait()


def run_prod():
    ensure_venv()
    uvicorn = VENV_DIR / ('Scripts' if os.name == 'nt' else 'bin') / 'uvicorn'
    subprocess.call([str(uvicorn), *BACKEND_CMD_PROD[1:]])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prod', action='store_true', help='Production mode')
    args = parser.parse_args()

    if args.prod:
        run_prod()
    else:
        run_dev()
