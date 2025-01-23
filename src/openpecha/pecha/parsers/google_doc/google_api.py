import io
import pickle
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from openpecha.config import GOOGLE_API_TOKEN_PATH


class GoogleDocAndSheetsDownloader:
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
        with open(GOOGLE_API_TOKEN_PATH, "rb") as token:
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
        with open(GOOGLE_API_TOKEN_PATH, "rb") as token:
            cred = pickle.load(token)

        file_id = self.get_id_from_link(file_link)
        try:
            service = build("drive", "v3", credentials=cred)
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
