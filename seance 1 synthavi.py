import aero_model 
import numpy as np
import matplotlib.pyplot as plt


aero_m = aero_model.Airbus_A319_100()
print(f'{aero_m.name}')
aero_m.set_options(stall=False, buffeting=False, wave_drag=False)
aero_m.set_mass(aero_m.m_design) 
aero_m.set_static_margin(0.2) 
mach, q, tas, dm = aero_m.mach_design, 0, aero_m.atm.tas_from_mach_altp(aero_m.mach_design, aero_m.altp_ref), 0        #la TAS ne doit pas être nulle
aoa_range = np.linspace(np.deg2rad(-10), np.deg2rad(20), 100)
for dtrim in [np.deg2rad(-12),np.deg2rad(7)]:
    cz_list = []
    for aoa in aoa_range:
        cz, cx, cm = aero_m.get_aero_coefs(aoa, mach, dtrim, dm, q, tas)
        cz_list.append(cz)
        # Tracé
    plt.plot(np.rad2deg(aoa_range), cz_list,
             label=f"δtrim = {np.rad2deg(dtrim):.0f}°")

plt.xlabel("Angle d'attaque α (deg)")
plt.ylabel("Coefficient de portance CL")
plt.title("CL en fonction de α pour différents δtrim")
plt.grid(True)
plt.legend()
plt.show()




aero_m = aero_model.Airbus_A319_100()
print(f'{aero_m.name}')
aero_m.set_options(stall=False, buffeting=False, wave_drag=False)
aero_m.set_mass(aero_m.m_design) 
aero_m.set_static_margin(0.2) 
machlist, q, dtrim, dm = [0.6,0.8], 0,0, 0        #la TAS ne doit pas être nulle
aoa_range = np.linspace(np.deg2rad(-10), np.deg2rad(20), 100)
for ma in machlist:
    tas=aero_m.atm.tas_from_mach_altp(ma, aero_m.altp_ref)
    cz_list = []
    cx_list=[]
    for aoa in aoa_range:
        cz, cx, cm = aero_m.get_aero_coefs(aoa, ma, dtrim, dm, q, tas)
        cz_list.append(cz)
        cx_list.append(cx)
    plt.plot(cx_list, cz_list, label=f"Mach {ma}")

plt.xlabel("Coefficient trainée Cd")
plt.ylabel("Coefficient de portance CL")
plt.title("Polaire aérodynamique CL = f(CD) (δtrim = 0) pour différentes incidence alpha")
plt.legend()
plt.grid(True)
plt.show()


aero_m = aero_model.Airbus_A319_100()
print(f'{aero_m.name}')
aero_m.set_options(stall=True, buffeting=False, wave_drag=False)
aero_m.set_mass(aero_m.m_design) 
aero_m.set_static_margin(0.2) 
machlist, q, dtrim, dm = [0.6,0.8], 0,0, 0        #la TAS ne doit pas être nulle
aoa_range = np.linspace(np.deg2rad(-10), np.deg2rad(20), 100)
for ma in machlist:
    tas=aero_m.atm.tas_from_mach_altp(ma, aero_m.altp_ref)
    cz_list = []
    cx_list=[]
    for aoa in aoa_range:
        cz, cx, cm = aero_m.get_aero_coefs(aoa, ma, dtrim, dm, q, tas)
        cz_list.append(cz)
        cx_list.append(cx)
    plt.plot(cx_list, cz_list, label=f"Mach {ma}")

plt.xlabel("Coefficient trainée Cd")
plt.ylabel("Coefficient de portance CL")
plt.title("Polaire aérodynamique CL = f(CD) (δtrim = 0) pour différentes incidence alpha")
plt.legend()
plt.grid(True)
plt.show()


aero_m = aero_model.Airbus_A319_100()
print(f'{aero_m.name}')
aero_m.set_options(stall=False, buffeting=False, wave_drag=True)
aero_m.set_mass(aero_m.m_design) 
aero_m.set_static_margin(0.2) 
machlist, q, dtrim, dm = [0.6,0.8], 0,0, 0        #la TAS ne doit pas être nulle
aoa_range = np.linspace(np.deg2rad(-10), np.deg2rad(20), 100)
for ma in machlist:
    tas=aero_m.atm.tas_from_mach_altp(ma, aero_m.altp_ref)
    cz_list = []
    cx_list=[]
    for aoa in aoa_range:
        cz, cx, cm = aero_m.get_aero_coefs(aoa, ma, dtrim, dm, q, tas)
        cz_list.append(cz)
        cx_list.append(cx)
    plt.plot(cx_list, cz_list, label=f"Mach {ma}")

