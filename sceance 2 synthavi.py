import numpy as np
import matplotlib.pyplot as plt
import aero_model
import dynamic
import display_utils
import scipy.integrate


## q1 + interprétation avec 1/2pv2SCz= mg
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
