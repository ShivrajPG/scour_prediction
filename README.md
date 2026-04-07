# Rapid Scour Depth Prediction AI

A machine learning pipeline and interactive web application designed to rapidly predict scour depth around coastal structures based on the intersection of established physical laws (Indian IRC:78-2014 & HEC-18) and modern Artificial Intelligence.

## Features
- **Synthetic Data Engine**: Generates physics-consistent coastal structural data.
- **Model Evaluation**: Implements and benchmarks Linear Regression against an optimized Random Forest algorithm.
- **Interpretability**: Generates analytical graphs for feature importance and velocity sensitivity scaling.
- **Interactive Full-Stack App**: A fully functioning Flask backend and glassmorphism HTML interface for real-time predictions.

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/your-username/scour_prediction.git
cd scour_prediction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### 1. The Interactive Web App (Recommended for Demos)
Run the Flask server which hosts the stunning interactive web dashboard:
```bash
python app.py
```
Then navigate to **http://127.0.0.1:5000** in your browser.

### 2. The Headless ML Pipeline
If you just want to generate new synthetic data, retrain the models, and generate new interpretability graphs strictly evaluating the metrics, you can run:
```bash
python main.py
```

## Project Structure
- `app.py`: The Flask server endpoints.
- `main.py`: The main orchestrator for headless pipeline evaluation.
- `src/`: Core Python modules for dataset generation, modeling, script, and evaluations.
- `web/`: Contains the front-end interactive UI (HTML/CSS/JS).
- `models/`: Saved `joblib` artifacts of the trained Random Forest and standard scaler.
- `data/`: Extracted synthetic CSV data.
- `output/`: Image artifacts of analysis graphs.
