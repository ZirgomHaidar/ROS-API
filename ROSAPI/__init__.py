from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from ROSAPI.Models import DnListModel
from ROSAPI.functions.DeviceVaraints import deviceVariants
from ROSAPI.functions.DeviceList import update_devicelist
from ROSAPI.functions.DeviceList import deviceInfo_list

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup and updating the devicelist now")
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_devicelist, "interval", minutes=10) # run it with 10 mins of interval
    scheduler.start()
    update_devicelist() # Run on startup once and then -------------------> /^\
    print("DeviceList is updated!!")
    yield
    print("Shutting Down the API")

app = FastAPI(title="ROSAPI", version="1.1.0", lifespan=lifespan)

# API entry
@app.get("/")
async def root():
    return {"API_Status" :"The API is Up and Running!"}

@app.get("/api/v1/device/deviceList", response_model= list[DnListModel])
async def get_devicelist():
    return deviceInfo_list

@app.get("/api/v1/device/{codename}")
async def get_device(codename: str):
    return deviceVariants(codename)
