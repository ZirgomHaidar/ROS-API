from fastapi import FastAPI
import requests
from pydantic import BaseModel

class DnListModel(BaseModel):
    codename : str
    oem : str
    device : str
    last_updated : int
    version : str
    changelog_url : str

deviceInfo_list : list[DnListModel] = []

app = FastAPI(title="ROSAPI", version="0.1.0")

def update_devicelist():
    # getting the list of official devices
    response = requests.get("https://raw.githubusercontent.com/ZirgomHaidar/android_vendor_RisingOTA/refs/heads/fourteen/risingOS.devices")

    # reset the devicelist
    deviceInfo_list.clear()

    # init some imp vars
    vanilla_data : dict = {}
    core_data : dict = {}
    gapps_data : dict = {}

    if response.status_code == 200:
        codename_list: list = response.text.split("\n")
        print(codename_list)

        vanilla_timestamp : int
        core_timestamp : int
        gapps_timestamp : int

        for codename in codename_list:
            if codename != '':
                print(codename)
                gapps_response = requests.get(f"https://raw.githubusercontent.com/ZirgomHaidar/android_vendor_RisingOTA/refs/heads/fourteen/GAPPS_{codename}.json")
                vanilla_response = requests.get(f"https://raw.githubusercontent.com/ZirgomHaidar/android_vendor_RisingOTA/refs/heads/fourteen/VANILLA_{codename}.json")
                core_response = requests.get(f"https://raw.githubusercontent.com/ZirgomHaidar/android_vendor_RisingOTA/refs/heads/fourteen/CORE_{codename}.json")
                try:

                    # checking if all the responses are 200 status or not
                    if vanilla_response.status_code == 200:
                        vanilla_data = vanilla_response.json()
                        vanilla_timestamp = vanilla_data['response'][0]['timestamp'] | 0
                    else:
                        vanilla_timestamp = 0

                    if core_response.status_code == 200:
                        core_data = core_response.json()
                        core_timestamp = core_data['response'][0]['timestamp'] | 0
                    else:
                        core_timestamp = 0

                    if gapps_response.status_code == 200:
                        gapps_data = gapps_response.json()
                        gapps_timestamp = gapps_data['response'][0]['timestamp'] | 0
                    else:
                        gapps_timestamp = 0

                    # trying to get data from variant response that is available
                    oem : str = gapps_data.get('response', [{}])[0].get('oem', '') or core_data.get('response', [{}])[0].get('oem', '') or vanilla_data.get('response', [{}])[0].get('oem', '')
                    device : str = gapps_data.get('response', [{}])[0].get('device', '') or core_data.get('response', [{}])[0].get('device', '') or vanilla_data.get('response', [{}])[0].get('device', '')
                    version : str = gapps_data.get('response', [{}])[0].get('version', '') or core_data.get('response', [{}])[0].get('version', '') or vanilla_data.get('response', [{}])[0].get('version', '')

                    data = DnListModel(
                        codename=codename,
                        oem=oem,
                        device=device,
                        last_updated=max(vanilla_timestamp, core_timestamp, gapps_timestamp),
                        version=version,
                        changelog_url=(f"https://raw.githubusercontent.com/ZirgomHaidar/android_vendor_RisingOTA/refs/heads/fourteen/changelog_{codename}.txt")
                    )

                    # pushing current codename data into the list
                    deviceInfo_list.append(data.model_dump())

                    #cleanup/reset to avoid carry forwarding of the current data
                    vanilla_data : dict = {}
                    core_data : dict = {}
                    gapps_data : dict = {}
                    oem = ""
                    device = ""
                    version = ""

                except Exception as e:
                    #cleanup/reset to avoid carry forwarding of the current data
                    vanilla_data : dict = {}
                    core_data : dict = {}
                    gapps_data : dict = {}
                    oem = ""
                    device = ""
                    version = ""
                    print(f"from try-Except Failed to retrieve data. Status code: {e}")
                    pass
            else:
                pass
    else:
        return(f"Failed to retrieve data. Status code: {response.status_code}")

# API entry
@app.get("/")
async def root():
    return {"API_Status" :"The API is Up and Running!"}

@app.get("/device/deviceList", response_model= list[DnListModel])
async def get_devicelist():
    return deviceInfo_list

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
