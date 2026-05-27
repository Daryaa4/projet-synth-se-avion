# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
import scipy.optimize
import aero_model
import dynamic
import display_utils


# =============================================================================
# QUESTION 1 -- Trim (alpha, delta_trim, delta_thr) en fonction de l'altitude
# =============================================================================
hs             = np.linspace(4000, 10000, 15)
machs          = [0.4, 0.6, 0.8]
static_margins = [0.2, 0.6, 1.0]
mass_coeffs    = [0.1, 0.5, 1.0]

for ms in static_margins:
    for km in mass_coeffs:
        aero_m = aero_model.Airbus_A321_200()
        aero_m.set_static_margin(ms)
        aero_m.set_mass_from_km(km)
        aero_m.set_options(stall=True, buffeting=True, wave_drag=True)

        fig, axes = plt.subplots(3, 1, figsize=(8, 10))
        fig.suptitle(f"Trim A321_200 | ms={ms:.1f} | km={km:.1f}", fontsize=14)

        for mach in machs:
            aoas, dtrims, dthrs = [], [], []
            for h in hs:
                tas = aero_m.atm.tas_from_mach_altp(mach, h)
                aoa_e, dtrim_e, dthr_e = dynamic.graceful_trim(
                    aero_m, h, tas, use_saturations=True
                )
                aoas.append(np.rad2deg(aoa_e))
                dtrims.append(np.rad2deg(dtrim_e))
                dthrs.append(100 * dthr_e)

            axes[0].plot(hs, aoas,   label=f"Mach {mach}")
            axes[1].plot(hs, dtrims, label=f"Mach {mach}")
            axes[2].plot(hs, dthrs,  label=f"Mach {mach}")

        display_utils.decorate(axes[0], title="Angle d'attaque",
                               xlab="Altitude h (m)", ylab=r"$\alpha$ (deg)", legend=None)
        display_utils.decorate(axes[1], title="Deflexion gouverne",
                               xlab="Altitude h (m)", ylab=r"$\delta_{trim}$ (deg)", legend=None)
        display_utils.decorate(axes[2], title="Poussee moteur",
                               xlab="Altitude h (m)", ylab=r"$\delta_{th}$ (%)", legend=None)
        for ax in axes:
            ax.legend(loc='best')
        plt.tight_layout()
        plt.show()


# =============================================================================
# QUESTION 2 -- Poussee necessaire f(Mach) par altitude
# =============================================================================
hs             = [4000, 6000, 8000, 10000]
machs          = [0.4, 0.6, 0.8]
static_margins = [0.2, 0.6, 1.0]
mass_coeffs    = [0.1, 0.5, 1.0]

for ms in static_margins:
    for km in mass_coeffs:
        aero_m = aero_model.Airbus_A321_200()
        aero_m.set_static_margin(ms)
        aero_m.set_mass_from_km(km)
        aero_m.set_options(stall=True, buffeting=True, wave_drag=True)

        fig, ax = plt.subplots(figsize=(7, 9))
        fig.suptitle(f"Trim A321_200 | ms={ms:.1f} | km={km:.1f}", fontsize=14)

        for h in hs:
            dthrs = []
            for mach in machs:
                tas = aero_m.atm.tas_from_mach_altp(mach, h)
                _, _, dthr_e = dynamic.graceful_trim(
                    aero_m, h, tas, use_saturations=True
                )
                dthrs.append(100 * dthr_e)
            ax.plot(machs, dthrs, label=f"h = {h} m")

        display_utils.decorate(ax,
                               title=f"Poussee necessaire | ms={ms:.1f} | km={km:.1f}",
                               xlab="Nombre de Mach", ylab=r"$\delta_{th}$ (%)", legend=None)
        ax.legend(loc='best')
        plt.tight_layout()
        plt.show()


# =============================================================================
# QUESTION 3 -- Methode graphique (etapes analytiques)
#
# Etape 1 : Cz_eqb = 2 m g / (rho V2 S)        sustentation en palier
# Etape 2 : alpha_eqb  lu sur Cz = f(alpha)     polaires seance 1
# Etape 3 : delta_thr  lu sur delta_thr=f(alpha) au meme alpha
# Etape 4 : Cx_eqb     lu sur polaire Cx=f(Cz)  pour Cz_eqb
# Etape 5 : delta_trim lu sur delta_trim=f(alpha) au meme alpha
#
# Conditions fixees pour la comparaison Q5
# =============================================================================
H0   = 6000.   # m
MACH = 0.4
MS   = 0.2
KM   = 0.5

