"""
Entry point for the voice assistant web interface.
Running this script starts the Flask GUI and opens it in a browser.
"""
import webbrowser

from web_gui import app


def main() -> None:
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)


if __name__ == "__main__":
    main()
