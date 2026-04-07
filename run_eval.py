from src.model import train_and_evaluate
import json
rf, lr, scaler, X_test, y_test, results = train_and_evaluate('data/synthetic_scour_data.csv')
with open('results.json', 'w') as f:
    json.dump(results, f, indent=4)
