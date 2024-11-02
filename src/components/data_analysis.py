import os
import sys
from src.logger import logging
import pandas as pd
from src.exception import CustomException
from src.utils.utils import (
    read_file,
    stopwords,
    positive_words,
    negative_words,
    polarity_score,
    subjectivity_score,
    get_input_val,
    save_excel,
)
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataExtractionArtifact,
    DataAnalysisArtifact,
)
from src.entity.config_entity import DataAnalysisConfig
from src.analysis.text_analysis import analyze_readability


class DataAnalysis:
    def __init__(
        self,
        data_ingestion_artifact: DataIngestionArtifact,
        data_extraction_artifact: DataExtractionArtifact,
        data_analysis_config: DataAnalysisConfig,
    ):
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_extraction_artifact = data_extraction_artifact
        self.data_analysis_config = data_analysis_config

    def remove_stopwords(self, text, stopwordlist):
        try:
            text_list = text.lower().split()
            text_list_clean = [item for item in text_list if item not in stopwordlist]
            return text_list_clean
        except Exception as e:
            raise CustomException(e, sys)

    def positive_score(self, text_list, positive_words_list):
        try:
            logging.info("Creating positive words dictionay")
            positive_list = []
            for text in text_list:
                if text in positive_words_list:
                    positive_list.append(text)
            logging.info("Positive words dictionary created successfully")
            
            return positive_list

        except Exception as e:
            raise CustomException(e, sys)

    def negative_score(self, text_list, negative_words_list):
        try:
            logging.info("Creating negative words dictionay")
            negative_list = []
            for text in text_list:
                if text in negative_words_list:
                    negative_list.append(text)
            logging.info("Negative words dictionary created successfully")

            return negative_list

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_analysis(self):
        try:
            logging.info("Initiating data analysis")
            text_file_paths = self.data_extraction_artifact.text_file_paths
            df = pd.read_csv(self.data_ingestion_artifact.data_file_path)
            stopwords_list = stopwords()
            positive_words_list = positive_words()
            negative_words_list = negative_words()
            data = []
            for text_file_path in text_file_paths:
                text = read_file(file_path=text_file_path)
                text_list_clean = self.remove_stopwords(text, stopwords_list)
                total_words_length = len(text_list_clean)
                positive_dict = self.positive_score(
                    text_list_clean, positive_words_list
                )
                negative_dict = self.negative_score(
                    text_list_clean, negative_words_list
                )
                pos_score = len(positive_dict)
                neg_score = len(negative_dict)
                polar_score = polarity_score(pos_score, neg_score)
                sub_score = subjectivity_score(pos_score, neg_score, total_words_length)
                text_str_clean = " ".join(text_list_clean)
                readability_analysis = analyze_readability(text_str_clean)
                url_id, url = get_input_val(df, text_file_path)
                data_point = {
                    "URL_ID": url_id,
                    "URL": url,
                    "POSITIVE SCORE": pos_score,
                    "NEGATIVE SCORE": neg_score,
                    "POLARITY SCORE": polar_score,
                    "SUBJECTIVITY SCORE": sub_score,
                    "AVG SENTENCE LENGTH": readability_analysis[
                        "Average Sentence Length"
                    ],
                    "PERCENTAGE OF COMPLEX WORDS": readability_analysis[
                        "Percentage of Complex Words"
                    ],
                    "FOG INDEX": readability_analysis["Fog Index"],
                    "AVG NUMBER OF WORDS PER SENTENCE": readability_analysis[
                        "Average Number of Words per Sentence"
                    ],
                    "COMPLEX WORD COUNT": readability_analysis[
                        "Number of Complex Words"
                    ],
                    "WORD COUNT": readability_analysis["Word Counts"],
                    "SYLLABLE PER WORD": readability_analysis["Syllable per Word"],
                    "PERSONAL PRONOUNS": readability_analysis["Personal Pronouns"],
                    "AVG WORD LENGTH": readability_analysis["Average Word Length"],
                }
                print(f"Data Analyzed URL_ID: {url_id}")
                data.append(data_point)

            print("Data Analysis completed")
            os.makedirs(self.data_analysis_config.DATA_ANALYSIS_ARTIFACT_DIR, exist_ok=True)
            save_excel(data, self.data_analysis_config.OUTPUT_FILE_PATH)
            print(
                f"Output file is saved into {self.data_analysis_config.OUTPUT_FILE_PATH}"
            )

            data_analysis_artifact = DataAnalysisArtifact(
                self.data_analysis_config.OUTPUT_FILE_PATH
            )
            logging.info("Data Analysis completed")
            return data_analysis_artifact

        except Exception as e:
            raise CustomException(e, sys)
