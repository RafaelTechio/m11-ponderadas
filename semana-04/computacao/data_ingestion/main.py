from .config import Config
from .app import App

def main():
    app = App(Config())
    app.run()

if __name__ == "__main__":
    main()