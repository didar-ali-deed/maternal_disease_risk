# Maternal Disease Risk Prediction API

A machine learning-powered REST API for predicting maternal health risk levels using patient health indicators. Built with Python, Scikit-learn, and FastAPI, the project provides a structured backend for loading a trained model and generating predictions.

## Project Overview

Maternal health risk assessment is an important part of identifying potential complications during pregnancy.

This project uses a machine learning classification model trained on maternal health data to predict risk categories based on patient health parameters.

The API exposes prediction endpoints through FastAPI and uses Pydantic schemas for request validation.

## Features

- Machine learning-based maternal health risk classification.
- Trained model persistence using Pickle.
- FastAPI backend for RESTful predictions.
- Pydantic-based input validation.
- Separate training, prediction, and model-loading modules.
- Model evaluation metrics stored in JSON format.
- Interactive API documentation through Swagger UI.

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| API Framework | FastAPI |
| ML Framework | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Model Serialization | Pickle |
| Data Validation | Pydantic |
| ASGI Server | Uvicorn |

## Project Structure

```text
maternal_disease/
│
├── backend/
│   ├── load_model.py
│   ├── main.py
│   ├── predictor.py
│   └── schemas.py
│
├── data/
│   ├── download_data.py
│   └── maternal_risk.csv
│
├── models/
│   ├── metrics.json
│   └── model.pkl
│
├── training/
│   ├── load_data.py
│   └── train.py
│
├── tests/
│
├── .gitignore
├── requirements.txt
└── README.md
```

## Dataset

The project uses a maternal health risk dataset containing clinical indicators associated with pregnancy.

The dataset includes the following features:

| Feature | Description |
|---|---|
| Age | Age of the patient |
| SystolicBP | Systolic blood pressure |
| DiastolicBP | Diastolic blood pressure |
| BS | Blood sugar level |
| BodyTemp | Body temperature |
| HeartRate | Heart rate |

**Target variable:** RiskLevel

The classification target contains three categories:

- Low Risk
- Mid Risk
- High Risk

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/didar-ali-deed/maternal_disease_risk
cd maternal_disease
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

On Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Model Training

To train the machine learning model, execute:

```bash
python -m training.train
```

The trained model and evaluation metrics are stored in the `models/` directory.

## Running the API

Start the FastAPI application from the project root:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### API Documentation

FastAPI automatically generates interactive API documentation.

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## Prediction Workflow

1. Patient health parameters are submitted through an API request.
2. Pydantic validates the incoming data.
3. The prediction module processes the input.
4. The trained machine learning model generates a risk classification.
5. The API returns the prediction as a JSON response.

## Model Evaluation

Evaluation metrics are maintained in:

```text
models/metrics.json
```

The model's performance should be assessed using appropriate classification metrics, including:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

Refer to the evaluation metrics generated during model training for actual performance results.

## Disclaimer

This project is intended for educational and research purposes only.

It is not a clinically validated diagnostic system and must not be used as a substitute for professional medical advice, diagnosis, or treatment. Maternal health decisions should always involve qualified healthcare professionals.

## Author

**Didar Ali**

- GitHub: https://github.com/didar-ali-deed
- Portfolio: https://didar-ali.vercel.app
- LinkedIn: https://linkedin.com/in/didar-ali-deed

---

*Developed as a machine learning project focused on maternal health risk prediction.*
