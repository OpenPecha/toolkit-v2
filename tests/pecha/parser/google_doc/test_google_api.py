from openpecha.pecha.parsers.google_doc.google_api import GoogleDocAndSheetsDownloader

def test_google_api():
    google_docs_id = "1uISaW2HYeS3vCPeAhiDTn-RmwDkM1B7kvhMGTEPyfp0"
    google_sheets_id = "1ZOftYpK_NjUVjAf4cWk_CTW143lEEM4rH64gSWQRr7A"
    google_obj = GoogleDocAndSheetsDownloader(google_docs_id=google_docs_id, google_sheets_id=google_sheets_id)
    assert (google_obj.docx_path).exists and (google_obj.sheets_path).exists