import os
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("HUGGINGFACE_API_TOKEN")
print(f"Token: {token}")

if token:
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get("https://huggingface.co/api/whoami", headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        print(f"Token is valid for user: {user_info.get('name')}")
    else:
        print(f"Token validation failed: {response.status_code} - {response.text}")
else:
    print("No token found in environment variables")