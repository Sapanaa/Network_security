import os
import numpy as np
import pandas as pd
import sys
from network_security.exception.exception import NetworkSecurityException
from network_security.entity.artifact_entity import DataValidationArtifact, DataTransformationArtifact
from network_security.entity.config_entity import DataTransformationConfig
from sklearn.impute import KNNImputer
from network_security.logging.logger import logging
from sklearn.pipeline import Pipeline

from network_security.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS, TARGET_COLUMN
from network_security.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_transformation_config: DataTransformationConfig, data_validation_artifact: DataValidationArtifact):
        try:
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            # reading training and testing file
            train_file_path = self.data_validation_artifact.valid_train_file_path
            test_file_path = self.data_validation_artifact.valid_test_file_path
            
            # reading training and testing file
            train_df = pd.read_csv(train_file_path)
            test_df = pd.read_csv(test_file_path)
            
            # selecting input feature for training the model
            input_feature_train_df = train_df.drop(TARGET_COLUMN, axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            
            input_feature_test_df = test_df.drop(TARGET_COLUMN, axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            # imputing missing values
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            input_feature_train_arr = imputer.fit_transform(input_feature_train_df)
            input_feature_test_arr = imputer.transform(input_feature_test_df)

            # save numpy array data
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=input_feature_train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=input_feature_test_arr)

            # save object
            save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=imputer)
            save_object('final_model/preprocesser.pkl', imputer)
            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            return data_transformation_artifact

            logging.info("Exited initiate_data_transformation method of DataTransformation class")
        except Exception as e:
            raise NetworkSecurityException(e, sys)