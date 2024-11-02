import sys
from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_extraction import DataExtraction
from src.components.data_analysis import DataAnalysis
from src.entity.artifact_entity import (
    DataIngestionArtifact,
    DataExtractionArtifact,
    DataAnalysisArtifact
)
from src.entity.config_entity import (
    DataIngestionConfig,
    DataExtractionConfig,
    DataAnalysisConfig
)


class ExecutePipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_extraction_config = DataExtractionConfig()
        self.data_analysis_config = DataAnalysisConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:

            logging.info("Starting data ingestion from pipeline..")
            dataingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = dataingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed in pipeline..")
            return data_ingestion_artifact
            
        except Exception as e:
            raise CustomException(e, sys)

    def start_data_extraction(
        self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataExtractionArtifact:
        try:
           
            logging.info("Starting data extraction from pipeline..")
            data_extraction = DataExtraction(
                data_ingestion_artifact, self.data_extraction_config
            )
            data_extraction_artifact = (
                data_extraction.initiate_data_extraction()
            )
            logging.info("Data extraction completed in pipeline..")
            return data_extraction_artifact
          

        except Exception as e:
            raise CustomException(e, sys)

    def start_data_analysis(
        self, 
        data_ingestion_artifact: DataIngestionArtifact,
        data_extraction_artifact: DataExtractionArtifact
    )-> DataAnalysisArtifact:
        try:

            logging.info("Starting data analysis from pipeline..")
            data_analysis = DataAnalysis(
                data_ingestion_artifact, data_extraction_artifact, self.data_analysis_config
            )
            data_analysis_artifact = data_analysis.initiate_data_analysis()
            logging.info("Data analysis completed in pipeline..")
            return data_analysis_artifact
            

        except Exception as e:
            raise CustomException(e, sys)

    def run_pipeline(self):
        try:
            logging.info("Running train pipeline...")
            data_ingestion_artifact = self.start_data_ingestion()
            data_extraction_artifact = self.start_data_extraction(
                data_ingestion_artifact
            )
            data_analysis_artifact = self.start_data_analysis(
                data_ingestion_artifact, 
                data_extraction_artifact
            )

            logging.info("Pipeline executed successfully..")
        except Exception as e:
            raise CustomException(e, sys)