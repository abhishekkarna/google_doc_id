1. Create a virtual environment - 'virtualenv -p python3 <ENVIRONMENT_NAME>'
2. Activate the environment - 'source <ENVIRONMENT_NAME>/bin/activate
3. Install dependencies - 'pip install -r requirement.txt'
4. Create service account from Google developer console and enable drive api + sheets api (https://console.cloud.google.com/apis/credentials/oauthclient)
5. Download service account json file and place in the root directory parallel to credentials.json.
6. Create .env file in root directory with following contents -
    SERVICE_ACCOUNT = <service_account_json_file_name>
    GOOGLE_SHEET = <GOOGLE_SHEET_LINK>
    WORKSHEET_TITLE = <GOOGLE_SHEET_TITLE>
    ROOT_FOLDER = <ROOT_FOLDER_IN_DRIVE>
7. In google sheet, click on 'share' and add service account email mentioned in service account json file.
8. Run python app.py.
9. At first launch, it would ask for user consent, later on it would store credentials in a file and won't ask for consent