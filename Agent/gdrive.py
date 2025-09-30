import os.path
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]



def authenticate():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    
    return creds


def list_files(creds):
  try:
    service = build("drive", "v3", credentials=creds)

    # Call the Drive v3 API
    results = (
        
        service.files()
        .list(pageSize=20,fields="nextPageToken, files(id,name,mimeType)",orderBy="modifiedTime desc")
        .execute()
    )
    items = results.get("files", [])
  
    return items
  except HttpError as error:
    print(f"An error occurred: {error}")
    return None



def read_file_content(creds, file_id, mime_type):
    try:
        service = build("drive", "v3", credentials=creds, cache_discovery=False)
        
        if mime_type == 'application/vnd.google-apps.document':
            request = service.files().export_media(fileId=file_id, mimeType='text/plain')
        else:
            request = service.files().get_media(fileId=file_id)

        file = io.BytesIO()
        downloader = MediaIoBaseDownload(file, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
        file.seek(0)
        return file.read().decode('utf-8', errors='replace')
        
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None
    
def search_files(creds, query):
    service = build("drive", "v3", credentials=creds)
    results = service.files().list(
        q=f"name contains '{query}'",
        pageSize=20,
        fields="files(id, name, mimeType)"
    ).execute()
    return results.get("files", [])
