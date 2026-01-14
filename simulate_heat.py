import numpy as np
import matplotlib.pyplot as plt

# --- 1. SETUP ---
N = 100               # Grid size (100x100)
timesteps = 1000      # Total duration
plate = np.full((N, N), 20.0)  # Initial room temp

# --- 2. THE ALPHA MAP (Bi-Material) ---
alpha_map = np.zeros((N, N))
# Real Materials: Left = Copper, Right = Steel
alpha_copper = 0.116
alpha_steel = 0.013

alpha_map[:, :50] = alpha_copper
alpha_map[:, 50:] = alpha_steel

# --- 3. THE SIMULATION LOOP ---
for t in range(timesteps):
    # Apply Dirichlet Condition: Left edge is a constant 500°C heater
    plate[:, 0] = 500.0
    
    # Calculate the change (Laplacian)
    # This checks top, bottom, left, and right neighbors
    interior = plate[1:-1, 1:-1]
    up    = plate[0:-2, 1:-1]
    down  = plate[2:,   1:-1]
    left  = plate[1:-1, 0:-2]
    right = plate[1:-1, 2:]
    
    # Heat equation update using the Alpha Map
    plate[1:-1, 1:-1] += alpha_map[1:-1, 1:-1] * (up + down + left + right - 4*interior)
    
    # Apply Neumann Condition: Right edge is insulated (no heat escapes)
    # The last column becomes equal to the one before it
    plate[:, -1] = plate[:, -2]

    # Add these inside the 'for' loop, after the physics update:
    plate[0, :] = plate[1, :]   # Insulate top edge
    plate[-1, :] = plate[-2, :] # Insulate bottom edge

# --- 4. VISUALIZATION ---
plt.figure(figsize=(10, 6))
plt.imshow(plate, cmap='hot', interpolation='nearest')
plt.colorbar(label='Temperature (°C)')
plt.title(f"Heat Diffusion in Bi-Material Plate (t={timesteps})")
plt.xlabel("Copper | Steel")
plt.savefig("Heat_Diffusion_Thumbnail.png", dpi=300)

plt.show()