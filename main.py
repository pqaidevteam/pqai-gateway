import os
import configparser
import importlib
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Response

load_dotenv()

config = configparser.ConfigParser()
config.read('config.ini')

app = FastAPI()

authentication_enabled = False
if "authentication" in config:
    authentication_enabled = config["authentication"].getboolean("enabled", fallback=False)

tokens = set()

if os.environ.get("TEST_TOKEN"):
    tokens.add(os.environ.get("TEST_TOKEN"))

if authentication_enabled and "tokens" in config["authentication"]:
    if config["authentication"]["tokens"].strip():
        for string in config["authentication"]["tokens"].split(","):
            tokens.add(string.strip())


@app.middleware("http")
async def authenticate(request, call_next):
    if not authentication_enabled:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if auth_header is None:
        return Response(status_code=401, content="Missing authorization header")
    
    if not auth_header.startswith("Bearer "):
        return Response(status_code=401, content="Invalid authorization header")
    
    token = auth_header.split(" ")[1]
    if token not in tokens:
        return Response(status_code=401, content="Invalid token")
    
    return await call_next(request)

def import_plugin(name):
    path = f"plugins.{name}.routes"
    routes = importlib.import_module(path)
    app.include_router(routes.router)
    print(f"Loaded plugin: {name}")


if 'plugins' in config:
    activated = config["plugins"]["active"].split(',')
    for plugin in activated:
        import_plugin(plugin.strip())


if __name__ == "__main__":
    port = int(os.environ['PORT'])
    uvicorn.run(app, host="0.0.0.0", port=port)