aero_m = aero_model.Airbus_A321_200()
aero_m.set_static_margin(MS)
aero_m.set_mass_from_km(KM)
aero_m.set_options(stall=False, buffeting=False, wave_drag=False)

pamb0, tamb0 = aero_m.atm.atmosphere(H0)
rho0  = aero_m.atm.air_density(pamb0, tamb0)
TAS0  = aero_m.atm.tas_from_mach_altp(MACH, H0)
S     = aero_m.w.s
MAC   = aero_m.w.mac
mass  = aero_m.m
g     = aero_m.atm.g

print("=" * 60)
print(f"Conditions Q3/Q5 : ms={MS} | km={KM} | h={H0:.0f} m | Mach={MACH}")
print(f"Masse={mass:.0f} kg | TAS={TAS0:.1f} m/s | rho={rho0:.4f} kg/m3")
print("=" * 60)

# Etape 1 -- Cz equilibre
Cz_eqb = (2 * mass * g) / (rho0 * TAS0**2 * S)
print(f"\nEtape 1 -- Cz_eqb = {Cz_eqb:.4f}")

# Etape 2 -- alpha equilibre
# cz_wf = cza * (aoa + set - a0)  =>  aoa = Cz/cza + a0 - set
aoa_graph = Cz_eqb / aero_m.cza + aero_m.a0 - aero_m.w.set
print(f"Etape 2 -- alpha_eqb = {np.rad2deg(aoa_graph):.4f} deg")

# Etape 3 -- delta_trim (Cm = 0)
dtrim_graph = -(aero_m.cm0 + aero_m.cma * (aoa_graph - aero_m.a0)) / aero_m.cmtrim
print(f"Etape 3 -- delta_trim = {np.rad2deg(dtrim_graph):.4f} deg")

# Etape 4 -- Cx equilibre via get_aero_coefs
cz_check, Cx_eqb, _ = aero_m.get_aero_coefs(aoa_graph, MACH, dtrim_graph, 0., 0., TAS0)
print(f"Etape 4 -- Cx_eqb = {Cx_eqb:.6f}  (Cz verifie = {cz_check:.4f})")

# Etape 5 -- delta_thr (T = D)
drag_eqb = 0.5 * rho0 * TAS0**2 * S * Cx_eqb
sigma     = rho0 / aero_m.atm.rho0

def thrust_residual(dthr):
    return aero_m.thrust(sigma, MACH, dthr) - drag_eqb

dthr_graph = scipy.optimize.brentq(thrust_residual, 0.0, 1.0)
print(f"Etape 5 -- Trainee={drag_eqb:.1f} N | delta_thr = {100*dthr_graph:.4f} %")


# =============================================================================
# QUESTION 4 -- Cle = f(alpha) pour deux marges statiques
#               + trace Cz = f(alpha) et delta_trim = f(alpha) pour la lecture
# =============================================================================
aero_m_q4 = aero_model.Airbus_A321_200()
aero_m_q4.set_options(stall=False, buffeting=False, wave_drag=False)
aero_m_q4.set_mass_from_km(KM)

mach_q4  = 0.4
h_q4     = H0
tas_q4   = aero_m_q4.atm.tas_from_mach_altp(mach_q4, h_q4)
aoa_range = np.linspace(np.deg2rad(-10), np.deg2rad(20), 200)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle(f"Q4 -- Courbes d'equilibre | h={H0:.0f} m | Mach={MACH}", fontsize=13)

for ms in [0.7, 0.2]:
    aero_m_q4.set_static_margin(ms)
    cl_list, dtrim_list, cx_list = [], [], []

    for aoa in aoa_range:
        dtrim_e = -(aero_m_q4.cm0 + aero_m_q4.cma * (aoa - aero_m_q4.a0)) / aero_m_q4.cmtrim
        cz, cx, _ = aero_m_q4.get_aero_coefs(aoa, mach_q4, dtrim_e, 0., 0., tas_q4)
        cl_list.append(cz)
        dtrim_list.append(np.rad2deg(dtrim_e))
        cx_list.append(cx)

    axes[0].plot(np.rad2deg(aoa_range), cl_list,    label=f"ms={ms}")
    axes[1].plot(np.rad2deg(aoa_range), dtrim_list, label=f"ms={ms}")
    axes[2].plot(cl_list, cx_list,                  label=f"ms={ms}")

