import os
import sys


"""
Defining common constant variables for training pipeline.
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME = "network_security"
ARTIFACT_DIR = "artifact"
FILE_NAME = "network_security.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"




"""
DATA INGESTION related constants 
"""

DATA_INGESTION_COLLECTION_NAME = "NetworkData"
DATA_INGESTION_DATABASE_NAME = "NichoTJ"
DATA_INGESTION_DIR_NAME = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR = "feature_store"
DATA_INGESTION_INGESTED_DIR = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION = 0.2