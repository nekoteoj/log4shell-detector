import os
import pathlib

from sanic import Sanic
from sanic.response import file, json

app = Sanic("SafeAppServer")

@app.get("/")
async def index_handler(request):
    return json({"message": "Server is working properly."})

@app.get("/get-safe-app")
async def safe_app_handler(request):
    filepath = pathlib.Path(__file__).parent.resolve()
    filepath = os.path.join(filepath, "SafeApp.class")
    return await file(filepath, filename="SafeApp.class")

app.run(host="0.0.0.0", port=5000)
