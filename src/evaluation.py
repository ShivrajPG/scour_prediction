import matplotlib.pyplot as plt
import numpy as np
import os

def create_interpretations(rf_model, lr_model, scaler, df, features):
    """
    Generate Feature Importance and Sensitivity Analysis plots.
    """
    out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Feature Importance (Random Forest)
    importances = rf_model.feature_importances_
    indices = np.argsort(importances)[::-1]
    sorted_features = [features[i] for i in indices]
    
    plt.figure(figsize=(10, 6))
    plt.bar(range(len(importances)), importances[indices])
    plt.xticks(range(len(importances)), sorted_features, rotation=15)
    plt.title('Random Forest Feature Importance')
    plt.ylabel('Relative Importance')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'feature_importance.png'))
    plt.close()
    
    # 2. Sensitivity Analysis (Varying Flow Velocity V)
    # Fix other variables at their mean
    means = df[features].mean().values
    v_idx = features.index('Flow_Velocity_V')
    
    # Generate 100 points of Velocity ranging from min to max
    v_values = np.linspace(df['Flow_Velocity_V'].min(), df['Flow_Velocity_V'].max(), 100)
    synthetic_samples = np.array([means]*100)
    synthetic_samples[:, v_idx] = v_values
    
    # Scale and predict
    synthetic_scaled = scaler.transform(synthetic_samples)
    rf_preds = rf_model.predict(synthetic_scaled)
    lr_preds = lr_model.predict(synthetic_scaled)
    
    plt.figure(figsize=(10, 6))
    plt.plot(v_values, rf_preds, label='Random Forest', linewidth=2)
    plt.plot(v_values, lr_preds, label='Linear Regression', linestyle='--', linewidth=2)
    plt.title('Sensitivity Analysis: Predicted Scour Depth vs Flow Velocity (V)')
    plt.xlabel('Flow Velocity (m/s)')
    plt.ylabel('Predicted Scour Depth (m)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'sensitivity_analysis.png'))
    plt.close()
