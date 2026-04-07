from src.dataset import generate_synthetic_data
from src.model import train_and_evaluate
from src.evaluation import create_interpretations
import os

if __name__ == "__main__":
    print("1. Generating Synthetic Data (100-300 points)...")
    # Generates 300 data points via Lacey's & HEC-18
    df = generate_synthetic_data(300)
    
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(output_dir, exist_ok=True)
    data_path = os.path.join(output_dir, 'synthetic_scour_data.csv')
    df.to_csv(data_path, index=False)
    print(f"Data generated and saved to {data_path}")
    
    print("\n2. Training ML Models...")
    # Features used: Velocity, Diameter, Depth, Grain Size
    features = ['Flow_Velocity_V', 'Pier_Diameter_D', 'Water_Depth_h', 'Grain_Size_d50']
    rf_model, lr_model, scaler, X_test, y_test, results = train_and_evaluate(data_path)
    
    print("\n--- Model Evaluation Results (Test Set) ---")
    for model_name, metrics in results.items():
        print(f"{model_name}:")
        print(f"  R2 Score : {metrics['R2']:.4f}")
        print(f"  MAE      : {metrics['MAE']:.4f}")
        print(f"  RMSE     : {metrics['RMSE']:.4f}")

    print("\n3. Generating Interpretations (Feature Importance & Sensitivity)...")
    create_interpretations(rf_model, lr_model, scaler, df, features)
    
    print("Done! Check 'output' directory for generated plots.")
