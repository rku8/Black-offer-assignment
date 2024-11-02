from dataclasses import dataclass
from typing import List

@dataclass
class DataIngestionArtifact:
    data_file_path: str


@dataclass
class DataExtractionArtifact:
    text_file_paths: List[str]


@dataclass
class DataAnalysisArtifact:
    output_file_path: str
   