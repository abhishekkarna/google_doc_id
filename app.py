from pydrive.drive import GoogleDrive
import pygsheets
import os
from dotenv import load_dotenv
load_dotenv('./.env')
# Constants
PATH_TO_SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT')
GOOGLE_SHEET = os.environ.get('GOOGLE_SHEET')
WORKSHEET_TITLE = os.environ.get('WORKSHEET_TITLE')
ROOT_FOLDER = os.environ.get('ROOT_FOLDER')
ROOT_FOLDER_ID = ""

# Clients
drive = GoogleDrive()
GOOGLE_SHEET_CLIENT = pygsheets.authorize(
    service_account_file=PATH_TO_SERVICE_ACCOUNT)
sheet = GOOGLE_SHEET_CLIENT.open_by_url(
    GOOGLE_SHEET).worksheet_by_title(WORKSHEET_TITLE)

# Searching the root folder
file_list = drive.ListFile(
    {'q': "'root' in parents and trashed=false"}).GetList()
for file in file_list:
    if(file['title'] == ROOT_FOLDER):
        ROOT_FOLDER_ID = file['id']
        break

# Query to get all files and exclude folders
query = "\'" + ROOT_FOLDER_ID + "\'" + \
    " in parents and trashed=false and mimeType!='application/vnd.google-apps.folder'"

# Getting id and title of each file and writing to Google sheet
file_list = drive.ListFile({'q': query}).GetList()
for file in file_list:
    sheet.insert_rows(sheet.rows, values=[
                      file['title'], file['id']], inherit=True)
