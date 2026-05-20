import numpy as np
import matplotlib.pyplot as plt
import aero_model
import dynamic
import display_utils
import scipy.integrate


## question 1 + interprétation avec 1/2pv2SCz= mg
# paramètres de l’étude
hs = np.linspace(4000, 10000, 15)      # altitudes (m)
machs = [0.4, 0.6, 0.8]                # nombres de Mach
static_margins = [0.2, 0.6, 1.0]       # marges statiques
mass_coeffs = [0.1, 0.5, 1.0]          # coefficients de masse
aero_m = aero_model.Airbus_A321_200()    # création du modèle avion
for ms in static_margins:
    for km in mass_coeffs: 
        aero_m.set_static_margin(ms)
        aero_m.set_mass(km * aero_m.m_design)
        aero_m.set_options(stall=True,buffeting=True,wave_drag=True)
        fig, axes = plt.subplots(3, 1, figsize=(8, 10))
        fig.suptitle( f"Trim A321_200 | ms={ms:.1f} | km={km:.1f}",fontsize=14)
        for mach in machs:
            aoas = []      # angle d’attaque
            dtrims = []    # trim profondeur
            dthrs = []     # poussée
            for h in hs:
                tas = aero_m.atm.tas_from_mach_altp(mach, h)
                aoa_e, dtrim_e, dthr_e = dynamic.graceful_trim(aero_m,h,tas,use_saturations=True)
                aoas.append(np.rad2deg(aoa_e))
                dtrims.append(np.rad2deg(dtrim_e))
                dthrs.append(100 * dthr_e)
            
            axes[0].plot( hs, aoas, label=f"Mach {mach}")
            axes[1].plot(hs,dtrims,label=f"Mach {mach}")
            axes[2].plot(hs,dthrs,label=f"Mach {mach}")
        # mise en forme graphique
        display_utils.decorate(axes[0], title="Angle d'attaque",xlab="Altitude h (m)",ylab=r"$\alpha$ (deg)",
                               legend=None)
        display_utils.decorate(axes[1],title="Déflexion gouverne",xlab="Altitude h (m)",
                               ylab=r"$\delta_{trim}$ (deg)",legend=None)
        display_utils.decorate(axes[2], title="Poussée moteur",xlab="Altitude h (m)",ylab=r"$\delta_{th}$ (%)",
                                legend=None)
        # affichage légendes
        axes[0].legend(loc='best')
        axes[1].legend(loc='best')
        axes[2].legend(loc='best')
        # ajustement figure
        plt.tight_layout()
        plt.show()


##question 2

hs = [4000, 6000, 8000, 10000]    # altitudes (m)
machs = [0.4, 0.6, 0.8]                # nombres de Mach
static_margins = [0.2, 0.6, 1.0]       # marges statiques
mass_coeffs = [0.1, 0.5, 1.0]          # coefficients de masse
for ms in static_margins:
    for km in mass_coeffs:
        aero_m = aero_model.Airbus_A321_200()  # création du modèle avion
        aero_m.set_static_margin(ms)
        aero_m.set_mass(km * aero_m.m_design)
        aero_m.set_options(stall=True,buffeting=True,wave_drag=True)
        fig, ax = plt.subplots(figsize=(7, 9))
        fig.suptitle( f"Trim A319 | ms={ms:.1f} | km={km:.1f}",fontsize=14)
        for h in hs:
            dthrs = []     # poussée
            for mach in machs:
                tas = aero_m.atm.tas_from_mach_altp(mach, h)
                aoa_e, dtrim_e, dthr_e = dynamic.graceful_trim(aero_m,h,tas,use_saturations=True)
                dthrs.append(100 * dthr_e)
            ax.plot(machs,dthrs,label=f"h = {h} m" )
        display_utils.decorate(ax, title=f"Poussée nécessaire | ms={ms:.1f} | km={km:.1f}",xlab="Nombre de Mach",
            ylab=r"$\delta_{th}$ (%)",legend=None)
        ax.legend(loc='best')
        plt.tight_layout()
        plt.show()


""" Pour la question 3 on calcul Czeqb avec l'equa de sustentation en palier, on lit alphaeqb avec Cz=f(alpha) de seance 1 puis on a dthreqb
avec dthr=f(alpha) et pour dtrim c'est pareil mais on trouve Cxeqb avec la polaire, en ayant Czeqb puis on trace Cx=f(alpha) et 
on trace dtrim=f(alpha) et on lit dtrimeqb"""

#question 4
"""On peut prend pour ms=0.2 et on fixe km, on reprend ce programme de la seance 1"""

aero_m = aero_model.Airbus_A321_200()
aero_m.set_options(stall=False, buffeting=False, wave_drag=False)
aero_m.set_mass(aero_m.m_design)
aero_m.set_mass_from_km(0.1)
mach,q,tas,dm = 0.4,0, aero_m.atm.tas_from_mach_altp(0.4, aero_m.altp_ref),0
aoa_range = np.linspace(np.deg2rad(-10), np.deg2rad(20), 100)

for ms in [0.7, 0.2]:
    aero_m.set_static_margin(ms)
    dtrim_list = []
    cl_list=[]
    
    for aoa in aoa_range:
        # trim condition Cm = 0
        dtrim_e = -(aero_m.cm0 + aero_m.cma * (aoa - aero_m.a0)) / aero_m.cmtrim

        # stockage
        dtrim_list.append(np.rad2deg(dtrim_e))

        cz, cx, cm = aero_m.get_aero_coefs(aoa, mach, dtrim_e, dm, q, tas)
        cl_list.append(cz)

    plt.plot(np.rad2deg(aoa_range),cl_list , label=f"ms = {ms}")

plt.xlabel("Incidence α (deg)")
plt.ylabel("coeff portance eqb Cle")
plt.title("Cle en fonction de l'incidence α")
plt.grid(True)
plt.legend()
plt.show()

tas = aero_m.atm.tas_from_mach_altp(0.4, 6000)
print((aero_m.set_mass(aero_m.m_design)*9.81*2)/atmosphere.air_density()*tas**2*surface
""" attention on affiche Cz mais il faut la surface de ref de cet avion et lire 
dans table d'atmosphere standard à cette altitude le T et P qui correspondent"""


"""cf table d'atm standard"""

#question 5 à faire 
