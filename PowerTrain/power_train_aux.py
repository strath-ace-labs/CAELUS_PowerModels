def powertrain_aux(d_a, d_e, d_r, dT) -> [float, float]:

    Ia = 400e-6/Vbatt  # Aeileron power consumption (max power selected)
    Ir = 50e-6/Vbatt   # Rudder power consumption (max power selected)
    Ie = 3.4e-6/Vbatt  # Elevator power consumption (max power selected)

    Iuc = 60/Vbatt     # Parasistic/Avionics load (specified by Avy, Please Confirm !!)


    Idis = (d_a*Ia) + (d_e*Ie) + (d_r*Ir) + Iuc
    Qcon = Idis*dT
    
    return Qcon, Idis

