from network_security.exception.exception import NetworkSecurityException
from network_security.logging.logger import logging
import os
import sys

from sklearn.metrics import f1_score, precision_score, recall_score
from network_security.utils.main_utils.utils import (
    save_object,
    load_object,
    load_numpy_array_data,
)
from network_security.utils.ml_utils.metric.classification_metric import (
    get_classification_metric_score,
)
from network_security.entity.config_entity import ModelTrainerConfig
from network_security.entity.artifact_entity import ModelTrainerArtifact
from network_security.entity.artifact_entity import DataTransformationArtifact
from network_security.utils.ml_utils.model.estimator import NetworkModel
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import AdaBoostClassifier
from network_security.utils.main_utils.utils import evaluate_models
import mlflow


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModelTrainerConfig,
        data_transformation_artifact: DataTransformationArtifact,
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, best_model, train_metric, test_metric):
        mlflow.set_tracking_uri(uri="http://127.0.0.1:5000")
        mlflow.set_experiment("network_security_training")

        with mlflow.start_run(run_name=f"{best_model.__class__.__name__}_training"):

            mlflow.log_metrics(
                {
                    "train_f1": train_metric.f1_score,
                    "train_precision": train_metric.precision_score,
                    "train_recall": train_metric.recall_score,
                    "test_f1": test_metric.f1_score,
                    "test_precision": test_metric.precision_score,
                    "test_recall": test_metric.recall_score,
                }
            )

            mlflow.log_param("model_name", best_model.__class__.__name__)

            mlflow.sklearn.log_model(sk_model=best_model, artifact_path="model")

            logging.info("Model and metrics successfully logged to MLflow")

    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boost": GradientBoostingClassifier(),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost Classifier": AdaBoostClassifier(),
        }
        params_grid = {
            "Decision Tree": {
                "criterion": ["gini", "entropy"],
                "max_depth": [2, 3, 4],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
            },
            "Random Forest": {
                "n_estimators": [50, 100, 200, 300],
                "max_depth": [None, 10, 20, 30],
                "min_samples_split": [2, 5, 10],
                "class_weight": ["balanced", None],
            },
            "Gradient Boost": {
                "learning_rate": [0.1, 0.01, 0.05],
                "n_estimators": [8, 16, 32],
                "max_depth": [2, 3, 4],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
            },
            "Logistic Regression": {},
            "AdaBoost Classifier": {
                "n_estimators": [8, 16, 32],
                "learning_rate": [0.1, 0.01, 0.05],
            },
        }
        model_report: dict = evaluate_models(
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test,
            models=models,
            params=params_grid,
        )

        best_model_score = max(sorted(model_report.values()))
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]

        classification_train_metric = get_classification_metric_score(
            y_train, best_model.predict(X_train)
        )

        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classification_metric_score(
            y_test, y_test_pred
        )

        ## tracking the experiments in mlflow

        self.track_mlflow(
            best_model, classification_train_metric, classification_test_metric
        )

        preprocesser = load_object(
            file_path=self.data_transformation_artifact.transformed_object_file_path
        )

        model_dir_path = os.path.dirname(
            self.model_trainer_config.trained_model_file_path
        )
        os.makedirs(model_dir_path, exist_ok=True)

        network_model = NetworkModel(preprocesser, best_model)
        save_object(
            file_path=self.model_trainer_config.trained_model_file_path,
            obj=network_model,
        )

        logging.info(f"Best model selected: {best_model_name}")
        logging.info(f"Best model validation score: {best_model_score}")
        save_object("final_model/model.pkl", best_model)
        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric,
        )
        logging.info("Exited initiate_model_trainer method of ModelTrainer class")
        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:

            logging.info("Entered initiate_model_trainer method of ModelTrainer class")
            transformed_train_file_path = (
                self.data_transformation_artifact.transformed_train_file_path
            )
            transformed_test_file_path = (
                self.data_transformation_artifact.transformed_test_file_path
            )

            train_array = load_numpy_array_data(file_path=transformed_train_file_path)
            test_array = load_numpy_array_data(file_path=transformed_test_file_path)

            X_train, y_train = train_array[:, :-1], train_array[:, -1]
            X_test, y_test = test_array[:, :-1], test_array[:, -1]

            model_trainer_artifact = self.train_model(
                X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test
            )

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
