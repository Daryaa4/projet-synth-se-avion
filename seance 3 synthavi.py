import numpy as np
import matplotlib.pyplot as plt
import aero_model
import dynamic
import atmosphere
from scipy.integrate import odeint


""" valeur propre suivant altitude"""
aero_m = aero_model.Airbus_A321_200()
mach = 0.6
ms = 0.7
km = 0.5
hs = [4000, 6000, 8000, 10000]
colors = ['blue', 'green', 'orange', 'red']
fig, ax = plt.subplots(figsize=(8,8))
for i, h in enumerate(hs):
    tas = aero_m.atm.tas_from_mach_altp(mach, h)
    aoa_e, dtrim_e, dthr_e = dynamic.graceful_trim (aero_m,h,tas,use_saturations=False)
    Xe = np.array([aoa_e,0,tas,0,h,0,aero_m.get_mass()])
    Ue = (dtrim_e, 0, dthr_e)
    A, B = dynamic.num_jacobian(Xe, Ue, aero_m)
    A4 = A[0:4,0:4]
    eigvals = np.linalg.eigvals(A4)
    for eig in eigvals:
        ax.plot(eig.real,eig.imag,'o', color=colors[i],label=f"h={h} m")

ax.axvline(0,color='k')
ax.set_xlabel("Re(λ)")
ax.set_ylabel("Im(λ)")
ax.set_title("Valeurs propres selon l'altitude")
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())
ax.grid(True)
plt.show()



machs = [0.4, 0.6, 0.8]
colors = ['blue', 'green', 'red']
h = 6000
fig, ax = plt.subplots(figsize=(8,8))

for i, mach in enumerate(machs):
    tas = aero_m.atm.tas_from_mach_altp(mach, h)
    aoa_e, dtrim_e, dthr_e = dynamic.graceful_trim(aero_m,h,tas,use_saturations=False)
   
    Xe = np.array([aoa_e,0,tas,0,h,0,aero_m.get_mass()])
    Ue = (dtrim_e, 0, dthr_e)

    A, B = dynamic.num_jacobian(Xe, Ue, aero_m)
    A4 = A[0:4,0:4]

    eigvals = np.linalg.eigvals(A4)
    for eig in eigvals:
        ax.plot( eig.real, eig.imag,'o',color=colors[i],label=f"Ma={mach}")

ax.axvline(0,color='k')
ax.set_xlabel("Re(λ)")
ax.set_ylabel("Im(λ)")
ax.set_title("Valeurs propres selon le Mach")

handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())
ax.grid(True)
plt.show()



""" valeur propre suivant marge statique"""
aero_m = aero_model.Airbus_A321_200()
mach = 0.6
h = 6000
mss = [0.2, 0.5, 0.7]
colors = ['blue', 'green', 'red']
fig, ax = plt.subplots(figsize=(8,8))

for i, ms in enumerate(mss):
    aero_m.set_static_margin(ms)
    tas = aero_m.atm.tas_from_mach_altp(mach, h)
    aoa_e, dtrim_e, dthr_e = dynamic.graceful_trim(aero_m,h,tas,use_saturations=False)

    Xe = np.array([aoa_e,0,tas,0,h,0, aero_m.get_mass()]) #état trim
    Ue = (dtrim_e, 0, dthr_e)# commande trim

    A, B = dynamic.num_jacobian(Xe, Ue, aero_m) # linéarisation
    A4 = A[0:4,0:4] # sous-système longitudinal

    eigvals = np.linalg.eigvals(A4) # valeurs propres
    for eig in eigvals:
        ax.plot(eig.real, eig.imag,'o',color=colors[i],markersize=8,label=f"ms = {ms}")

ax.axvline(0,color='black') # axe stabilité
ax.set_xlabel("Partie réelle")
ax.set_ylabel("Partie imaginaire")
ax.set_title("Valeurs propres selon la marge statique")

# éviter doublons légende
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())
ax.grid(True)
plt.show()