plt.xlabel("Coefficient trainée Cd")
plt.ylabel("Coefficient de portance CL")
plt.title("Polaire aérodynamique CL = f(CD) (δtrim = 0) pour différentes incidence alpha")
plt.legend()
plt.grid(True)
plt.show()


aero_m = aero_model.Airbus_A319_100()
print(f'{aero_m.name}')
aero_m.set_options(stall=False, buffeting=False, wave_drag=False)
aero_m.set_mass(aero_m.m_design) 
mach, q, tas,dtrim, dm = aero_m.mach_design, 0, aero_m.atm.tas_from_mach_altp(aero_m.mach_design, aero_m.altp_ref),0, 0        #la TAS ne doit pas être nulle
aoa_range = np.linspace(np.deg2rad(-10), np.deg2rad(20), 100)
for ms in [0.7,0.2,0,-0.3]:
    aero_m.set_static_margin(ms)
    cm_list = []
    for aoa in aoa_range:
        cz, cx, cm = aero_m.get_aero_coefs(aoa, mach, dtrim, dm, q, tas)
        cm_list.append(cm)
        # Tracé
    plt.plot(np.rad2deg(aoa_range), cm_list,
             label=f"ms = {ms}")

plt.xlabel("Angle d'attaque α (deg)")
plt.ylabel("Coefficient de moment de tangage Cm")
plt.title("Cm en fonction de α pour différents ms")
plt.grid(True)
plt.legend()
plt.show()


aero_m = aero_model.Airbus_A319_100()
aero_m.set_options(stall=False, buffeting=False, wave_drag=False)
aero_m.set_mass(aero_m.m_design)

mach,q,tas,dm = aero_m.mach_design,0, aero_m.atm.tas_from_mach_altp(aero_m.mach_design, aero_m.altp_ref),0
aoa_range = np.linspace(np.deg2rad(-10), np.deg2rad(20), 100)

for ms in [0.7, 0.2, 0, -0.3]:
    aero_m.set_static_margin(ms)
    dtrim_list = []
    cm_list = []
    
    for aoa in aoa_range:
        # trim condition Cm = 0
        dtrim_e = -(aero_m.cm0 + aero_m.cma * (aoa - aero_m.a0)) / aero_m.cmtrim

        # stockage
        dtrim_list.append(np.rad2deg(dtrim_e))

        # calcul Cm avec trim équilibré (doit être ~0)
        cz, cx, cm = aero_m.get_aero_coefs(aoa, mach, dtrim_e, dm, q, tas)
        cm_list.append(cm)

    plt.plot(np.rad2deg(aoa_range), dtrim_list, label=f"ms = {ms}")

plt.xlabel("Incidence α (deg)")
plt.ylabel("δtrim,e (deg)")
plt.title("Commande de trim d’équilibre en fonction de α")
plt.grid(True)
plt.legend()
plt.show()




aero_m = aero_model.Airbus_A319_100()
aero_m.set_options(stall=False, buffeting=False, wave_drag=False)
aero_m.set_mass(aero_m.m_design)

mach,q,tas,dm = aero_m.mach_design,0, aero_m.atm.tas_from_mach_altp(aero_m.mach_design, aero_m.altp_ref),0
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


aero_m = aero_model.Airbus_A319_100()
print(f'{aero_m.name}')
aero_m.set_options(stall=True, buffeting=False, wave_drag=False)
aero_m.set_mass(aero_m.m_design) 
aero_m.set_static_margin(0.2) 
mach,q,tas,dm = aero_m.mach_design,0, aero_m.atm.tas_from_mach_altp(aero_m.mach_design, aero_m.altp_ref),0
aoa_range = np.linspace(np.deg2rad(-10), np.deg2rad(20), 100)
for ms in [0.7, 0.2]:
    aero_m.set_static_margin(ms)
    cze_list = []
    cxe_list=[]
    for aoa in aoa_range:
        # trim condition Cm = 0
        dtrim_e = -(aero_m.cm0 + aero_m.cma * (aoa - aero_m.a0)) / aero_m.cmtrim

        # stockage
        dtrim_list.append(np.rad2deg(dtrim_e))
        cze, cxe, cme = aero_m.get_aero_coefs(aoa, mach,dtrim_e, dm, q, tas)
        cze_list.append(cze)
        cxe_list.append(cxe)
    cz_list = np.array(cze_list)
    cx_list = np.array(cxe_list)

        # finesse
    finesse = cz_list / cx_list
    fmax = np.max(finesse)
    plt.plot(cx_list, cz_list, label=f"ms {ms}")
print(fmax)
plt.xlabel("Coefficient trainée Cde")
plt.ylabel("Coefficient de portance CLe")
plt.title("Polaire équilibrée CLe = f(CDe) (δtrim = 0) pour différentes incidence alpha")
plt.legend()
plt.grid(True)
plt.show()






    
