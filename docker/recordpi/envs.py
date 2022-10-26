from dotenv import load_dotenv
import os
# Read Env Vars
load_dotenv()

## Shared Values
ice_host = os.environ.get("ICE_HOST")
ice_port = os.environ.get("ICE_PORT")
ice_mount = os.environ.get("ICE_MOUNT")
clip_base_name = os.environ.get("CLIP_BASE_NAME")
clip_base_path = os.environ.get("CLIP_BASE_PATH")
clip_api_url = os.environ.get("CLIP_API_URL")
### Audd Values
audd_token = os.environ.get("AUDD_API_TOKEN")
return_values = os.environ.get("RETURN_VALUES")

#### ACR Values
## ACR FS
acr_access_token = os.environ.get("ACR_ACCESS_TOKEN")
acr_container_id = os.environ.get("ACR_CONTAINER_ID")

## ACR ID
acr_id_host = os.environ.get("ACR_ID_HOST")
acr_access_key = os.environ.get("ACR_ACCESS_KEY")
acr_access_secret = os.environ.get("ACR_ACCESS_SECRET")