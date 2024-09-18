import re
from typing import Dict, List


class PechaFrameWork:
    def __init__(self, input: str, metadata: Dict = None):
        self.input = input
        self.meta_data = {} if not metadata else metadata
        self.data = self.preprocess()
        self.output = None

    def serialize_json(self):
        pipeline_definition = ["pecha_publish_serializer_pipe"]
        self.serializer_pipeline(pipeline_definition)

    def parse_text(self):
        pipeline_defination = [
            "chapter_parser_pipe",
            "tsawa_parser_pipe",
            "tsikhang_parser_pipe",
        ]
        self.parser_pipeline(pipeline_defination)

    def pecha_human_check_serializer_pipe(self):
        """
        input is self.data
        process is to export data in docx format
        """

        pass

    def pecha_publish_serializer_pipe(self):
        """
        input is self.data
        process is to export data in json format to be published on website
        """
        pass

    def serializer_pipeline(self, pipelist: List):
        """
        reads the list of pipes and runs them in sequence
        if a pipe is a string, call built-in pipe,
        if it is a function, call the function
        """
        pass

    def parser_pipeline(self, pipelist: List):
        """
        reads the list of pipes and runs them in sequence
        if a pipe is a string, call built-in pipe,
        if it is a function, call the function
        """
        for pipe in pipelist:
            if isinstance(pipe, str):
                getattr(self, pipe)()
            else:
                pipe(self.data)

    def preprocess(self) -> Dict:
        """split the text into atomic units with newline"""
        return {"raw_string": self.input.split("\n")}

    def chapter_parser_pipe(self):
        """
        input is self.data
        process is to group all the lines within the same chapter together
        output is to update self.data and by including the chapter information
        """
        chapter_number_regex = r"\Ach(\d+)-"
        chapter_name_regex = r"-\"([\u0F00-\u0FFF]+)\""

        for i, input_line in enumerate(self.data["raw_string"]):
            chapter_data = {}

            # Check for chapter number
            chapter_number_match = re.match(chapter_number_regex, input_line)
            if chapter_number_match:
                chapter_number = chapter_number_match.group(1)
                chapter_data["chapter_number"] = chapter_number

            # Check for chapter name
            chapter_name_match = re.search(chapter_name_regex, input_line)
            if chapter_name_match:
                chapter_name = chapter_name_match.group(1)
                chapter_data["chapter_name"] = chapter_name

            # Update input if chapter data is found
            if chapter_data:
                chapter_data["start_index"] = i
                if "chapter" not in self.data:
                    self.data["chapter"] = [chapter_data]
                else:
                    self.data["chapter"].append(chapter_data)

        return input

    def tsawa_parser_pipe(self):
        """
        Dependency: This pipe requires the chapter parser pipe already has been ran

        input is self.data with chapter information
        process is to look inside every chapter and tag the chapter title
        output is to update self.data and by including the tsawa information
        """
        pass

    def tsikhang_parser_pipe(self):
        """
        Dependency: This pipe requires the chapter tsawa parser pipe already has been ran

        input is self.data with chapter information and chapter title information
        process is to look inside the content of each chapter ignoring the title and split into tsikhang
        output is to update self.data and by including the tsikhang information
        """
        pass
