import os
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup
from src.logger import logging
from src.utils.utils import save_file
from src.exception import CustomException
from src.entity.config_entity import DataExtractionConfig
from src.entity.artifact_entity import DataIngestionArtifact, DataExtractionArtifact


class DataExtraction:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_extraction_config: DataExtractionConfig,
    ):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_extraction_config = data_extraction_config

    def extract_data(self, url):
        try:
            logging.info(f"Extracting the data from {url}")
            response = requests.get(url)
            content = response.content
            soup = BeautifulSoup(content, "html.parser")

            # Extract the title
            elements = soup.find_all(class_="td-post-title")
            elements = elements[0]
            article_title = (
                elements.find(class_="entry-title").get_text(strip=True)
                if elements.find(class_="entry-title")
                else ""
            )

            # Extract the article text
            article_text = soup.find_all(class_="td-post-content")[0].get_text(
                separator=" ", strip=True
            )
            split_phrases = ["project website url", "contact details"]

            # Function to split the text
            def split_text_by_phrases(text, phrases):
                for phrase in phrases:
                    if phrase in text:
                        parts = text.split(phrase, 1)
                        return parts[0].strip()
                return text

            article_text = split_text_by_phrases(article_text.lower(), split_phrases)
            article_content = article_title + " " + article_text
            article_content = article_content.lower()
            logging.info(f"Data extracted successfully from {url}")
            return article_content.strip()

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_extraction(self) -> DataExtractionArtifact:
        try:
            logging.info("Initiating data extraction")
            df = pd.read_csv(self.data_ingestion_artifact.data_file_path)
            rows = df.shape[0]
            os.makedirs(
                self.data_extraction_config.DATA_EXTRACTION_ARTIFACT_DIR, exist_ok=True
            )
            text_file_paths = []
            for i in range(rows):
                url = df.iloc[i]["URL"]
                text = self.extract_data(url)
                url_id = df.iloc[i]["URL_ID"]
                text_file = url_id + ".txt"
                text_file_path = os.path.join(
                    self.data_extraction_config.DATA_EXTRACTION_ARTIFACT_DIR, text_file
                )
                text_file_paths.append(text_file_path)
                save_file(file_path=text_file_path, text=text)
                print(f"Data extracted: {url_id} ID")

            data_extraction_artifact = DataExtractionArtifact(
                text_file_paths=text_file_paths
            )
            logging.info("Data extracted successfully")
            print(f"Data extracted successfully to {self.data_extraction_config.DATA_EXTRACTION_ARTIFACT_DIR}")
            return data_extraction_artifact

        except Exception as e:
            raise CustomException(e, sys)
