from github import Github
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Fetch the GitHub token from the environment
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("GitHub TOKEN not found in environment variables!")

# Authenticate and access the repository
git = Github(TOKEN)
repo = git.get_repo("ZirgomHaidar/android_vendor_RisingOTA")

print(f"Successfully connected to repository: {repo.full_name}")
