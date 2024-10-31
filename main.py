from fastapi import FastAPI
import requests

app = FastAPI(title="ROSAPI", version="0.1.0")

# API entry
@app.get("/")
async def root():
    return {"API_Status" :"The API is Up and Running!"}

@app.get("/device/{codename}")
async def get_device(codename: str):
     variants_data : list = []

     vanilla_response = requests.get(f"https://raw.githubusercontent.com/ZirgomHaidar/android_vendor_RisingOTA/refs/heads/fourteen/VANILLA_{codename}.json")
     core_response = requests.get(f"https://raw.githubusercontent.com/ZirgomHaidar/android_vendor_RisingOTA/refs/heads/fourteen/CORE_{codename}.json")
     gapps_response = requests.get(f"https://raw.githubusercontent.com/ZirgomHaidar/android_vendor_RisingOTA/refs/heads/fourteen/GAPPS_{codename}.json")

     if vanilla_response.status_code == 200:
        vanilla_data = vanilla_response.json()
        variants_data.append(vanilla_data['response'][0])

     if core_response.status_code == 200:
        core_data = core_response.json()
        variants_data.append(core_data['response'][0])

     if gapps_response.status_code == 200:
        gapps_data = gapps_response.json()
        variants_data.append(gapps_data['response'][0])

     return variants_data # the data will always return in order vanilla -> core -> gapps
