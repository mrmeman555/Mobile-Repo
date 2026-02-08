# Role: Lead Research Engineer & Visualization Architect

**Objective:**
Expand the "Lithic Circuit" suite by adding **Module 5: The Global Network**. This module moves beyond the single-site analysis to verify the "Infrastructure" that connects them. You will verify the **Wireless Transmission** (Obelisks), the **Grounding Network** (Subsurface Grid), and the **Seasonal Activation** (Aquifer Pulse).

**Phase 1: Build the Physics Engine (`network_engine.py`)**

Create a new file `network_engine.py` to handle the physics for these new components.

**Class 1: `ObeliskTuner` (The Antenna)**
* **Physics:** Model the Obelisk as a **Tapered Cantilever Beam**.
* **Formula:** Use the Transverse Vibration equation for a tapered beam:
    * $f = \frac{1.875^2}{2\pi L^2} \sqrt{\frac{E \cdot I}{\rho \cdot A}}$ (Simplified for fundamental mode).
    * *Variables:*
        * $E$ (Young's Modulus): 60 GPa (Aswan Granite).
        * $\rho$ (Density): 2700 kg/m³.
        * $L$ (Height): Input (10m - 40m).
        * $W$ (Base Width): Input (1m - 4m).
* **Method `calculate_resonance(height, width)`:**
    * Return the Fundamental Frequency (Hz).
    * Check if it matches a Harmonic of Giza (117 Hz / 2, etc.).

**Class 2: `AquiferSwitch` (The Ground)**
* **Physics:** Model the electrical conductivity of the Alabaster/Water interface.
* **Logic:**
    * Input: `flood_level_meters` (0 - 10m).
    * Threshold: If `flood_level` > 7.0m (Floor Level), switch state = **CLOSED**.
    * Conductivity: If Wet, `sigma` = 0.5 S/m (Semiconductor). If Dry, `sigma` = 1e-12 (Insulator).

**Phase 2: Update the Dashboard (`app.py`)**

**1. Update Navigation:**
* Add **"🌍 Global Network (Active)"** to the Sidebar.

**2. Build the "Global Network" View:**
* **Tab 1: 📡 The Obelisk Tuner (Wireless)**
    * **Controls:** Sliders for Height (m) and Base Width (m).
    * **Metric:** "Natural Frequency".
    * **Visual (Plotly):** A 3D Cone/Pyramid representing the Obelisk.
        * *Interactive:* If the Calculated Freq is a harmonic of 117 Hz (+/- 1 Hz), make the Obelisk **GLOW GOLD**. If mistuned, color it **GREY**.

**Tab 2: 🏔️ Subsurface Tomography (The Roots)**
* **Context:** Visualizing the "Malanga Grid" (Granite pillars beneath Giza).
* **Visual (Plotly 3D Scatter/Mesh):**
    * Render a translucent Pyramid on top.
    * Render a **Red Grid** of vertical columns extending 50m underground.
    * Render a **Blue Plane** at -60m representing the Aquifer.
    * **Slider:** "Tomography Depth". As you slide deeper, hide the top layers to reveal the "Granite Roots."

**Tab 3: 🌊 The Aquifer Pulse (The Switch)**
* **Controls:** Slider "Nile Flood Level" (Low to High).
* **Visual (Plotly Area Chart):**
    * X-Axis: Season (Akhet, Peret, Shemu).
    * Y-Axis: Water Level.
    * **Animation:** Show the water level rising. When it hits the "Temple Floor" line:
        * Change annotation to **"CIRCUIT CLOSED: SYSTEM ONLINE"**.
        * Change color scheme to Green.

**Task 3: Forensic Data**
* Add all new calculations to the `full_report` JSON in the "Forensic Data Vault" tab.

**Execution:**
Create `network_engine.py` and update `app.py` to include this new multi-tab module. Ensure high-quality Plotly visualizations for the Obelisk and Subsurface views.