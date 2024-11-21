from pathlib import Path


class CommentarySerializer:
    def __init__(self):
        self.category = []
        self.books = []
        self.required_metadata = {}

    def extract_metadata(self, pecha_path: Path):
        """
        Extract neccessary metadata from opf for serialization to json
        """
        pass

    def set_metadata_to_json(self, pecha_path: Path):
        """
        Set extracted metadata to json format
        """
        pass

    def get_category(self, title: str):
        """
        Input: title: Title of the pecha commentary which will be used to get the category format
        Process: Get the category format from the pecha.org categorizer package
        """
        pass

    def set_category_to_json(self):
        """
        Set the category format to self.category attribute
        """
        pass

    def get_sapche_anns(self, pecha_path: Path):
        """
        Get the sapche annotations from the sapche layer
        """
        pass

    def format_sapche_anns(self):
        """
        Format the sapche annotations to the required format
        """
        pass

    def get_text_related_to_sapche(self):
        """
        Get the text related to the sapche annotations from meaning segment layer
        """
        pass

    def serialize(self, pecha_path: Path, title: str):
        """
        Serialize the commentary pecha to json format
        """
        self.extract_metadata(pecha_path)
        self.set_metadata_to_json(pecha_path)
        self.get_category(title)
        self.set_category_to_json()
        self.get_sapche_anns(pecha_path)
        self.format_sapche_anns()
        self.get_text_related_to_sapche()
        # serialize to json
        pass