""" valeur propre suivant masse avec réglage km"""
aero_m = aero_model.Airbus_A321_200()
mach = 0.6
h = 6000
kms = [0.1, 0.5, 1.0]
colors = ['blue', 'green', 'red']
fig, ax = plt.subplots(figsize=(8,8))

for i, km in enumerate(kms):
    aero_m.set_mass_from_km(km)
    tas = aero_m.atm.tas_from_mach_altp(mach, h)
    aoa_e, dtrim_e, dthr_e = dynamic.graceful_trim(aero_m,h,tas,use_saturations=False)

    Xe = np.array([aoa_e,0,tas,0,h,0,aero_m.get_mass()])
    Ue = np.array([dtrim_e,0,dthr_e])

    A, B = dynamic.num_jacobian(Xe, Ue, aero_m)
    A4 = A[0:4, 0:4]

    eigvals = np.linalg.eigvals(A4)
    print(f"\nkm = {km}")
    print(eigvals)
    for eig in eigvals:
        ax.plot(eig.real,eig.imag,'o',color=colors[i],markersize=8,label=f"km = {km}")

ax.axvline(0, color='black')
ax.set_xlabel("Partie réelle")
ax.set_ylabel("Partie imaginaire")
ax.set_title("Valeurs propres selon la masse")

# légende sans doublons
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys())
ax.grid(True)
plt.show()


"""
mach = 0.6
h = 6000
ms = 0.1
km = 0.5

choix point de trim stable
"""

"""
autre alternative, on affiche un point de trim particulier avec print dans console
"""

atm = atmosphere.AtmosphereISA()
avion = aero_model.Airbus_A321_200(atm)


avion.set_mass_from_km(0.5)
avion.set_static_margin(0.1)
h = 6000      # m
mach = 0.6

Va = atm.tas_from_mach_altp(mach, h)

trim = dynamic.get_trim_level_flight(avion, h, Va)
print("\nRésultat du trim :")
print(trim)

aoa_e = trim["aoa"][0]
dtrim_e = trim["dtrim"][0]
dthr_e = trim["dthr"][0]

# construction point d'équilibre
Xe = np.array([aoa_e,0.0,Va,0.0,h,0.0,avion.get_mass()])
Ue = np.array([dtrim_e, 0.0,dthr_e])# commande d'équilibre

Wh = 2.0  # modélisation cisaillement du vent
delta_alpha = np.arctan(Wh / Va)

X0 = Xe.copy()
X0[0] += delta_alpha

t = np.linspace(0, 240, 5000)

# MODELE NON LINEAIRE
Xnl = odeint(dynamic.get_state_dot,X0,t,args=(Ue, avion))
print("\nDimensions Xnl :")
print(Xnl.shape)

alpha_nl = Xnl[:, 0]
q_nl     = Xnl[:, 1]
Va_nl    = Xnl[:, 2]
gamma_nl = Xnl[:, 3]
theta_nl = alpha_nl + gamma_nl

# MODELE LINEARISE
A, B = dynamic.num_jacobian(Xe, Ue, avion)
idx = [0, 1, 2, 3]
A4 = A[np.ix_(idx, idx)]
B4 = B[np.ix_(idx,[dynamic.iv_dtrim,dynamic.iv_dm,dynamic.iv_dthr])]


eigvals = np.linalg.eigvals(A4)
print("\nValeurs propres du modèle linéarisé :")
print(eigvals)

# condition initiale perturbée
x0 = np.array([delta_alpha,0,0,0])

# système linéarisé
def f_lin(x, t):
    return A4 @ x

# simulation
Xlin = odeint(f_lin,x0,t)
alpha_lin = aoa_e + Xlin[:, 0]
q_lin     = Xlin[:, 1]
Va_lin    = Va + Xlin[:, 2]
gamma_lin = Xlin[:, 3]
theta_lin = alpha_lin + gamma_lin

# COMPARAISON
plt.figure(figsize=(10,8))

plt.subplot(411)
plt.plot(t, Va_nl, label='Non linéaire')
plt.plot(t, Va_lin, '--', label='Linéarisé')
plt.ylabel("Va (m/s)")
plt.legend()
plt.grid()

