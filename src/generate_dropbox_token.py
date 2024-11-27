import json
import requests
import webbrowser
import base64

with open("/home/dlhogan/GitHub/pysumma/dropbox.json") as f:
    token = json.load(f)
    APP_KEY = token['APP_KEY']
    APP_SECRET = token['APP_SECRET']
    ACCESS_CODE_GENERATED = token['ACCESS_CODE_GENERATED']
url = f"https://www.dropbox.com/oauth2/authorize?client_id={APP_KEY}&token_access_type=offline&response_type=code"

try:
    BASIC_AUTH = base64.b64encode(f'{APP_KEY}:{APP_SECRET}'.encode())

    headers = {
        'Authorization': f"Basic {BASIC_AUTH}",
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = f'code={ACCESS_CODE_GENERATED}&grant_type=authorization_code'

    response = requests.post('https://api.dropboxapi.com/oauth2/token', data=data, auth=(APP_KEY, APP_SECRET), headers=headers)

    # write refresh token to file
    with open("/home/dlhogan/GitHub/pysumma/.dropbox_token", "w") as f:
        f.write(json.loads(response.text)['refresh_token'])
    print('Refresh token saved to .dropbox_token file.')
except:
    # Open URL in web
    PermissionError(f'Go to {url} to get the access code.')
    print('Copy the access code and paste it in the ACCESS_CODE_GENERATED variable in the dropbox.json file.')
