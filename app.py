from pydrive.drive import GoogleDrive
import pygsheets
import os
from dotenv import load_dotenv
load_dotenv('./.env')
# Constants
PATH_TO_SERVICE_ACCOUNT = os.environ.get('SERVICE_ACCOUNT')

ROOT_FOLDER_ID = ""
sheet = None
drive = GoogleDrive()
GOOGLE_SHEET_CLIENT = pygsheets.authorize(service_account_file=PATH_TO_SERVICE_ACCOUNT)

"""
Take user inputs
"""
def userInput():
    while True:
        if input('Do you want to enter google sheet url (Y/N) ? ') in ('y', 'Y'):
            GOOGLE_SHEET = input()
        else:
            GOOGLE_SHEET = os.environ.get('GOOGLE_SHEET')
        WORKSHEET_TITLE = input('Please enter worksheet title : ')
        ROOT_FOLDER = input('Please enter the root folder : ')
        if '' not in (GOOGLE_SHEET,WORKSHEET_TITLE,ROOT_FOLDER):
            return (GOOGLE_SHEET,WORKSHEET_TITLE,ROOT_FOLDER)
        else:
            print('Not valid input. Please retry.')

def main():
    GOOGLE_SHEET,WORKSHEET_TITLE,ROOT_FOLDER = userInput()
    sheet = GOOGLE_SHEET_CLIENT.open_by_url(GOOGLE_SHEET).worksheet_by_title(WORKSHEET_TITLE)
    # Query to print top level items
    file_list = drive.ListFile(
        {'q': "'root' in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"}).GetList()
    
    # Search the root folder
    for file in file_list:
        if(file['title'] == ROOT_FOLDER):
            ROOT_FOLDER_ID = file['id']
            break

    # Query to get all subfolders
    query = "\'" + ROOT_FOLDER_ID + "\'" + \
        " in parents and trashed=false and mimeType='application/vnd.google-apps.folder'"
 
    # Getting id and title of each file and writing to Google sheet
    subFolderList = drive.ListFile({'q': query}).GetList()
    for subFolder in subFolderList:
        print('-----Searching through folder -> ',subFolder)
        subQuery = "\'" + subFolder['id'] + "\'" + \
            " in parents and trashed=false and mimeType!='application/vnd.google-apps.folder'"
        files = drive.ListFile({'q': subQuery}).GetList()
        for file in files:
            sheet.insert_rows(sheet.rows, values=[
                file['title'], file['id']], inherit=True)


if __name__ == "__main__":
    main()
