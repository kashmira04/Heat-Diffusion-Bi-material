import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 1. SETUP ---
N = 100
plate = np.full((N, N), 20.0)
alpha_map = np.zeros((N, N))
# Copper diffusivity: 0.116 | Steel diffusivity: 0.013
alpha_map[:, :50] = 0.116 
alpha_map[:, 50:] = 0.013

# --- 2. PREPARE THE FIGURE ---
fig, ax = plt.subplots(figsize=(10, 6))
im = ax.imshow(plate, cmap='hot', vmin=20, vmax=500, interpolation='nearest')
plt.colorbar(im, label='Temperature (°C)')

# UPDATED LABELS: Naming the materials clearly
ax.set_title("Transient Heat Diffusion: Copper vs. Steel Interface")
ax.set_xlabel("Position (Material: Copper | Steel)")
ax.set_ylabel("Position (Y-axis)")

# Add a vertical dashed line to mark the interface at x=50
ax.axvline(x=49.5, color='cyan', linestyle='--', linewidth=2, label='Interface')
ax.text(10, 95, "COPPER", color='white', fontweight='bold', fontsize=12)
ax.text(65, 95, "STEEL", color='white', fontweight='bold', fontsize=12)

# --- 3. THE ANIMATION FUNCTION ---
def update(frame):
    global plate
    for _ in range(15): 
        plate[:, 0] = 500.0 # Left edge heater
        
        interior = plate[1:-1, 1:-1]
        laplacian = (plate[:-2, 1:-1] + plate[2:, 1:-1] + 
                     plate[1:-1, :-2] + plate[1:-1, 2:] - 4*interior)
        
        plate[1:-1, 1:-1] += alpha_map[1:-1, 1:-1] * laplacian
        
        # Insulation Conditions
        plate[:, -1] = plate[:, -2] 
        plate[0, :] = plate[1, :]   
        plate[-1, :] = plate[-2, :] 
        
    im.set_array(plate)
    return [im]

# --- 4. SAVE THE GIF ---
print("Generating GIF with material labels...")
ani = FuncAnimation(fig, update, frames=80, blit=True)

# Save using the pillow writer
ani.save('heat_diffusion_copper_steel.gif', writer='pillow', fps=15)
print("Success! 'heat_diffusion_copper_steel.gif' is now in your folder.")

plt.show()