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
        # Use regex to split by spaces or newlines and keep the delimiters
        splited_strings = [x for x in re.split(r"([\s\n])", self.input) if x != ""]
        return {"raw_string": splited_strings}

    def chapter_parser_pipe(self):
        """
        input is self.data
        process is to group all the lines within the same chapter together
        output is to update self.data and by including the chapter information
        """
        chapter_number_regex = r"\Ach(\d+)-"
        chapter_name_regex = r"-\"([\u0F00-\u0FFF]+)\""

        char_count = 0
        previous_chapter_data = None  # Keep track of the previous chapter
        for i, input_line in enumerate(self.data["raw_string"]):
            if input_line in [" ", "\n"]:
                char_count += 1
                continue

            chapter_data = {}

            # Check for chapter number
            chapter_number_match = re.match(chapter_number_regex, input_line)
            if chapter_number_match:
                chapter_number = chapter_number_match.group(1)
                chapter_data["number"] = chapter_number

            # Check for chapter name
            chapter_name_match = re.search(chapter_name_regex, input_line)
            if chapter_name_match:
                chapter_name = chapter_name_match.group(1)
                chapter_data["name"] = chapter_name

            char_count += len(input_line)

            # Update input if chapter data is found
            if chapter_data:
                # Set index_start and char_start for the current chapter
                chapter_data["index_start"] = (
                    i + 2
                )  # Add two to skip chapter number and name
                chapter_data["char_start"] = (
                    char_count + 1
                )  # Add one to include the space character

                # If there's a previous chapter, update its index_end and char_end
                if previous_chapter_data:
                    previous_chapter_data["index_end"] = (
                        i - 1
                    )  # End at the line before the current chapter starts
                    previous_chapter_data["char_end"] = char_count - len(
                        input_line
                    )  # char_end just before current chapter starts

                # Append the new chapter data
                if "chapter" not in self.data:
                    self.data["chapter"] = [chapter_data]
                else:
                    self.data["chapter"].append(chapter_data)

                # Set current chapter as the previous for the next iteration
                previous_chapter_data = chapter_data

        # After the loop, update the last chapter's index_end and char_end to the end of the data
        if previous_chapter_data:
            previous_chapter_data["index_end"] = len(self.data["raw_string"]) - 1
            previous_chapter_data[
                "char_end"
            ] = char_count  # Final char count to the end of the text

        return self.data

    def tsawa_parser_pipe(self):
        """
        input is self.data
        process is to look inside and check for tsawa
        output is to update self.data and by including the tsawa information
        """
        char_count = 0

        index_start, char_start = 0, 0
        for i, input_line in enumerate(self.data["raw_string"]):
            if input_line in [" ", "\n"]:
                char_count += 1
                continue

            char_count += len(input_line)
            if i + 1 >= len(self.data["raw_string"]):
                continue

            if (
                self.data["raw_string"][i + 1] == "\n"
                and self.data["raw_string"][i + 2] == "\n"
            ):
                index_end = i
                char_end = char_count
                tsawa_data = {
                    "index_start": index_start,
                    "char_start": char_start,
                    "index_end": index_end,
                    "char_end": char_end,
                }
                if "tsawa" not in self.data:
                    self.data["tsawa"] = [tsawa_data]
                else:
                    self.data["tsawa"].append(tsawa_data)

                index_start = i + 3
                char_start = char_count + 2

        tsawa_data = {
            "index_start": index_start,
            "char_start": char_start,
            "index_end": len(self.data["raw_string"]) - 1,
            "char_end": char_count,
        }
        if "tsawa" not in self.data:
            self.data["tsawa"] = [tsawa_data]
        else:
            self.data["tsawa"].append(tsawa_data)

        return self.data
