from dotenv import load_dotenv
import os
# Read Env Vars
load_dotenv()
token = os.environ.get("API_TOKEN")
url_flag = os.environ.get("URL_FLAG")
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
region_name = os.environ.get("AWS_DEFAULT_REGION")
bucket_name = os.environ.get("BUCKET_NAME")
ice_host = os.environ.get("ICE_HOST")
ice_port = os.environ.get("ICE_PORT")
ice_mount = os.environ.get("ICE_MOUNT")