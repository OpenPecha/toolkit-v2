import io
import pickle
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from openpecha.config import GOOGLE_API_CRENDENTIALS_PATH, GOOGLE_API_TOKEN_PATH


class GoogleDocAndSheetsDownloader:
    def __init__(
        self,
        credential_path: str = GOOGLE_API_CRENDENTIALS_PATH,
    ):
        self.credential_path = credential_path
        self.token = self.authenticate()

    def authenticate(self):
        """
        Authenticate the user using the credentail json file.
        If not authenticated, it will open a browser to authenticate the user.And save the token in the token.pickle file.

        If yes, it will load the token from the token.pickle file.
        """
        SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

        creds = None
        if GOOGLE_API_TOKEN_PATH.exists():
            with open(GOOGLE_API_TOKEN_PATH, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credential_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(GOOGLE_API_TOKEN_PATH, "wb") as token:
                pickle.dump(creds, token)

        self.token = creds

    def get_id_from_link(self, link: str) -> Optional[str]:
        """
        Input: link to a Google Doc or Google sheet Document.
        Output:  Document ID.
        """
        parsed_link = urlparse(link)
        segments = parsed_link.path.split("/")
        try:
            index = segments.index("d")
            id = segments[index + 1]
            if not id:
                raise ValueError("Document ID is empty.")
            return id
        except Exception as e:
            raise ValueError(f"[Invalid link]:[{link}]{str(e)}")

    def get_google_docx(self, file_link: str, output_path: Path):
        file_id = self.get_id_from_link(file_link)
        try:
            service = build("drive", "v3", credentials=self.token)
            request = service.files().export_media(
                fileId=file_id,
                mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                supportsAllDrives=True,
            )
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                _, done = downloader.next_chunk()

            fh.seek(0)
            with open(output_path, "wb") as f:
                f.write(fh.read())

            return output_path
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_google_sheet(self, file_link: str, output_path: Path):
        file_id = self.get_id_from_link(file_link)
        try:
            service = build("drive", "v3", credentials=self.token)
            request = service.files().export_media(
                fileId=file_id,
                mimeType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                supportsAllDrives=True,
            )
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                _, done = downloader.next_chunk()

            fh.seek(0)
            with open(output_path, "wb") as f:
                f.write(fh.read())

            return output_path
        except Exception as e:
            print(f"An error occurred: {e}")
