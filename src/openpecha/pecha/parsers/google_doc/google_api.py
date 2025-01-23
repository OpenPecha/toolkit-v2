import io
import pickle
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from openpecha.config import GOOGLE_API_TOKEN_PATH


class GoogleDocAndSheetsDownloader:
    def __init__(self, token_path: Path = GOOGLE_API_TOKEN_PATH):
        """
        This token should be a .pickle file
        1.Go to Google API
        2.Create a Oauth2 web app api
        3.Download the api credential .json file
        4.Authenticate through pop up window
        5.Give .pickle token here
        """
        self.token_path: Path = token_path

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
            raise ValueError(f"[Invalid link] [{link}]{str(e)}")

    def get_google_docx(self, file_link: str, output_path: Path):
        with open(self.token_path, "rb") as token:
            cred = pickle.load(token)

        file_id = self.get_id_from_link(file_link)
        try:
            service = build("drive", "v3", credentials=cred)
            request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
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
        with open(self.token_path, "rb") as token:
            cred = pickle.load(token)

        file_id = self.get_id_from_link(file_link)
        try:
            service = build("drive", "v3", credentials=cred)
            request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
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


def get_token_via_authentication(
    credential_path: Path, output_dir: Path = Path(".")
) -> Path:
    """
    Get authenticated token via web app credential
    """
    SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

    flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
    creds = flow.run_local_server(port=0)
    output_dir.mkdir(parents=True, exist_ok=True)
    token_file_path = output_dir / "token.pickle"
    with open(token_file_path, "wb") as token:
        pickle.dump(creds, token)
    return token_file_path
