# read data from store create the features store and separate the data into train and test and save it

from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging


#config file for the Data Ingestion Cofig
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import pymongo
from sklearn.model_selection import train_test_split
import pandas as pd


from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def export_collection_as_dataframe(self):
        try:
            logging.info("Exporting collection as dataframe")
            database = self.data_ingestion_config.database_name
            collection = self.data_ingestion_config.collection_name

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            
            collection = self.mongo_client[database][collection]

            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop("_id", axis=1)
            return df
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        

    def export_data_to_feature_store(self, dataframe: pd.DataFrame):
        try:
            logging.info("Exporting data to feature store")
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def split_train_test(self, dataframe: pd.DataFrame):
        try:
            logging.info("Splitting data into train and test")
            train, test = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio, random_state=42)
            dir_path = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train.to_csv(self.data_ingestion_config.train_file_path, index=False, header=True)

            dir_path = os.path.dirname(self.data_ingestion_config.test_file_path)
            os.makedirs(dir_path, exist_ok=True)
            test.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
            self.split_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file_path,
                test_file_path=self.data_ingestion_config.test_file_path,
            )
            return dataingestionartifact
        

        except Exception as e:
            raise NetworkSecurityException(e, sys)