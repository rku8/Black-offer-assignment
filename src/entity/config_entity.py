import os
from src.constants import *
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    DATA_INGESTION_ARTIFACT_DIR = os.path.join(
        ARTIFACT_DIR, DATA_INGESTION_ARTIFACT_DIR
    )
    DATA_FILE_PATH = os.path.join(DATA_INGESTION_ARTIFACT_DIR, DATA_FILE_NAME)

@dataclass
class DataExtractionConfig:
    DATA_EXTRACTION_ARTIFACT_DIR = os.path.join(
        ARTIFACT_DIR, DATA_EXTRACTION_ARTIFACT_DIR
    )

@dataclass
class DataAnalysisConfig:
    DATA_ANALYSIS_ARTIFACT_DIR = os.path.join(ARTIFACT_DIR, DATA_ANALYSIS_ARTIFACT_DIR)
    OUTPUT_FILE_PATH = os.path.join(DATA_ANALYSIS_ARTIFACT_DIR, OUTPUT_FILE)