plt.subplot(412)
plt.plot(t, np.rad2deg(alpha_nl))
plt.plot(t, np.rad2deg(alpha_lin), '--')
plt.ylabel("α (deg)")
plt.grid()

plt.subplot(413)
plt.plot(t, np.rad2deg(theta_nl))
plt.plot(t, np.rad2deg(theta_lin), '--')
plt.ylabel("θ (deg)")
plt.grid()

plt.subplot(414)
plt.plot(t, np.rad2deg(q_nl))
plt.plot(t, np.rad2deg(q_lin), '--')
plt.ylabel("q (deg/s)")
plt.xlabel("Temps (s)")
plt.grid()

plt.tight_layout()
plt.show()



atm = atmosphere.AtmosphereISA()
avion = aero_model.Airbus_A321_200(atm)
avion.set_mass_from_km(0.5)
avion.set_static_margin(0.1)
h = 6000      # m
mach = 0.6
Va = atm.tas_from_mach_altp(mach, h)

trim = dynamic.get_trim_level_flight(avion, h, Va)
print("\nRésultat du trim :")
print(trim)

aoa_e = trim["aoa"][0]
dtrim_e = trim["dtrim"][0]
dthr_e = trim["dthr"][0]

Xe = np.array([aoa_e,0.0,Va,0.0,h,0.0,avion.get_mass()])
Ue = np.array([dtrim_e,0.0,dthr_e])
Wh = 2.0
delta_alpha = np.arctan(Wh / Va)
X0 = Xe.copy()
X0[0] += delta_alpha

t = np.linspace(0, 10, 1000)

# MODELE NON LINEAIRE
Xnl = odeint(dynamic.get_state_dot,X0,t,args=(Ue, avion))
print("\nDimensions Xnl :")
print(Xnl.shape)

alpha_nl = Xnl[:, 0]
q_nl     = Xnl[:, 1]
Va_nl    = Xnl[:, 2]
gamma_nl = Xnl[:, 3]
theta_nl = alpha_nl + gamma_nl

# MODELE LINEARISE
A, B = dynamic.num_jacobian(Xe, Ue, avion)
idx = [0, 1, 2, 3]
A4 = A[np.ix_(idx, idx)]
B4 = B[np.ix_(idx,[dynamic.iv_dtrim,dynamic.iv_dm,dynamic.iv_dthr])]

eigvals = np.linalg.eigvals(A4)
print("\nValeurs propres du modèle linéarisé :")
print(eigvals)

# condition initiale perturbée
x0 = np.array([delta_alpha,0,0,0])

# système linéarisé
def f_lin(x, t):
    return A4 @ x

# simulation
Xlin = odeint(f_lin,x0,t)
alpha_lin = aoa_e + Xlin[:, 0]
q_lin     = Xlin[:, 1]
Va_lin    = Va + Xlin[:, 2]
gamma_lin = Xlin[:, 3]
theta_lin = alpha_lin + gamma_lin

# COMPARAISON
plt.figure(figsize=(10,8))
plt.subplot(411)
plt.plot(t, Va_nl, label='Non linéaire')
plt.plot(t, Va_lin, '--', label='Linéarisé')
plt.ylabel("Va (m/s)")
plt.legend()
plt.grid()

plt.subplot(412)
plt.plot(t, np.rad2deg(alpha_nl))
plt.plot(t, np.rad2deg(alpha_lin), '--')
plt.ylabel("α (deg)")
plt.grid()

plt.subplot(413)
plt.plot(t, np.rad2deg(theta_nl))
plt.plot(t, np.rad2deg(theta_lin), '--')
plt.ylabel("θ (deg)")
plt.grid()

plt.subplot(414)
plt.plot(t, np.rad2deg(q_nl))
plt.plot(t, np.rad2deg(q_lin), '--')
plt.ylabel("q (deg/s)")
plt.xlabel("Temps (s)")
plt.grid()

plt.tight_layout()
plt.show()




