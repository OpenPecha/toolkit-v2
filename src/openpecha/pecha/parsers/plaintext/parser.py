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
                getattr(self, pipe)(self.data)
            else:
                pipe(self.data)

    def preprocess(self) -> List[str]:
        """split the text into atomic units with newline"""
        return self.input.split("\n")

    def chapter_parser_pipe(self, input: List[Dict]):
        """
        input is self.data
        process is to group all the lines within the same chapter together
        output is to update self.data and by including the chapter information
        """

        pass

    def tsawa_parser_pipe(self, input: List[Dict]):
        """
        Dependency: This pipe requires the chapter parser pipe already has been ran

        input is self.data with chapter information
        process is to look inside every chapter and tag the chapter title
        output is to update self.data and by including the tsawa information
        """
        pass

    def tsikhang_parser_pipe(self, input: List[Dict]):
        """
        Dependency: This pipe requires the chapter tsawa parser pipe already has been ran

        input is self.data with chapter information and chapter title information
        process is to look inside the content of each chapter ignoring the title and split into tsikhang
        output is to update self.data and by including the tsikhang information
        """
        pass
