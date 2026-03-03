from network_security.components.data_ingestion import DataIngestion
from network_security.logging.logger import logging
import sys
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    trainingpipelineConfig = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=trainingpipelineConfig)
    data_ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
    dataingestionartifact = data_ingestion.initiate_data_ingestion()
    print(dataingestionartifact)