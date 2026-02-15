import numpy as np
import matplotlib.pyplot as plt
"""
%
def simulation_atterrissage_xfly():
    # --- 1. Paramètres du X-FLY J65 (Version 70mm) ---
    masse = 3.9        # kg (Poids en ordre de vol)
    surface_alaire = 0.43  # m^2 (43 dm^2)
    vitesse_kmh = 130   # km/h (Vitesse typique d'approche pour ce jet)
    
    # --- 2. Constantes physiques ---
    g = 9.81           # Gravité (m/s^2)
    rho = 1.225        # Densité de l'air au niveau de la mer (kg/m^3)
    
    # Conversion vitesse en m/s
    vitesse_ms = vitesse_kmh / 3.6
    
    # --- 3. Calcul de la Portance Requise ---
    # Pour ne pas tomber comme une pierre, Portance (Lift) = Poids (Weight) * cos(pente)
    # Sur une pente faible, on approxime Lift ≈ Poids = m * g
    poids_newtons = masse * g
    
    # Équation de la portance : L = 0.5 * rho * V^2 * S * CL
    # On isole le Coefficient de Portance (CL) nécessaire
    cl_requis = poids_newtons / (0.5 * rho * (vitesse_ms**2) * surface_alaire)
    
    # --- 4. Estimation de l'Angle d'Attaque (Alpha) ---
    # Pour un profil d'aile standard, la pente de portance est d'environ 0.1 par degré.
    # CL = CL0 + (dCL/dAlpha * Alpha)
    # On suppose un profil symétrique ou semi-symétrique (CL0 proche de 0 pour simplifier)
    pente_portance = 0.1 # par degré (standard)
    alpha_degres = cl_requis / pente_portance
    
    # --- 5. Calcul de l'Assiette (Pitch) ---
    # Relation : Assiette (Theta) = Pente (Gamma) + Angle d'attaque (Alpha)
    angle_pente_degres = -3.5  # Pente d'approche standard RC (un peu plus raide que le grandeur nature)
    
    assiette_nez = angle_pente_degres + alpha_degres

    # --- 6. Affichage des Résultats ---
    print(f"--- RÉSULTATS SIMULATION X-FLY J65 ---")
    print(f"Vitesse d'approche : {vitesse_kmh} km/h")
    print(f"Portance requise   : {poids_newtons:.2f} N")
    print(f"CL (Coef. Portance): {cl_requis:.3f}")
    print(f"--------------------------------------")
    print(f"Angle de pente (Trajectoire) : {angle_pente_degres:.2f}°")
    print(f"Angle d'attaque (Aerodynamique): +{alpha_degres:.2f}°")
    print(f"-> ANGLE DU NEZ AVEC LE SOL  : {assiette_nez:.2f}°")
    
    # --- 7. Visualisation Graphique (Arrondi) ---
    # Simulation de la trajectoire finale (Flare)
    dist_horizontale = np.linspace(0, 100, 500) # 100m de distance
    altitude = np.zeros_like(dist_horizontale)
    
    # Approche linéaire puis exponentielle pour l'arrondi (flare)
    h_init = 15 # Hauteur début simulation
    pente_rad = np.radians(angle_pente_degres)
    
    for i, x in enumerate(dist_horizontale):
        # Descente simple
        h_theorique = h_init + (x * np.tan(pente_rad))
        
        # Arrondi : on commence à tirer doucement à 2m du sol
        if h_theorique < 2 and h_theorique > 0:
            altitude[i] = h_theorique * (1 + 0.5 * (2-h_theorique)) # Facteur de lissage
        else:
            altitude[i] = max(0, h_theorique)

    plt.figure(figsize=(10, 6))
    plt.plot(dist_horizontale, altitude, label='Trajectoire du Train Principal', color='blue', linewidth=2)
    plt.axhline(0, color='black', linewidth=2) # Sol
    
    # Représentation de l'avion à l'impact
    x_touch = dist_horizontale[np.argmin(np.abs(altitude - 0.1))] # Point de toucher
    plt.scatter(x_touch, 0, color='red', s=100, label='Point de Toucher', zorder=5)
    
    plt.title(f"Simulation Atterrissage X-FLY J65\nAssiette calculée : {assiette_nez:.1f}° (Nez levé)", fontsize=14)
    plt.xlabel("Distance (m)")
    plt.ylabel("Altitude (m)")
    plt.grid(True, linestyle='--')
    plt.legend()
    plt.annotate(f"Le nez est levé de {assiette_nez:.1f}°\npour compenser la descente", 
                 xy=(x_touch, 1), xytext=(x_touch-20, 5),
                 arrowprops=dict(facecolor='black', shrink=0.05))
    
    plt.show()

if __name__ == "__main__":
    simulation_atterrissage_xfly()
"""

