# Project Documentation: 2D Heat Diffusion in Bi-Materials

## 1. Project Overview

This project implements a numerical simulation of transient heat transfer through a composite material plate (Copper and Steel). The simulation utilizes the **Finite Difference Method (FDM)** to solve the heat equation in a 2D spatial domain.

The primary goal is to demonstrate:

* Application of numerical methods to physical problems.
* Efficient computation using **NumPy vectorization**.
* Handling of diverse boundary conditions (Dirichlet and Neumann).

## 2. Theoretical Background

The simulation is governed by the 2D Heat Equation:


### Thermal Diffusivity ()

Instead of using arbitrary constants, this simulation uses the physical **Thermal Diffusivity** of real materials, defined as .

| Material | Region | Diffusivity () | Characteristics |
| --- | --- | --- | --- |
| **Copper** | Left Half | 0.116 | High thermal conductivity; rapid heat spread. |
| **Steel** | Right Half | 0.013 | Lower conductivity; acts as a thermal barrier. |

## 3. Implementation Methodology

### Numerical Solver: Vectorized Slicing

To ensure high performance, the code avoids Python `for` loops for spatial updates. Instead, it uses **NumPy array slicing** to calculate the 5-point stencil (Laplacian) across the entire grid simultaneously:

```python
interior = plate[1:-1, 1:-1]
up, down = plate[0:-2, 1:-1], plate[2:, 1:-1]
left, right = plate[1:-1, 0:-2], plate[1:-1, 2:]

# Laplacian Update
plate[1:-1, 1:-1] += alpha_map[1:-1, 1:-1] * (up + down + left + right - 4*interior)

```

### Boundary Conditions

* **Dirichlet (Heater):** The left edge is fixed at a constant .
* **Neumann (Insulation):** The top, bottom, and right edges are perfectly insulated (Zero Flux), achieved by equating edge pixels to their interior neighbors: `plate[:, -1] = plate[:, -2]`.

## 4. Visual Results and Analysis

The resulting heatmap illustrates a sharp change in the temperature gradient at the material interface ().

1. **Copper Zone:** Shows a smooth, deep penetration of heat.
2. **Steel Zone:** Shows a rapid drop in temperature, confirming its role as an insulator.
3. **Steady State:** Over time, the system approaches a linear temperature profile, modified by the differing thermal resistances of the two materials.

## 5. How to Run the Simulation

1. **Environment:** Python 3.x with a Virtual Environment (`venv`).
2. **Dependencies:** `pip install numpy matplotlib`.
3. **Execution:** Run the script to generate the `Heat_Diffusion_BiMaterial.pdf` report and the on-screen heatmap.

---
