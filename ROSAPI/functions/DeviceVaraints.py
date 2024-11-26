from ROSAPI.Models.deviceModels import variantDataModel
from ROSAPI.authentication.github import repo
from concurrent.futures import ThreadPoolExecutor
import json

def deviceVariants(codename: str):
    """
    Fetches variant data for a given codename concurrently.
    Returns a list of variant data in the order: vanilla -> core -> gapps.
    """
    def fetch_variant(variant: str):
        try:
            response = repo.get_contents(f"{variant}_{codename}.json").decoded_content.decode("utf-8")
            return json.loads(response)['response'][0]
        except Exception:
            print(f"{variant} variant not available")
            return None

    variants = ["VANILLA", "CORE", "GAPPS"]

    # Fetch all variants concurrently
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_variant, variants))

    # Filter out None results and return the data in the desired order
    return [variant for variant in results if variant]
