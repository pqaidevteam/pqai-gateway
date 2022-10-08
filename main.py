import os
import configparser
import importlib
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

config = configparser.ConfigParser()
config.read('config.ini')

app = FastAPI()

def import_plugin(name):
    path = f"plugins.{name}.routes"
    routes = importlib.import_module(path)
    app.include_router(routes.router)


if 'plugins' in config:
    activated = config["plugins"]["active"].split(',')
    for plugin in activated:
        import_plugin(plugin.strip())


if __name__ == "__main__":
    port = int(os.environ['PORT'])
    uvicorn.run(app, host="0.0.0.0", port=port)
