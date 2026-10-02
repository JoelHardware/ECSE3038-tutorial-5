import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["ecse3038"]
devices = db["tutorial5"]

app = FastAPI()


class Device(BaseModel):
    name: str
    room: str
    temp: float
    online: bool


# Your handlers go below this line.

#Task 1: Write a get request to print all devices
@app.get("/devices")
async def get_devices():
    return devices.find({}, {"_id": 0})

#task 2: Write a get request to print a device by name
@app.get("/devices/{name}")
async def get_device(name: str):
    device = devices.find_one({"name": name}, {"_id": 0})
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

#task 3: Write a post request to add a device
@app.post("/devices")
async def add_device(device: Device):
    devices.insert_one(device.dict())
    return device

#task 4: Write a put request to update a device by name
@app.put("/devices/{name}")
async def update_device(name: str, device: Device):
    result = devices.replace_one({"name": name}, device.dict())
    if not result.matched_count:
        raise HTTPException(status_code=404, detail="Device not found")
    return device
