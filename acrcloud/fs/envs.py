from dotenv import load_dotenv
import os
# Read Env Vars
load_dotenv()
access_token = os.environ.get("ACCESS_TOKEN")
container_id = os.environ.get("CONTAINER_ID")
token = access_token
container=container_id
url = f"https://api-v2.acrcloud.com/api/fs-containers/{container}/files"
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {token}'
  }