# Marquage du point d'equilibre Q3 sur les courbes (ms=0.2)
aero_m_q4.set_static_margin(0.2)
dtrim_ref = -(aero_m_q4.cm0 + aero_m_q4.cma * (aoa_graph - aero_m_q4.a0)) / aero_m_q4.cmtrim
cz_ref, cx_ref, _ = aero_m_q4.get_aero_coefs(aoa_graph, MACH, dtrim_ref, 0., 0., TAS0)

axes[0].axhline(Cz_eqb, color='gray', linestyle=':', linewidth=1, label=f"Cz_eqb={Cz_eqb:.3f}")
axes[0].axvline(np.rad2deg(aoa_graph), color='red', linestyle='--', linewidth=1,
                label=f"alpha_eqb={np.rad2deg(aoa_graph):.2f} deg")
axes[1].axvline(np.rad2deg(aoa_graph), color='red', linestyle='--', linewidth=1)
axes[1].axhline(np.rad2deg(dtrim_ref), color='orange', linestyle=':', linewidth=1,
                label=f"dtrim={np.rad2deg(dtrim_ref):.2f} deg")
axes[2].axvline(Cz_eqb, color='gray', linestyle=':', linewidth=1)
axes[2].axhline(cx_ref, color='orange', linestyle=':', linewidth=1,
                label=f"Cx_eqb={cx_ref:.5f}")

axes[0].set_xlabel("alpha (deg)")
axes[0].set_ylabel("Cle")
axes[0].set_title("Portance d'equilibre Cle = f(alpha)")
axes[0].legend(fontsize=8)
axes[0].grid(True)

axes[1].set_xlabel("alpha (deg)")
axes[1].set_ylabel("delta_trim (deg)")
axes[1].set_title("Deflexion equilibre delta_trim = f(alpha)")
axes[1].legend(fontsize=8)
axes[1].grid(True)

axes[2].set_xlabel("Cle")
axes[2].set_ylabel("Cxe")
axes[2].set_title("Polaire d'equilibre Cxe = f(Cle)")
axes[2].legend(fontsize=8)
axes[2].grid(True)

plt.tight_layout()
plt.show()


# =============================================================================
# QUESTION 5 -- Comparaison trajectoires sur 100 s
#               Trim numerique (graceful_trim) vs trim graphique (Q3)
# =============================================================================

# --- Trim numerique ---
aoa_num, dtrim_num, dthr_num = dynamic.graceful_trim(
    aero_m, H0, TAS0, use_saturations=True
)

print("\n--- Trim numerique ---")
print(f"  alpha_trim = {np.rad2deg(aoa_num):.4f} deg")
print(f"  delta_trim = {np.rad2deg(dtrim_num):.4f} deg")
print(f"  delta_thr  = {100*dthr_num:.4f} %")

print("\n--- Ecarts (graphique - numerique) ---")
print(f"  D_alpha    = {np.rad2deg(aoa_graph   - aoa_num):+.4f} deg")
print(f"  D_dtrim    = {np.rad2deg(dtrim_graph - dtrim_num):+.4f} deg")
print(f"  D_dthr     = {100*(dthr_graph - dthr_num):+.4f} %")


# --- Equations du mouvement (point-masse, plan vertical) ---
# x_dot     = V cos(gamma)
# h_dot     = V sin(gamma)
# V_dot     = (T cos(alpha) - D - m g sin(gamma)) / m
# gamma_dot = (T sin(alpha) + L - m g cos(gamma)) / (m V)
def equations_du_mouvement(state, t, aero_m, aoa_trim, dtrim_trim, dthr_trim):
    x, h, V, gamma = state
    h = max(h, 0.0)
    V = max(V, 1.0)

    pamb, tamb = aero_m.atm.atmosphere(h)
    rho   = aero_m.atm.air_density(pamb, tamb)
    vsnd  = aero_m.atm.sound_speed(tamb)
    mach  = V / vsnd
    sigma = rho / aero_m.atm.rho0

    cz, cx, _ = aero_m.get_aero_coefs(aoa_trim, mach, dtrim_trim, 0., 0., V)

    pdyn = 0.5 * rho * V**2 * aero_m.w.s
    L = pdyn * cz
    D = pdyn * cx
    T = aero_m.thrust(sigma, mach, dthr_trim)
    m = aero_m.m

    return [
        V * np.cos(gamma),
        V * np.sin(gamma),
        (T * np.cos(aoa_trim) - D - m * g * np.sin(gamma)) / m,
        (T * np.sin(aoa_trim) + L - m * g * np.cos(gamma)) / (m * V)
    ]


