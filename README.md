# Network Intrusion Detection – MLOps Pipeline

**End-to-end machine learning pipeline for classifying network events as malicious or benign**  
Built with modular components, artifact tracking, FastAPI serving, Docker, and CI/CD readiness for cloud deployment (AWS/Azure).


## 🎯 Problem & Business Value

In modern cybersecurity, detecting threats in high-volume network traffic is critical.  
This project delivers:
- Automated data ingestion from MongoDB
- Feature engineering & validation
- Multi-model training & evaluation
- Production-ready prediction API
- Containerized deployment & CI/CD
- Cloud push option (AWS/Azure) for production models

Reduces manual effort, improves reproducibility, and enables continuous retraining when drift occurs.

## 🏗 Machine Learning Pipeline Architecture

The system follows a production-grade flow:

<p align="center">
  <img src="screenshots/architecture.png.png" alt="Machine learning Pipeline Flow" width="1000"/>
  <br/>
  <em>Click to enlarge </em>
</p>

**Key flow**:
1. **Data Ingestion** ← MongoDB → DataIngestionArtifact
2. **Validation** → checks schema, drift, completeness
3. **Transformation** → feature engineering, scaling → TransformationArtifact
4. **Model Training** → multiple algorithms + hyperparams → TrainerArtifact
5. **Evaluation** → metrics → decide if model is accepted
6. **Push** → if accepted → upload to cloud (AWS/Azure)

## 🔍 Component Breakdown

Each stage is independent and configurable:

| Stage                | Component File              | Key Responsibility                          | Output Artifact                  |
|----------------------|-----------------------------|---------------------------------------------|----------------------------------|
| Ingestion            | `data_ingestion.py`         | Read from MongoDB                           | Raw dataset artifact             |
| Validation           | `data_validation.py`        | Schema check, drift detection               | Validation report                |
| Transformation       | `data_transformation.py`    | Preprocessing, feature creation             | Transformed train/test files     |
| Training             | `model_trainer.py`          | Multi-model training + selection            | Trained model + metrics          |
| Evaluation           | (integrated in trainer)     | Compare models, select best                 | Evaluation artifact              |
| Push (optional)      | `model_pusher.py`           | Upload to cloud if accepted                 | Cloud model location             |

## 🚀 Quick Start (Local)

```bash
# Clone & enter
git clone https://github.com/your/network-security.git
cd network-security

# Virtual env
python -m venv .venv
.venv\Scripts\activate  # Windows

# Install
pip install -e ".[dev]"

# Run API
uvicorn app:app --reload --port 8000

# Open docs
http://localhost:8000/docs


## 🐳 Docker + Deployment

Containerize the application for consistent, portable deployment across environments.

### Build & Run Locally

```bash
# Build the Docker image
docker build -t network-security:latest .

# Run the container (maps port 8000)
docker run -p 8000:8000 --name ns-predictor network-security:latest