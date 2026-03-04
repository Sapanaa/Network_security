from network_security.components.data_ingestion import DataIngestion
from network_security.logging.logger import logging
import sys
from network_security.components.data_validation import DataValidation
from network_security.entity.config_entity import DataIngestionConfig, DataValidationConfig
from network_security.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    trainingpipelineConfig = TrainingPipelineConfig()
    data_ingestion_config = DataIngestionConfig(training_pipeline_config=trainingpipelineConfig)
    data_ingestion = DataIngestion(data_ingestion_config = data_ingestion_config)
    dataingestionartifact = data_ingestion.initiate_data_ingestion()
    logging.info("Data Ingestion Completed")
    data_validation_config = DataValidationConfig(training_pipeline_config=trainingpipelineConfig)
    data_validation = DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact=dataingestionartifact)
    logging.info("Initaite the data validation process")
    datavalidationartifact = data_validation.initiate_data_validation()
    logging.info("Data validation completed")