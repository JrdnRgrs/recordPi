from time import sleep
from functions import *
from helpers import *

pick_api = os.environ.get("PICK_API")
#while True:
try:
    if pick_api == "audd":
        ## Audd
        while True:
            print("Running the Audd Loop")
            audd_api_wrapper()
    elif pick_api == "acr_fs":
        ## ACR FS
        while True:
            print("Running the ACR FS Loop")
            acr_fs_api_wrapper()
    elif pick_api == "acr_id":
        ## ACR ID
        while True:
            print("Running the ACR ID Loop")
            acr_id_api_wrapper()
    else:
        print("No PICK_API was selected.")
finally:
    print("Exiting Loop...Sleeping for 5 seconds")
    sleep(5)
    #break