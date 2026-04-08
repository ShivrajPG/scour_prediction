# Parameter Logic Diagram

You can use or recreate this diagram in your presentation slides to visually explain to your professor how the 4 parameters are mathematically sufficient. 

This flowchart shows how the raw inputs map perfectly to the two major empirical theories (HEC-18 and Lacey's), proving that our AI has the complete mathematical blueprint to predict scour depth.

```mermaid
graph TD
    %% Input Parameters
    classDef input fill:#1e3a8a,stroke:#3b82f6,color:#fff,stroke-width:2px;
    classDef physics fill:#065f46,stroke:#10b981,color:#fff,stroke-width:2px;
    classDef theory fill:#7c2d12,stroke:#f97316,color:#fff,stroke-width:2px;
    classDef model fill:#4c1d95,stroke:#a855f7,color:#fff,stroke-width:3px;

    V("🌊 Flow Velocity (V)"):::input
    h("📏 Water Depth (h)"):::input
    D("🏛️ Pier Diameter (D)"):::input
    d50("🏖️ Grain Size (d50)"):::input

    %% Intermediate Physics Concepts
    Fr(("Froude Number<br>(Fr ≈ V / √gh)")):::physics
    q(("Discharge Intensity<br>(q ≈ V × h)")):::physics
    f(("Lacey's Silt Factor<br>(f ≈ √d50)")):::physics

    %% Connecting Inputs to Physics
    V --> Fr
    h --> Fr
    
    V --> q
    h --> q
    
    d50 --> f

    %% Connecting to Empirical Standards
    HEC18{"HEC-18 Equation<br>(International)"}:::theory
    Lacey{"Lacey's Regime Theory<br>(IRC:78-2014)"}:::theory

    Fr --> HEC18
    D --> HEC18
    h --> HEC18

    q --> Lacey
    f --> Lacey

    %% Machine Learning
    RF[["🧠 Random Forest AI Model"]]:::model

    HEC18 -. "Implicitly Learns" .-> RF
    Lacey -. "Implicitly Learns" .-> RF

    V ==> RF
    h ==> RF
    D ==> RF
    d50 ==> RF

    %% Final Output
    Output((("🎯 Predicted<br>Scour Depth"))):::input

    RF ===> Output
```

### How to explain this graphic:
1. Point to the **blue Input boxes** at the top. State that these are the only 4 parameters your model needs.
2. Point out how **Velocity (V)** and **Depth (h)** combine in fluid dynamics to form the Froude Number and Discharge Intensity.
3. Show how **Grain Size (d50)** entirely dictates the bed erodibility (Silt factor).
4. Explain that because the AI (purple block) receives all 4 raw inputs, it mathematically has the full capability to implicitly learn both the **HEC-18 standard** and **Lacey's Indian standard**.
