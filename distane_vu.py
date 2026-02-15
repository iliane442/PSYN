import matplotlib.pyplot as plt
import numpy as np

###

angle_assiette_min = 0.0 #degree
angle_assiette_max =10.0 #degree

long_atterrissage = 1000.0 #m
v_verticale = -0.05 #m_vert/m_horizontal
alt_origin = 20.0 #m

###

def distance(alt,angle_assiette):
    #calcul de la distance vu par le lidar
    d = np.sqrt((np.sin(np.radians(angle_assiette))*alt**2+alt**2))
    #print(f"Distance au sol vu par le lidar : {d}m, pour un angle de {angle_assiette}° avec le sol et une altitude de {alt}m")
    return d

#distance(alt_origin,angle_assiette_max)