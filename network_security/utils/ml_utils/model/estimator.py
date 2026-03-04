from network_security.entity.artifact_entity import ClassificationMetricArtifact
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging

import os
import sys
from network_security.constants.training_pipeline import SAVE_MODEL_DIR, MODEL_FILE_NAME


class NetworkModel:
    def __init__(self, preprocessor, model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_pred = self.model.predict(x_transform)
            return y_pred
        except Exception as e:
            raise NetworkSecurityException(e, sys)
