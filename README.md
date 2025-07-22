# Fraud Detection Deployment

This project is an MLOps-based Fraud Detection system that leverages Machine Learning to identify fraudulent transactions. The solution is designed for robust deployment, monitoring, and scalability using modern DevOps practices.

## Features
- **Machine Learning Model**: Trained to detect fraudulent transactions.
- **API Service**: Flask-based API for model inference.
- **Streamlit App**: User-friendly interface for interacting with the model.
- **Data Processing**: Automated data cleaning and feature engineering.
- **Dockerized Deployment**: Easily deployable using Docker and Docker Compose.
- **MLOps Workflow**: Supports continuous integration and deployment.

## Project Structure
```
app/
  dataProcess.py         # Data processing and feature engineering
  flask_api.py           # Flask API for model inference
  main.py                # Main entry point
  model.pkl              # Trained ML model
  output.csv             # Sample output data
  requirements.txt       # Python dependencies
  streamlit_app.py       # Streamlit web app
Dockerfile               # Docker image definition
requirements.txt         # Project dependencies
```

## Getting Started

### Prerequisites
- Docker
- Docker Compose
- Python 3.11 (for local development)

### Build and Run with Docker Compose
```bash
docker-compose up --build
```

### Accessing the Services
- **Flask API**: http://localhost:5000
- **Streamlit App**: http://localhost:8501

## Usage
- Use the Streamlit app to upload transaction data and get fraud predictions.
- Integrate with the Flask API for programmatic access.

## MLOps Practices
- Containerized deployment for consistency across environments.
- Modular codebase for easy updates and maintenance.
- Ready for CI/CD integration.

## License
This project is licensed under the MIT License.
