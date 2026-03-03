from dataclasses import dataclass
from network_security.exception.exception import NetworkSecurityException
import os, sys
from datetime import datetime

@dataclass()
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str