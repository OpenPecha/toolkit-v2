import importlib
import inspect
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union

import toml
from pydantic import BaseModel, ConfigDict, Field, field_serializer, model_validator

from openpecha.ids import get_initial_pecha_id
from openpecha.pecha.parsers import BaseParser


class InitialCreationType(Enum):
    ocr = "ocr"
    ebook = "ebook"
    input = "input"
    tmx = "tmx"


class Language(Enum):
    tibetan = "bo"
    english = "en"
    chinese = "zh"
    sanskrit = "sa"


class CopyrightStatus(Enum):
    UNKNOWN = "Unknown"
    COPYRIGHTED = "In copyright"
    PUBLIC_DOMAIN = "Public domain"


class Copyright(BaseModel):
    status: CopyrightStatus = CopyrightStatus.UNKNOWN
    notice: Optional[str] = ""
    info_url: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


Copyright_copyrighted = Copyright(
    status=CopyrightStatus.COPYRIGHTED,
    notice="In copyright by the original author or editor",
    info_url="http://rightsstatements.org/vocab/InC/1.0/",
)

Copyright_unknown = Copyright(
    status=CopyrightStatus.UNKNOWN,
    notice="Copyright Undertermined",
    info_url="http://rightsstatements.org/vocab/UND/1.0/",
)

Copyright_public_domain = Copyright(
    status=CopyrightStatus.PUBLIC_DOMAIN,
    notice="Public domain",
    info_url="https://creativecommons.org/publicdomain/mark/1.0/",
)


class LicenseType(Enum):
    # based on https://creativecommons.org/licenses/

    CC0 = "CC0"
    PUBLIC_DOMAIN_MARK = "Public Domain Mark"
    CC_BY = "CC BY"
    CC_BY_SA = "CC BY-SA"
    CC_BY_ND = "CC BY-ND"
    CC_BY_NC = "CC BY-NC"
    CC_BY_NC_SA = "CC BY-NC-SA"
    CC_BY_NC_ND = "CC BY-NC-ND"

    UNDER_COPYRIGHT = "under copyright"
    UNKNOWN = "Unknown"


