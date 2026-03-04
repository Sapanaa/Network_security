# Network Security ML Pipeline 

This project implements an **end-to-end Machine Learning pipeline for network security threat detection**.
It includes **data processing, model training, API deployment, containerization, and CI/CD automation**.

The system predicts whether a network event is **malicious or safe** using a trained machine learning model.

---

##  Project Features

* End-to-end **Machine Learning pipeline**
* **Data ingestion and validation**
* **Data transformation and preprocessing**
* **Model training and evaluation**
* **FastAPI prediction API**
* **Docker containerization**
* **CI/CD pipeline with GitHub Actions**
* **Deployment using AWS**

---

##  Project Architecture

```
                Developer
                    │
                    │  git push
                    ▼
           GitHub Repository
        (source code & workflow)
                    │
                    ▼
        GitHub Actions CI/CD Pipeline
        ┌───────────────────────────┐
        │ Install dependencies      │
        │ Run lint checks           │
        │ Run tests                 │
        │ Build Docker image        │
        └───────────────┬───────────┘
                        │
                        ▼
               Docker Container Image
                        │
                        ▼
          Amazon Elastic Container Registry
                        │
                        ▼
                Self-hosted EC2 Runner
                        │
                        ▼
                 Docker Container
                        │
                        ▼
                 FastAPI Application
                        │
                        ▼
                    REST API
```

---

##  Machine Learning Pipeline

```
Dataset
   │
   ▼
Data Ingestion
   │
   ▼
Data Validation
   │
   ▼
Data Transformation
   │
   ▼
Model Training
   │
   ▼
Model Evaluation
   │
   ▼
Saved Model (.pkl)
   │
   ▼
FastAPI Prediction API
```

---

## 📂 Project Structure

```
network_security
│
├── network_security
│   ├── components
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   │
│   ├── pipeline
│   │   └── training_pipeline.py
│   │
│   ├── utils
│   │   └── utils.py
│   │
│   ├── entity
│   ├── exception
│   └── logging
│
├── templates
├── app.py
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

## 🚀 API Endpoints

### Home

```
GET /
```

Redirects to API documentation.

### Train Model

```
GET /train
```

Triggers the ML training pipeline.

### Predict

```
POST /predict
```

Upload a CSV file and receive predictions.

---

##  Docker

Build Docker image:

```
docker build -t network_security .
```

Run container:

```
docker run -p 8000:8000 network_security
```

---

##  CI/CD Pipeline

The project uses **GitHub Actions** for CI/CD automation.

Pipeline stages:

1. Install dependencies
2. Run lint checks
3. Run tests
4. Build Docker image
5. Push image to container registry
6. Deploy container

---

##  Example API Documentation

After running the application:

```
http://localhost:8000/docs
```

You will see the interactive **Swagger UI** for testing the API.

---

##  Technologies Used

* Python
* FastAPI
* Scikit-learn
* Docker
* GitHub Actions
* AWS

---

## 📸 Screenshots

Add screenshots here:

```
screenshots/pipeline_success.png
screenshots/api_docs.png
```


---

##  Author

Developed as part of a **Machine Learning / MLOps project** demonstrating:

* ML pipeline engineering
* API deployment
* Docker containerization
* CI/CD automation
