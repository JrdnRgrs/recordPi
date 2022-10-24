from functions import *
from time import sleep
api_data_file_name = "clip.json"
suffix_digits=4
# Run idefinitely, sleeping for 30 seconds in between.
while True:
    print("Running Stream Clipper")
    my_clip_suffix = get_clip_suffix(suffix_digits)
    my_clip_name = f"{clip_base_name}-{my_clip_suffix}"
    my_clip_path = get_stream_recording(my_clip_suffix)
    print(f"Saved file to {my_clip_path}")
    is_quiet = is_clip_quiet(my_clip_path)
    if is_quiet==True:
        # set api should_run = false
        should_run = False
    else:
        should_run = True
    set_api_data(my_clip_name,my_clip_suffix,should_run)

    print("Sleeping for 30 seconds")
    sleep(30)