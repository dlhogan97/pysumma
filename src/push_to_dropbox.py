import os
import dropbox
from dropbox.exceptions import ApiError
import json
import time

# read token file
with open('/home/dlhogan/GitHub/pysumma/.dropbox_token', 'r') as f:
    token = f.read().strip()
# read OAuth2 information
with open("/home/dlhogan/GitHub/pysumma/dropbox.json") as f:
    app_data = json.load(f)
    APP_KEY = app_data['APP_KEY']
    APP_SECRET = app_data['APP_SECRET']

def upload_folder_to_dropbox(local_folder_path, dropbox_folder_path, access_token, delay=0.5, max_retries=3):
    """
    Uploads all files from a local folder to a Dropbox folder with rate limiting and retries.

    Parameters:
        local_folder_path (str): Path to the local folder containing files to upload.
        dropbox_folder_path (str): Path in Dropbox where files will be uploaded.
        access_token (str): Access token for Dropbox API.
        delay (float): Time (in seconds) to wait between file uploads to respect rate limits.
        max_retries (int): Number of times to retry a failed upload.

    Returns:
        str: Summary message indicating the result of the upload.
    """
    try:
        # Initialize Dropbox client
        dbx = dropbox.Dropbox(app_key=APP_KEY,
                              app_secret=APP_SECRET,
                              oauth2_refresh_token=access_token)
        
        # Iterate through files in the local folder
        for root, _, files in os.walk(local_folder_path):
            for file_name in files:
                local_file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(local_file_path, local_folder_path)
                dropbox_file_path = os.path.join(dropbox_folder_path, relative_path).replace("\\", "/")
                
                # Retry logic for file upload
                for attempt in range(max_retries):
                    try:
                        with open(local_file_path, "rb") as f:
                            dbx.files_upload(f.read(), dropbox_file_path, mode=dropbox.files.WriteMode("overwrite"))
                        print(f"Uploaded: {dropbox_file_path}")
                        break  # Exit retry loop on success
                    except ApiError as e:
                        if attempt < max_retries - 1:
                            print(f"Retrying ({attempt + 1}/{max_retries}) for file: {dropbox_file_path} due to error: {e}")
                            time.sleep(delay * 2)  # Backoff strategy for retries
                        else:
                            print(f"Failed to upload: {dropbox_file_path} after {max_retries} attempts.")
                
                # Wait to respect rate limits
                time.sleep(delay)
        
        return f"All files from '{local_folder_path}' have been processed for upload to '{dropbox_folder_path}'."
    except Exception as e:
        return f"An error occurred: {e}"


# Example usage
# Replace 'your-access-token' with your Dropbox API access token
access_token = token
figures_file = "/home/dlhogan/GitHub/pysumma/src/figures/"  # Path to your model output file
output_file = "/home/dlhogan/GitHub/pysumma/src/output/"  # Output file name
dropbox_figure_path = "/Apps/push-and-pull-pysumma/figures"  # Destination path in Dropbox
dropbox_output_path = "/Apps/push-and-pull-pysumma/output"  # Destination path in Dropbox

result = upload_folder_to_dropbox(figures_file, dropbox_figure_path, access_token)
print(result)

result = upload_folder_to_dropbox(output_file, dropbox_output_path, access_token)
print(result)