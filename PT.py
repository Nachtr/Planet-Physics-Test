from vpython import sphere, vector, rate, color, curve, scene, button
import random  # Fix: Import properly

scene.userzoom = True
scene.userspin = True
scene.userpan = True
scene.title = "Planetary System Physics Simulation"

# Sun (Star)
sun = sphere(pos=vector(0, 0, 0), radius=0.6, color=color.yellow)

# Planets
planet = sphere(pos=vector(1, 0, 0), radius=0.05, color=color.blue)
planet2 = sphere(pos=vector(1.8, 0, 0), radius=0.05, color=color.green)

# Constants
G = 1
M_sun = 1
M_planet = 0.01
dt = 0.01

# Function to prevent division by zero errors
def safe_norm(v):
    return v.norm() if v.mag > 1e-6 else vector(0, 0, 0)

# Compute stable orbital velocity for the planets around the Sun
r1 = planet.pos - sun.pos
orbital_velocity1 = vector(0, (G * M_sun / r1.mag) ** 0.5, 0)

r2 = planet2.pos - sun.pos
orbital_velocity2 = vector(0, (G * M_sun / r2.mag) ** 0.5, 0)

# Assign velocities
planet.velocity = orbital_velocity1
planet2.velocity = orbital_velocity2

# Trails for visualization
orbit_path1 = curve(color=color.white)
orbit_path2 = curve(color=color.red)

# Function to generate stars in the background (Fix: Proper random import)
def generate_stars(n):
    stars = []
    for _ in range(n):
        x, y, z = (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10))
        star = sphere(pos=vector(x, y, z), radius=0.02, color=color.white, emissive=True)
        stars.append(star)
    return stars

# Generate 100 stars randomly in the background
stars = generate_stars(100)

# Pause/Resume functionality
running = True
def toggle_simulation():
    global running
    running = not running
    start_button.text = "Resume" if not running else "Pause"

# Toggle Trails functionality (Fix: Clear trails without breaking references)
trails_enabled = True
def toggle_trails():
    global trails_enabled
    trails_enabled = not trails_enabled
    trail_button.text = "Enable Trails" if not trails_enabled else "Disable Trails"

    if not trails_enabled:
        orbit_path1.clear()  # Properly clear trails
        orbit_path2.clear()

# Create buttons
start_button = button(text="Pause", bind=toggle_simulation)
trail_button = button(text="Disable Trails", bind=toggle_trails)

# Spacebar Pause/Resume
def key_input(evt):
    global running
    if evt.key == ' ':
        toggle_simulation()

scene.bind('keydown', key_input)

# Simulation loop
while True:
    rate(100)  # Animation speed

    if running:
        # Gravity calculations
        r = planet.pos - sun.pos
        force = (-G * M_sun / r.mag2) * safe_norm(r)

        f = planet2.pos - sun.pos
        force2 = (-G * M_sun / f.mag2) * safe_norm(f)

        # Update velocities before updating positions
        planet.velocity += force * dt
        planet.pos += planet.velocity * dt

        planet2.velocity += force2 * dt
        planet2.pos += planet2.velocity * dt

        # Update orbit trails only if enabled
        if trails_enabled:
            orbit_path1.append(pos=planet.pos)
            orbit_path2.append(pos=planet2.pos)