"""
def simulation_charge_lourde():
    # --- 1. Configuration "Charge Scientifique" ---
    v_decrochage_kmh = 100.0  # La limite mortelle
    v_decrochage_ms = v_decrochage_kmh / 3.6
    
    # Pour respecter la sécurité (1.3 Vs), on approche très vite
    v_approche_kmh = 130.0 
    v0 = v_approche_kmh / 3.6
    
    # Estimation de la masse basée sur ce décrochage (calcul inverse approximatif)
    # Pour décrocher à 100km/h avec cette surface, l'avion est très lourd ou le profil peu porteur
    masse = 7.5  # kg (Hypothèse d'un avion très chargé)
    surface_alaire = 0.43 
    
    # Paramètres physiques
    g = 9.81
    rho = 1.225
    cd0 = 0.035  # Traînée un peu plus forte (pods scientifiques externes ?)
    
    # --- 2. Initialisation ---
    z = 20.0   # Altitude initiale
    x = 0.0
    
    # Pente d'approche standard (-3°)
    gamma_deg = -3.0
    vx = v0 * np.cos(np.radians(gamma_deg))
    vz = v0 * np.sin(np.radians(gamma_deg))
    
    dt = 0.02
    
    # Listes pour graphiques
    pos_x, pos_z = [x], [z]
    vitesses_kmh = [v_approche_kmh]
    incidence_deg = []
    etat_vol = [] # 0=Vol, 1=Décrochage, 2=Sol
    
    crashed = False
    touched = False
    
    # --- 3. Boucle de Simulation ---
    while x < 1000 and not touched and not crashed: # On rallonge la piste simulée
        
        v_total = np.sqrt(vx**2 + vz**2)
        
        # --- LOGIQUE PILOTE ---
        h_flare = 3.0 # On commence l'arrondi bas
        
        # Commande de portance cible (Load Factor n)
        if z > h_flare:
            # Maintien de la pente
            nz_demande = 1.0 # 1G
            # Légère correction si on descend trop vite
            if vz < -8.0: nz_demande = 1.2
        else:
            # ARRONDI (Flare)
            # Avec un avion lourd, il faut tirer fort mais PAS TROP (risque de décrochage)
            # On essaie de casser la vitesse verticale
            nz_demande = 1.0 + (abs(vz) * 0.4) # Loi proportionnelle
        
        # --- AÉRODYNAMIQUE CRITIQUE ---
        
        # 1. Calcul du CL requis pour obtenir ce facteur de charge
        portance_requise = nz_demande * masse * g
        
        # Effet de sol (très important pour un avion lourd)
        if z < 1.5: 
            portance_requise *= 0.85 # L'effet de sol "aide", on a besoin de moins de CL
            
        pression_dyn = 0.5 * rho * (v_total**2) * surface_alaire
        cl_requis = portance_requise / pression_dyn
        
        # 2. VÉRIFICATION DU DÉCROCHAGE (STALL)
        # Un CL max typique est environ 1.2 à 1.4. 
        # Si on dépasse CL max, ou si V < V_decrochage, c'est la chute.
        cl_max = 1.3
        
        # Calcul de l'angle d'attaque (Alpha) approximatif
        alpha = cl_requis / 0.1
        
        est_decroche = False
        if v_total < v_decrochage_ms:
            est_decroche = True
        elif cl_requis > cl_max:
            est_decroche = True # Décrochage dynamique (High speed stall)
            
        if est_decroche:
            # En décrochage : Portance s'effondre, Traînée explose
            lift = 0.3 * pression_dyn * surface_alaire # Chute de portance
            drag = 0.8 * pression_dyn * surface_alaire # Mur de traînée
            etat_vol.append(1)
            crashed = True # Considéré comme perte de contrôle près du sol
        else:
            # Vol normal
            lift = portance_requise
            cd = cd0 + 0.05 * (cl_requis**2)
            drag = pression_dyn * cd * surface_alaire
            etat_vol.append(0)

        # --- Équations du mouvement ---
        gamma = np.arctan2(vz, vx)
        
        fx = -drag * np.cos(gamma) - lift * np.sin(gamma)
        fz = lift * np.cos(gamma) - drag * np.sin(gamma) - masse * g
        
        ax = fx / masse
        az = fz / masse
        
        vx += ax * dt
        vz += az * dt
        
        x += vx * dt
        z += vz * dt
        
        # Contact sol
        if z <= 0:
            z = 0
            touched = True
            etat_vol[-1] = 2
        
        pos_x.append(x)
        pos_z.append(z)
        vitesses_kmh.append(np.sqrt(vx**2 + vz**2)*3.6)
        incidence_deg.append(alpha)

    # --- 4. Visualisation ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Trajectoire
    ax1.plot(pos_x, pos_z, 'b-', linewidth=2, label='Trajectoire')
    ax1.axhline(0, color='k', linewidth=2)
    ax1.axhspan(0, 1.5, color='green', alpha=0.1, label='Zone Effet de Sol')
    
    if crashed:
        idx_crash = etat_vol.index(1)
        ax1.scatter(pos_x[idx_crash], pos_z[idx_crash], color='red', s=200, marker='X', label='DÉCROCHAGE', zorder=10)
        ax1.text(pos_x[idx_crash], pos_z[idx_crash]+2, "PERTE DE PORTANCE !", color='red', fontweight='bold')
    else:
        ax1.scatter(pos_x[-1], 0, color='green', s=100, label='Toucher')
        
    ax1.set_title(f"Atterrissage Lourd (Charge Scientifique)\nApproche: {v_approche_kmh} km/h | Décrochage: {v_decrochage_kmh} km/h")
    ax1.set_ylabel("Altitude (m)")
    ax1.set_ylim(0, 20)
    ax1.legend()
    ax1.grid(True)
    
    # Vitesse vs Limite
    ax2.plot(pos_x, vitesses_kmh, 'b-', linewidth=2, label='Vitesse Avion')
    ax2.axhline(v_decrochage_kmh, color='red', linewidth=3, linestyle='--', label='LIMITE DÉCROCHAGE (100 km/h)')
    
    # Colorier la zone de danger
    ax2.fill_between(pos_x, 0, v_decrochage_kmh, color='red', alpha=0.1)
    
    # Afficher la vitesse de toucher
    v_touch = vitesses_kmh[-1]
    ax2.scatter(pos_x[-1], v_touch, color='black')
    ax2.annotate(f"Vitesse Toucher: {v_touch:.1f} km/h", 
                 xy=(pos_x[-1], v_touch), xytext=(pos_x[-1]-100, v_touch+10),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    ax2.set_xlabel("Distance (m)")
    ax2.set_ylabel("Vitesse (km/h)")
    ax2.set_ylim(80, 140)
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    simulation_charge_lourde()

    """