class PechaMetaData(BaseModel):
    id: str
    title: Optional[Union[List[str], Dict[str, str], str]] = None
    author: Optional[Union[List[str], Dict[str, str], str]] = None
    imported: Optional[datetime] = None
    source: Optional[str] = None
    toolkit_version: Optional[str] = None
    parser: str
    initial_creation_type: InitialCreationType
    language: Language
    source_metadata: Dict = {}
    bases: List[Dict] = []
    copyright: Copyright = Copyright()
    licence: LicenseType = LicenseType.UNKNOWN

    model_config = ConfigDict(extra="allow", arbitrary_types_allowed=True)

    @model_validator(mode="before")
    def set_id(cls, values):
        if "id" not in values or values["id"] is None:
            values["id"] = get_initial_pecha_id()
        return values

    @classmethod
    def get_toolkit_parsers(cls):
        # List to store all classes from the package
        all_classes = []
        import sys

        base_path = Path(__file__).parent / "parsers"
        pecha_parser_path = "openpecha.pecha.parsers"

        for py_file in base_path.rglob("*.py"):
            path_parts = list(py_file.parts)
            path_parts[-1] = path_parts[-1].replace(".py", "")
            if path_parts[-1] == "__init__":
                path_parts.pop()

            if path_parts[0] == "/":
                path_parts.pop(0)

            start_index = path_parts.index(pecha_parser_path.split(".")[0])
            parser_path = ".".join(path_parts[start_index:])
            importlib.import_module(parser_path)
            classes = inspect.getmembers(sys.modules[parser_path], inspect.isclass)
            all_classes.extend(classes)

        parser_classes = [
            (name, class_)
            for name, class_ in all_classes
            if issubclass(class_, BaseParser) and class_ is not BaseParser
        ]
        return parser_classes

    @model_validator(mode="before")
    def validate_parser(cls, values):
        parser_classes = cls.get_toolkit_parsers()
        if values["parser"] not in [name for name, _ in parser_classes]:
            raise ValueError(
                f"Parser {values['parser']} not found in the Toolkit parsers."
            )
        return values

    @model_validator(mode="before")
    def set_toolkit_version(cls, values):
        if "toolkit_version" not in values or values["toolkit_version"] is None:
            with open("pyproject.toml") as f:
                pyproject_data = toml.load(f)

            toolkit_version = pyproject_data["project"]["version"]
            values["toolkit_version"] = toolkit_version
        return values

    @model_validator(mode="before")
    def set_imported(cls, values):
        if "imported" not in values or values["imported"] is None:
            values["imported"] = datetime.now()
        return values

    # Custom serializers using field_serializer
    @field_serializer("imported", mode="plain")
    def serialize_imported(self, value: Optional[datetime]) -> Optional[str]:
        return value.isoformat() if value else None

    @field_serializer("licence", mode="plain")
    def serialize_licence(self, value: LicenseType) -> str:
        return value.value

    @field_serializer("language", mode="plain")
    def serialize_language(self, value: Language) -> str:
        return value.value

    @field_serializer("initial_creation_type", mode="plain")
    def serialize_inital_creation_type(self, value: InitialCreationType) -> str:
        return value.value

    @field_serializer("copyright", mode="plain")
    def serialize_copyright(self, value: Copyright) -> Dict:
        return {
            "status": value.status.value,
            "notice": value.notice,
            "info_url": value.info_url,
        }

    def to_dict(self):
        """
        Prepare PechaMetaData attribute to be JSON serializable
        """
        data = self.model_dump()

        # Dynamically get standard fields from the model
        standard_fields = list(set(self.model_fields.keys()))

        # Move any extra fields to source_metadata
        extra_fields = {}
        for k, v in data.items():
            if k not in standard_fields:
                if isinstance(v, Enum):
                    extra_fields[k] = v.value
                elif isinstance(v, datetime):
                    extra_fields[k] = v.isoformat()
                else:
                    extra_fields[k] = v

        data["source_metadata"].update(extra_fields)

        # Remove extra fields from the top-level data
        for field in extra_fields:
            del data[field]

        return data


class KungsangMonlamMetaData(BaseModel):
    author: Optional[Dict[str, str]] = Field(default_factory=dict)
    composition_date: Optional[Dict[str, str]] = Field(default_factory=dict)
    source: Optional[Dict[str, str]] = Field(default_factory=dict)
    presentation: Optional[Dict[str, str]] = Field(default_factory=dict)
    usage_title: Optional[Dict[str, str]] = Field(default_factory=dict)
    title_short: Optional[Dict[str, str]] = Field(default_factory=dict)
    title_long_clean: Optional[Dict[str, str]] = Field(default_factory=dict)
    title_alt_1: Optional[Dict[str, str]] = Field(default_factory=dict)
    title_alt_2: Optional[Dict[str, str]] = Field(default_factory=dict)
    is_commentary_of: Optional[Dict[str, str]] = Field(default_factory=dict)
    is_version_of: Optional[Dict[str, str]] = Field(default_factory=dict)
    lang: Optional[str] = None

    model_config = ConfigDict(extra="allow")

    def to_pecha_metadata(self, parser: str) -> PechaMetaData:
        """
        Extract relevant fields from KunsangMonlamMetaData and map them to PechaMetaData fields
        """
        title = self.title_short if self.title_short else {}
        author = self.author if self.author else []
        source = self.source if self.source else ""
        language = self.lang if self.lang else ""

        extra_metadata = {
            k: v
            for k, v in self.model_dump().items()
            if k not in ["author", "source", "source", "lang"]
        }

        return PechaMetaData(
            title=title,
            author=author,
            source=source,
            parser=parser,
            initial_creation_type=InitialCreationType.input,
            language=language,
            source_metadata={},
            **extra_metadata,
        )
