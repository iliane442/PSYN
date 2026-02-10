import matplotlib.pyplot as plt
import numpy as np

# --- Paramètres xFly J-65 (2x 2860-KV2200) ---
mass = 4.2           
thrust_static = 48.0 
s_area = 0.35        
cl_takeoff = 1.2     
cd = 0.04            
crr = 0.03           
rho = 1.225          
g = 9.81
target_alt = 150.0   
climb_angle_target = 20.0 # Angle cible en degrés durant la montée

# --- Initialisation ---
v = 0.1              
pos_x = 0            
alt = 0              
t = 0
dt = 0.05            
state = "GROUND_ROLL"
angle_deg = 0.0      # Angle initial

results = {"t": [], "v": [], "alt": [], "angle": []}

while t < 25:
    dynamic_pressure = 0.5 * rho * v**2
    thrust = thrust_static * (1 - (v / 180)) 
    
    if state == "GROUND_ROLL":
        angle_deg = 0.0
        lift = dynamic_pressure * s_area * cl_takeoff
        drag = dynamic_pressure * s_area * cd
        friction = crr * max(0, (mass * g) - lift)
        
        accel = (thrust - drag - friction) / mass
        v += accel * dt
        pos_x += v * dt
        
        if lift >= (mass * g):
            state = "CLIMB"

    elif state == "CLIMB":
        angle_deg = climb_angle_target
        angle_rad = np.radians(angle_deg)
        drag = dynamic_pressure * s_area * cd
        
        # Accélération tangentielle
        accel = (thrust - drag - (mass * g * np.sin(angle_rad))) / mass
        
        v += accel * dt
        pos_x += (v * np.cos(angle_rad)) * dt
        alt += (v * np.sin(angle_rad)) * dt
        
        if alt >= target_alt:
            state = "CRUISE"
            alt = target_alt

    elif state == "CRUISE":
        angle_deg = 0.0  # L'avion se remet à plat
        drag = dynamic_pressure * s_area * cd
        accel = (thrust - drag) / mass
        
        v += accel * dt
        pos_x += v * dt

    t += dt
    results["t"].append(t)
    results["v"].append(v * 3.6)
    results["alt"].append(alt)
    results["angle"].append(angle_deg)

# --- Visualisation ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

# 1. Altitude
ax1.plot(results["t"], results["alt"], color='blue', label='Altitude (m)')
ax1.set_ylabel("Altitude (m)")
ax1.grid(True)

# 2. Vitesse
ax2.plot(results["t"], results["v"], color='green', label='Vitesse (km/h)')
ax2.set_ylabel("Vitesse (km/h)")
ax2.grid(True)

# 3. Angle (Pitch)
ax3.step(results["t"], results["angle"], color='purple', where='post', label='Angle (deg)')
ax3.set_ylabel("Angle d'assiette (°)")
ax3.set_xlabel("Temps (s)")
ax3.set_ylim(-5, 30)
ax3.grid(True)

plt.tight_layout()
plt.show()