X0     = [0.0, H0, TAS0, 0.0]
t_span = np.linspace(0, 100, 1000)

sol_num = scipy.integrate.odeint(
    equations_du_mouvement, X0, t_span,
    args=(aero_m, aoa_num,   dtrim_num,   dthr_num),
    rtol=1e-8, atol=1e-8
)
sol_grph = scipy.integrate.odeint(
    equations_du_mouvement, X0, t_span,
    args=(aero_m, aoa_graph, dtrim_graph, dthr_graph),
    rtol=1e-8, atol=1e-8
)

x_num,  h_num,  V_num,  gam_num  = sol_num.T
x_grph, h_grph, V_grph, gam_grph = sol_grph.T

# --- Figures ---
fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.suptitle(
    f"Q5 -- Comparaison trajectoires | ms={MS} | km={KM} | h0={H0:.0f} m | Mach={MACH}",
    fontsize=13
)

axes[0, 0].plot(t_span, h_num,  label="Trim numerique",  color="steelblue")
axes[0, 0].plot(t_span, h_grph, label="Trim graphique",  color="tomato", linestyle="--")
axes[0, 0].set_xlabel("Temps (s)")
axes[0, 0].set_ylabel("Altitude h (m)")
axes[0, 0].set_title("Altitude")
axes[0, 0].legend()
axes[0, 0].grid(True)

axes[0, 1].plot(t_span, V_num,  label="Trim numerique", color="steelblue")
axes[0, 1].plot(t_span, V_grph, label="Trim graphique", color="tomato", linestyle="--")
axes[0, 1].set_xlabel("Temps (s)")
axes[0, 1].set_ylabel("TAS (m/s)")
axes[0, 1].set_title("Vitesse vraie")
axes[0, 1].legend()
axes[0, 1].grid(True)

axes[1, 0].plot(t_span, np.rad2deg(gam_num),  label="Trim numerique", color="steelblue")
axes[1, 0].plot(t_span, np.rad2deg(gam_grph), label="Trim graphique", color="tomato", linestyle="--")
axes[1, 0].set_xlabel("Temps (s)")
axes[1, 0].set_ylabel("gamma (deg)")
axes[1, 0].set_title("Pente de trajectoire")
axes[1, 0].legend()
axes[1, 0].grid(True)

axes[1, 1].plot(t_span, h_grph - h_num, color="darkorange")
axes[1, 1].axhline(0, color="gray", linewidth=0.8, linestyle=":")
axes[1, 1].set_xlabel("Temps (s)")
axes[1, 1].set_ylabel("Delta h (m)")
axes[1, 1].set_title("Ecart d'altitude (graphique - numerique)")
axes[1, 1].grid(True)

plt.tight_layout()
plt.show()

# Trajectoire dans le plan (x, h)
fig2, ax2 = plt.subplots(figsize=(11, 4))
ax2.plot(x_num  / 1000, h_num,  color="steelblue", label="Trim numerique")
ax2.plot(x_grph / 1000, h_grph, color="tomato",    linestyle="--", label="Trim graphique")
ax2.set_xlabel("Distance parcourue (km)")
ax2.set_ylabel("Altitude (m)")
ax2.set_title(f"Trajectoire plan vertical | ms={MS} | km={KM} | Mach={MACH}")
ax2.legend()
ax2.grid(True)
plt.tight_layout()
plt.show()

# --- Resume chiffre ---
print("\n=== Etat a t = 100 s ===")
print(f"{'':25s} {'Numerique':>12s}  {'Graphique':>12s}  {'Ecart':>10s}")
print(f"{'Altitude h (m)':25s} {h_num[-1]:>12.2f}  {h_grph[-1]:>12.2f}  {h_grph[-1]-h_num[-1]:>+10.2f}")
print(f"{'Vitesse TAS (m/s)':25s} {V_num[-1]:>12.4f}  {V_grph[-1]:>12.4f}  {V_grph[-1]-V_num[-1]:>+10.4f}")
print(f"{'Pente gamma (deg)':25s} {np.rad2deg(gam_num[-1]):>12.6f}  {np.rad2deg(gam_grph[-1]):>12.6f}  {np.rad2deg(gam_grph[-1]-gam_num[-1]):>+10.6f}")
print(f"{'Distance x (km)':25s} {x_num[-1]/1000:>12.3f}  {x_grph[-1]/1000:>12.3f}  {(x_grph[-1]-x_num[-1])/1000:>+10.3f}")