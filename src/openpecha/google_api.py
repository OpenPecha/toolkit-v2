from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from openpecha.config import GOOGLE_API_CRENDENTIALS_PATH, PECHAS_PATH


class GoogleDocAndSheetsDownloader:
    def __init__(
        self,
        google_docs_link: Optional[str] = None,
        google_sheets_link: Optional[str] = None,
        credentials_path: Optional[str] = GOOGLE_API_CRENDENTIALS_PATH,
        output_dir: str | Path = PECHAS_PATH,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/drive.readonly"],
        )
        self.drive_service = build("drive", "v3", credentials=self.credentials)

        if google_docs_link is not None:
            google_docs_id = self.get_id_from_link(google_docs_link)
            self.docx_path = self.get_google_docs(google_docs_id)

        if google_sheets_link is not None:
            google_sheets_id = self.get_id_from_link(google_sheets_link)
            self.sheets_path = self.get_google_sheets(google_sheets_id)

    def get_id_from_link(self, link: str) -> str:
        parsed_url = urlparse(link)
        path_segments = parsed_url.path.split("/")
        try:
            d_index = path_segments.index("d")
            doc_id = path_segments[d_index + 1]
            if not doc_id:
                raise ValueError("Document ID is empty.")
            return doc_id
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid Google Docs link format: {link}") from e

    def get_google_docs(self, google_docs_id: str) -> Optional[Path]:
        try:
            file_metadata = (
                self.drive_service.files()
                .get(fileId=google_docs_id, fields="name")
                .execute()
            )
            document_title = file_metadata.get("name", "untitled_document")
            docx_path = self.output_dir / f"{document_title}.docx"

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
            file_metadata = (
                self.drive_service.files()
                .get(fileId=google_sheets_id, fields="name")
                .execute()
            )
            sheet_title = file_metadata.get("name", "untitled_sheet")
            sheet_path = self.output_dir / f"{sheet_title}.xlsx"
            # Prepare the export request
            mime_type = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
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
