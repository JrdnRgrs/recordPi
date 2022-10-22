from dotenv import load_dotenv
import os
# Read Env Vars
load_dotenv()
access_key = os.environ.get("ACCESS_KEY")
access_secret = os.environ.get("ACCESS_SECRET")
host = os.environ.get("HOST")