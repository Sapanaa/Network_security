from network_security.entity.artifact_entity import ClassificationMetricArtifact
from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import sys
import numpy as np
import sklearn.metrics as metrics
from sklearn.metrics import f1_score, precision_score, recall_score

def get_classification_metric_score(test_y, y_pred)->ClassificationMetricArtifact:
    try:
        f1 = f1_score(test_y, y_pred)
        precision = precision_score(test_y, y_pred)
        recall = recall_score(test_y, y_pred)
        classification_metric = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e, sys)