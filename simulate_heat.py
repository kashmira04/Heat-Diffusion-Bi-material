import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# --- 1. SETUP ---
N = 100
timesteps = 1200 # Slightly longer to see the heat cross the interface
plate = np.full((N, N), 20.0)

# Alpha Map: Copper (Left) | Steel (Right)
alpha_map = np.zeros((N, N))
alpha_map[:, :50] = 0.116 
alpha_map[:, 50:] = 0.013

# --- 2. ANIMATION PREP ---
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(plate, cmap='hot', vmin=20, vmax=500, interpolation='nearest')
plt.colorbar(im, label='Temperature (°C)')
ax.set_title("Heat Diffusion: Copper vs. Steel Interface")
ax.set_xlabel("Copper (Left) | Steel (Right)")

def update(frame):
    global plate
    # Run 10 sub-steps per frame to speed up the animation
    for _ in range(10):
        plate[:, 0] = 500.0 # Heater
        
        interior = plate[1:-1, 1:-1]
        up, down = plate[0:-2, 1:-1], plate[2:, 1:-1]
        left, right = plate[1:-1, 0:-2], plate[1:-1, 2:]
        
        plate[1:-1, 1:-1] += alpha_map[1:-1, 1:-1] * (up + down + left + right - 4*interior)
        
        # Insulated Boundaries
        plate[:, -1] = plate[:, -2]
        plate[0, :] = plate[1, :]
        plate[-1, :] = plate[-2, :]
        
    im.set_array(plate)
    return [im]

# Create the animation (Frames = total steps / sub-steps)
ani = FuncAnimation(fig, update, frames=120, interval=50, blit=True)

# Save as GIF (Requires 'pillow' library: pip install pillow)
print("Saving animation... this may take a minute.")
ani.save('heat_diffusion.gif', writer='pillow')
plt.show()