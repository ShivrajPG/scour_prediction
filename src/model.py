import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import os

def train_and_evaluate(data_path):
    """
    Load data, preprocess, train baseline Linear Regression and primary Random Forest models,
    and evaluate them.
    """
    df = pd.read_csv(data_path)
    
    # Define features and target
    features = ['Flow_Velocity_V', 'Pier_Diameter_D', 'Water_Depth_h', 'Grain_Size_d50']
    X = df[features]
    y = df['Experimental_Scour']
    
    # 80/20 train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Preprocessing: Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 1. Baseline Model: Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train_scaled, y_train)
    lr_preds = lr_model.predict(X_test_scaled)
    
    # Evaluate Linear Regression
    lr_r2 = r2_score(y_test, lr_preds)
    lr_mae = mean_absolute_error(y_test, lr_preds)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_preds))
    
    # 2. Primary Model: Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train_scaled, y_train)
    rf_preds = rf_model.predict(X_test_scaled)
    
    # Evaluate Random Forest
    rf_r2 = r2_score(y_test, rf_preds)
    rf_mae = mean_absolute_error(y_test, rf_preds)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))
    
    results = {
        'Linear Regression': {
            'R2': lr_r2,
            'MAE': lr_mae,
            'RMSE': lr_rmse
        },
        'Random Forest': {
            'R2': rf_r2,
            'MAE': rf_mae,
            'RMSE': rf_rmse
        }
    }
    
    # Save the models and scaler for interpretation phase
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(rf_model, os.path.join(output_dir, 'rf_model.pkl'))
    joblib.dump(lr_model, os.path.join(output_dir, 'lr_model.pkl'))
    joblib.dump(scaler, os.path.join(output_dir, 'scaler.pkl'))
    
    return rf_model, lr_model, scaler, X_test, y_test, results

if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'synthetic_scour_data.csv')
    rf, lr, scaler, X_test, y_test, results = train_and_evaluate(data_path)
    
    print("--- Model Evaluation Results ---")
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        print(f"  R2 Score : {metrics['R2']:.4f}")
        print(f"  MAE      : {metrics['MAE']:.4f}")
        print(f"  RMSE     : {metrics['RMSE']:.4f}")