# TRIM 1 : point autour duquel on construit le modèle linéaire
atm = atmosphere.AtmosphereISA()
avion1 = aero_model.Airbus_A321_200(atm)
avion1.set_mass_from_km(0.5)
avion1.set_static_margin(0.10)
h1 = 6000
mach1 = 0.60
Va1 = atm.tas_from_mach_altp(mach1, h1)
trim1 = dynamic.get_trim_level_flight(avion1,h1,Va1)

aoa1   = trim1["aoa"][0]
dtrim1 = trim1["dtrim"][0]
dthr1  = trim1["dthr"][0]
Xe1 = np.array([aoa1,0.0,Va1,0.0,h1,0.0,avion1.get_mass()])
Ue1 = np.array([dtrim1,0.0,dthr1])

# Linéarisation autour du trim 1
A1, B1 = dynamic.num_jacobian(Xe1,Ue1,avion1)
A4 = A1[0:4, 0:4]

eigvals = np.linalg.eigvals(A4)
print("Valeurs propres du modèle linéarisé :")
print(eigvals)


# PERTURBATION INITIALE
Wh = 2.0
delta_alpha = np.arctan(Wh / Va1)
x0_lin = np.array([delta_alpha,0.0,0.0,0.0])


# SIMULATION MODELE LINEARISE
def f_lin(x, t):
    return A4 @ x

t = np.linspace(0, 240, 5000)
Xlin = odeint(f_lin,x0_lin,t)

alpha_lin = aoa1 + Xlin[:,0]
q_lin     = Xlin[:,1]
Va_lin    = Va1 + Xlin[:,2]
gamma_lin = Xlin[:,3]
theta_lin = alpha_lin + gamma_lin


# TRIM 2 : point différent
avion2 = aero_model.Airbus_A321_200(atm)
avion2.set_mass_from_km(1.0)
avion2.set_static_margin(0.10)
h2 = 10000
mach2 = 0.78
Va2 = atm.tas_from_mach_altp(mach2,h2)

trim2 = dynamic.get_trim_level_flight(avion2,h2,Va2)
aoa2   = trim2["aoa"][0]
dtrim2 = trim2["dtrim"][0]
dthr2  = trim2["dthr"][0]

Xe2 = np.array([aoa2,0.0, Va2,0.0,h2,0.0,avion2.get_mass()])
Ue2 = np.array([dtrim2,0.0,dthr2])

# PERTURBATION IDENTIQUE
delta_alpha2 = np.arctan(Wh / Va2)
X0_nl = Xe2.copy()
X0_nl[0] += delta_alpha2


# SIMULATION NON LINEAIRE
Xnl = odeint(dynamic.get_state_dot,X0_nl,t,args=(Ue2, avion2))
alpha_nl = Xnl[:,0]
q_nl     = Xnl[:,1]
Va_nl    = Xnl[:,2]
gamma_nl = Xnl[:,3]
theta_nl = alpha_nl + gamma_nl


# COMPARAISON
plt.figure(figsize=(10,8))
plt.subplot(411)
plt.plot(t,Va_nl,label="Non linéaire (Trim 2)")
plt.plot(t,Va_lin,'--',label="Linéaire (Trim 1)")
plt.ylabel("Va (m/s)")
plt.legend()
plt.grid()

plt.subplot(412)
plt.plot(t,np.rad2deg(alpha_nl),label="Non linéaire")
plt.plot(t,np.rad2deg(alpha_lin),'--',label="Linéaire")
plt.ylabel("α (deg)")
plt.grid()


plt.subplot(413)
plt.plot(t,np.rad2deg(theta_nl))
plt.plot(t,np.rad2deg(theta_lin),'--')
plt.ylabel("θ (deg)")
plt.grid()


plt.subplot(414)
plt.plot(t,np.rad2deg(q_nl))
plt.plot(t,np.rad2deg(q_lin),'--')

plt.ylabel("q (deg/s)")
plt.xlabel("Temps (s)")
plt.grid()

plt.tight_layout()
plt.show()