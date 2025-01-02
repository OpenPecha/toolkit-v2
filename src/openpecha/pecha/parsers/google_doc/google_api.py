import os
import tempfile
from pathlib import Path
from typing import Optional

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload


tempdir = tempfile.TemporaryDirectory()
OUTPUT_DIR = Path(tempdir.name)


credentials_path = Path("~/.gcloud/google_docs_and_sheets.json").expanduser()
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(credentials_path)


class GoogleDocAndSheetsDownloader:
    def __init__(
        self,
        google_docs_id: Optional[str] = None,
        google_sheets_id: Optional[str] = None,
    ):
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )
        self.drive_service = build("drive", "v3", credentials=self.credentials)

        if google_docs_id is not None:
            self.docx_path = self.get_google_docs(google_docs_id)

        if google_sheets_id is not None:
            self.sheets_path = self.get_google_sheets(google_sheets_id)


    def get_google_docs(self, google_docs_id: str) -> Optional[Path]:
        try:
            file_metadata = self.drive_service.files().get(
                fileId=google_docs_id, fields="name"
            ).execute()
            document_title = file_metadata.get("name", "untitled_document")
            docx_path = OUTPUT_DIR / f"{document_title}.docx"

            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            request = self.drive_service.files().export_media(
                fileId=google_docs_id, mimeType=mime_type
            )
            with docx_path.open("wb") as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()
            return docx_path

        except HttpError as error:
            print(f"An error occurred: {error}")
            return None


    def get_google_sheets(self, google_sheets_id: str):
        try:
            # Get the sheet metadata to obtain the title
            file_metadata = self.drive_service.files().get(
                fileId=google_sheets_id, fields="name"
            ).execute()
            sheet_title = file_metadata.get("name", "untitled_sheet")
            # with tempfile.TemporaryDirectory() as tmpdirname:
            #     OUTPUT_DIR = Path(tmpdirname)
            sheet_path = OUTPUT_DIR / f"{sheet_title}.xlsx"

            # Prepare the export request
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            request = self.drive_service.files().export_media(
                fileId=google_sheets_id, mimeType=mime_type
            )

            # Download the file
            with sheet_path.open("wb") as fh:
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while not done:
                    _, done = downloader.next_chunk()

            return sheet_path
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None
        

class GoogleDocAndSheets:
    def __init__(self,google_docs_id: Optional[str] = None,google_sheets_id: Optional[str] = None):
        if google_docs_id is not None:
            self.docx_path = self.get_google_docs(google_docs_id)
        if google_sheets_id is not None:
            self.sheets_path = self.get_google_sheets(google_sheets_id)


    def get_google_docs(self, google_docs_id):
        try:
            docs_service = build('docs', 'v1')
            document = docs_service.documents().get(documentId=google_docs_id).execute()
            return document
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None


    def get_google_sheets(self, google_sheets_id: str):
        try:
            sheets_service = build('sheets', 'v4')
            sheet = sheets_service.spreadsheets().get(spreadsheetId=google_sheets_id).execute()
            return sheet
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None