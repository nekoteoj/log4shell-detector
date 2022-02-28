import os
import pathlib
from asyncio import Lock

from sanic import Sanic
from sanic.response import file, json

request_class_flag = False
request_class_flag_lock = Lock()

app = Sanic("SafeAppServer")

@app.get("/")
async def index_handler(request):
    global request_class_flag
    async with request_class_flag_lock:
        request_class_flag = False
    return json({"message": "Server is working properly."})

@app.get("/SafeApp.class")
async def safe_app_handler(request):
    global request_class_flag
    async with request_class_flag_lock:
        request_class_flag = True
    filepath = pathlib.Path(__file__).parent.resolve()
    filepath = os.path.join(filepath, "SafeApp.class")
    return await file(filepath, filename="SafeApp.class")

@app.post("/reset")
async def reset_handler(request):
    global request_class_flag
    async with request_class_flag_lock:
        request_class_flag = False
    return json({"message": "Success"})

@app.get("/status")
async def status_handler(request):
    return json({"status": request_class_flag})

app.run(host="0.0.0.0", port=5000)
