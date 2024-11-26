from ROSAPI.Models.deviceModels import DnListModel
from ROSAPI.authentication.github import repo
from concurrent.futures import ThreadPoolExecutor
import json

deviceInfo_list : list[DnListModel] = []

def fetch_variant_data(repo, codename, variant):
    """
    Fetches data for a specific variant (e.g., GAPPS, VANILLA, CORE) for a given codename.
    """
    try:
        response = repo.get_contents(f"{variant}_{codename}.json").decoded_content.decode("utf-8")
        if response:
            data = json.loads(response)
            timestamp = data['response'][0].get('timestamp', 0)
            return data, timestamp
    except Exception:
        print(f"{variant} variant not available for {codename}")
    return {}, 0

def update_devicelist():
    """
    Updates the device list with information from the repository.
    """
    # Reset the device list
    deviceInfo_list.clear()

    # Fetch the list of codenames
    try:
        response = repo.get_contents("risingOS.devices").decoded_content.decode("utf-8")
        codename_list = [line.strip() for line in response.splitlines() if line.strip()]
    except Exception as e:
        print(f"Failed to retrieve device list. Error: {e}")
        return

    # Process each codename
    for codename in codename_list:
        print(f"Processing {codename}...")

        try:
            # Fetch all variants concurrently
            variants = ["GAPPS", "VANILLA", "CORE"]
            with ThreadPoolExecutor() as executor:
                results = list(executor.map(lambda v: fetch_variant_data(repo, codename, v), variants))

            # Extract data and timestamps
            gapps_data, gapps_timestamp = results[0]
            vanilla_data, vanilla_timestamp = results[1]
            core_data, core_timestamp = results[2]

            # Determine the most recent timestamp
            last_updated = max(vanilla_timestamp, core_timestamp, gapps_timestamp)

            # Extract common data (fallback to available variant data)
            oem = (
                gapps_data.get('response', [{}])[0].get('oem', '') or
                core_data.get('response', [{}])[0].get('oem', '') or
                vanilla_data.get('response', [{}])[0].get('oem', '')
            )
            device = (
                gapps_data.get('response', [{}])[0].get('device', '') or
                core_data.get('response', [{}])[0].get('device', '') or
                vanilla_data.get('response', [{}])[0].get('device', '')
            )
            version = (
                gapps_data.get('response', [{}])[0].get('version', '') or
                core_data.get('response', [{}])[0].get('version', '') or
                vanilla_data.get('response', [{}])[0].get('version', '')
            )

            # Create and append the device data
            data = DnListModel(
                codename=codename,
                oem=oem,
                device=device,
                last_updated=last_updated,
                version=version,
                changelog_url=f"https://raw.githubusercontent.com/ZirgomHaidar/android_vendor_RisingOTA/refs/heads/fourteen/changelog_{codename}.txt"
            )
            deviceInfo_list.append(data.model_dump())

        except Exception as e:
            print(f"Failed to process {codename}. Error: {e}")

    # Sort the device list by last_updated (newest first)
    print("Sorting the data...")
    deviceInfo_list.sort(key=lambda x: x['last_updated'], reverse=True)
    print("Sorting DONE!")