def simulation_avec_assiette():
    # --- 1. Paramètres (Config "Lourde") ---
    masse = 7.5         # kg
    surface_alaire = 0.43 
    g = 9.81
    rho = 1.225
    cd0 = 0.035
    
    # Limites
    v_decrochage_kmh = 100.0 
    v_decrochage_ms = v_decrochage_kmh / 3.6
    alpha_max = 14.0 # Angle d'incidence max avant décrochage (degrés)
    
    # Conditions Initiales (Approche rapide pour compenser le poids)
    v_approche_kmh = 135.0 
    v0 = v_approche_kmh / 3.6
    
    z = 20.0  
    x = 0.0
    gamma_init = -3.0 # Pente initiale
    
    vx = v0 * np.cos(np.radians(gamma_init))
    vz = v0 * np.sin(np.radians(gamma_init))
    
    dt = 0.02
    
    # --- LISTES DE DONNÉES ---
    pos_x, pos_z = [x], [z]
    vitesses_kmh = [v_approche_kmh]
    
    # Nouvelles listes pour les angles
    liste_assiette = []   # Theta (Pitch)
    liste_incidence = []  # Alpha (Attack)
    liste_pente = []      # Gamma (Flight Path)
    
    crashed = False
    touched = False
    
    while x < 800 and not touched and not crashed:
        v_total = np.sqrt(vx**2 + vz**2)
        
        # --- CALCUL DES ANGLES INSTANTANÉS ---
        # 1. Pente actuelle (Gamma)
        gamma_rad = np.arctan2(vz, vx)
        gamma_deg = np.degrees(gamma_rad)
        
        # --- PILOTAGE & PHYSIQUE ---
        h_flare = 3.5
        
        # Facteur de charge demandé (Pilotage)
        if z > h_flare:
            nz = 1.0 # Approche stable
            if vz < -7.0: nz = 1.3 # Correction si chute trop rapide
        else:
            # Arrondi : on tire progressivement
            # Attention : avec un avion lourd, tirer trop fort = décrochage immédiat
            nz = 1.0 + (abs(vz) * 0.35)
            
        # Portance requise
        lift_req = nz * masse * g
        if z < 1.5: lift_req *= 0.85 # Effet de sol
        
        # Coefficient de portance (CL)
        q = 0.5 * rho * (v_total**2) * surface_alaire
        cl_requis = lift_req / q
        
        # 2. Incidence estimée (Alpha)
        # Relation linéaire simplifiée : Alpha = CL / 0.1
        # On borne alpha pour simuler la limite physique de l'aile
        alpha_deg = cl_requis / 0.1
        
        # DÉTECTION DÉCROCHAGE
        est_decroche = False
        if v_total < v_decrochage_ms or alpha_deg > alpha_max:
            est_decroche = True
            crashed = True
            alpha_deg = 20.0 # L'incidence explose lors du décrochage
        
        # 3. Calcul de l'Assiette (Theta)
        # Theta = Gamma + Alpha
        # (Si je descends à -3° et que mon aile a +5° d'incidence, mon nez est à +2°)
        theta_deg = gamma_deg + alpha_deg
        
        # Stockage
        liste_pente.append(gamma_deg)
        liste_incidence.append(alpha_deg)
        liste_assiette.append(theta_deg)
        
        # --- DYNAMIQUE ---
        if est_decroche:
            lift = 0.4 * q # Perte portance
            drag = 0.9 * q # Mur de traînée
        else:
            lift = lift_req
            drag = q * (cd0 + 0.05 * (cl_requis**2))
            
        # Projection des forces
        fx = -drag * np.cos(gamma_rad) - lift * np.sin(gamma_rad)
        fz = lift * np.cos(gamma_rad) - drag * np.sin(gamma_rad) - masse * g
        
        vx += (fx / masse) * dt
        vz += (fz / masse) * dt
        x += vx * dt
        z += vz * dt
        
        if z <= 0:
            z = 0
            touched = True
            
        pos_x.append(x)
        pos_z.append(z)
        vitesses_kmh.append(np.sqrt(vx**2 + vz**2)*3.6)

    # --- AJUSTEMENT TAILLE LISTES ---
    # Les listes d'angles ont 1 élément de moins que pos_x (calculé dans la boucle)
    # On duplique la dernière valeur pour l'affichage
    liste_assiette.append(liste_assiette[-1])
    liste_incidence.append(liste_incidence[-1])
    liste_pente.append(liste_pente[-1])

    # --- VISUALISATION (3 Graphiques) ---
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    
    # 1. Altitude
    ax1.plot(pos_x, pos_z, 'b-', label='Altitude')
    ax1.axhline(0, color='k', linewidth=2)
    ax1.set_ylabel("Altitude (m)")
    ax1.set_title("Simulation Complète : Altitude, Vitesse et Assiette")
    ax1.grid(True)
    
    if crashed:
        ax1.text(pos_x[-1], pos_z[-1]+2, "DÉCROCHAGE", color='red', fontweight='bold')
    
    # 2. Vitesse
    ax2.plot(pos_x, vitesses_kmh, 'g-', label='Vitesse')
    ax2.axhline(v_decrochage_kmh, color='red', linestyle='--', label='Limite Décrochage')
    ax2.set_ylabel("Vitesse (km/h)")
    ax2.legend()
    ax2.grid(True)
    
    # 3. ANGLES (Le nouveau graphique)
    ax3.plot(pos_x, liste_assiette, 'r-', linewidth=2, label='Assiette (Nez) $\\theta$')
    ax3.plot(pos_x, liste_incidence, 'k--', alpha=0.5, label='Incidence Aile $\\alpha$')
    ax3.plot(pos_x, liste_pente, 'b:', alpha=0.5, label='Pente Trajectoire $\\gamma$')
    
    # Zone idéale d'atterrissage (Nez entre 0 et 5 degrés)
    ax3.axhspan(0, 5, color='green', alpha=0.1, label='Assiette Idéale au Toucher')
    ax3.axhline(0, color='black', linewidth=1)
    
    ax3.set_ylabel("Angles (Degrés)")
    ax3.set_xlabel("Distance (m)")
    ax3.legend(loc='upper left')
    ax3.grid(True)
    
    # Annotations sur l'assiette finale
    theta_final = liste_assiette[-1]
    ax3.annotate(f"Assiette Finale: {theta_final:.1f}°", 
                 xy=(pos_x[-1], theta_final), 
                 xytext=(pos_x[-1]-100, theta_final+5),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    simulation_avec_assiette()