from dotenv import load_dotenv
import os
# Read Env Vars
load_dotenv()
ice_host = os.environ.get("ICE_HOST")
ice_port = os.environ.get("ICE_PORT")
ice_mount = os.environ.get("ICE_MOUNT")
recording_secs = os.environ.get("RECORDING_SECS")
clip_base_name = os.environ.get("CLIP_BASE_NAME")
clip_base_path = os.environ.get("CLIP_BASE_PATH")