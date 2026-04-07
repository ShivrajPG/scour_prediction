import numpy as np
import pandas as pd
import os

def generate_synthetic_data(n_samples=300, random_state=42):
    """
    Generate synthetic data for ML-based scour prediction.
    Features: Flow velocity (V), Pier diameter (D), Water depth (h), Grain size (d50)
    Targets are generated based on Lacey's theory and HEC-18 equations with added noise.
    """
    np.random.seed(random_state)
    
    # Generate random features
    # Velocity (m/s)
    V = np.random.uniform(0.5, 4.0, n_samples)
    # Pier Diameter (m)
    D = np.random.uniform(0.5, 3.0, n_samples)
    # Water Depth (m)
    h = np.random.uniform(1.0, 10.0, n_samples)
    # Grain Size (mm)
    d50 = np.random.uniform(0.1, 5.0, n_samples)

    # 1. Lacey's Scour Depth (Indian Practice: IRC:78-2014)
    # Silt factor f = 1.76 * sqrt(d50) where d50 is in mm
    f = 1.76 * np.sqrt(d50)
    # Discharge intensity q = V * h (approx for wide channel)
    q = V * h
    # Lacey's normal scour depth d = 1.34 * (q^2 / f)^(1/3)
    d_lacey = 1.34 * np.power((q**2 / f), 1/3)
    # Design scour for piers = 2.0 * d
    pier_scour_lacey = 2.0 * d_lacey

    # 2. HEC-18 Equation (International Practice)
    # Fr = V / sqrt(g * h), g = 9.81
    g = 9.81
    Fr = V / np.sqrt(g * h)
    # Assuming K1, K2, K3 = 1.0 for standard pier/flow conditions
    K1, K2, K3 = 1.0, 1.0, 1.0
    pier_scour_hec18 = D * 2.0 * K1 * K2 * K3 * np.power((h/D), 0.35) * np.power(Fr, 0.43)

    # 3. Create synthetic "Experimental" Scour Depth
    # We combine both to ensure Scour depends on all features (D from HEC, d50 from Lacey)
    # and add Gaussian noise to simulate experimental error.
    noise = np.random.normal(0, 0.15, n_samples)
    # Weighted average logic: 60% HEC-18 (better includes D) + 40% Lacey (includes d50)
    scour_experimental = 0.6 * pier_scour_hec18 + 0.4 * pier_scour_lacey + noise
    # Ensure no negative scour values
    scour_experimental = np.maximum(scour_experimental, 0.1)

    # Create DataFrame
    df = pd.DataFrame({
        'Flow_Velocity_V': V,
        'Pier_Diameter_D': D,
        'Water_Depth_h': h,
        'Grain_Size_d50': d50,
        'Froude_Number': Fr,               # Derived feature computed for ML
        'Lacey_Scour': pier_scour_lacey,   # For reference
        'HEC18_Scour': pier_scour_hec18,   # For reference
        'Experimental_Scour': scour_experimental # Target variable for ML
    })
    
    return df

if __name__ == "__main__":
    df = generate_synthetic_data(300)
    
    # Save to data directory
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, 'synthetic_scour_data.csv')
    df.to_csv(out_path, index=False)
    
    print(f"Generated {len(df)} synthetic data points and saved to {os.path.abspath(out_path)}")
    print(df.head())
