from dotenv import load_dotenv
import os
# Read Env Vars
load_dotenv()
token = os.environ.get("API_TOKEN")
ice_host = os.environ.get("ICE_HOST")
ice_port = os.environ.get("ICE_PORT")
ice_mount = os.environ.get("ICE_MOUNT")
clip_base_name = os.environ.get("CLIP_BASE_NAME")
clip_base_path = os.environ.get("CLIP_BASE_PATH")
clip_api_url = os.environ.get("CLIP_API_URL")
return_values = os.environ.get("RETURN_VALUES")