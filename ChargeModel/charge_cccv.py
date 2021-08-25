from .batt_chg_cell import batt_chg_cell
from math import inf

def charge_cccv(depth_of_discharge, c_rate) -> float:
    """
    param depth_of_discharge: int 0-100
    param c_rate: float
    """

    Q = 22 # Capacity
    I_1C = 22 # 1C rating of battery: A
    Vnom = 3.7 # Nominal Voltage: V
    Vmax = 4.2 # Max/Charge Voltage: V
    Vcut = 2.75 # Battery  cut-off voltage

    # Battery Charge Profile: CC - CV
    Icc = c_rate*I_1C # Constant Current: C-rating

    CVprof = [
        [1, 10/60],
        [2, 6/60]
    ]

    CVprof = [
        [CVprof[1][1], CVprof[1][2], (CVprof[1][1] * CVprof[1][2]), CVprof[1][1]**2, CVprof[1][2]**2],
        [CVprof[2][1], CVprof[2][2], (CVprof[2][1] * CVprof[2][2]), CVprof[2][1]**2, CVprof[2][2]**2]
    ]

    # What operation is this?
    Ex = sum([row[0] for row in CVprof]); # Sum of x values
    Ey = sum([row[1] for row in CVprof]); # Sum of y values
    Exy = sum([row[2] for row in CVprof]); # Sum of x.y values
    Ex2 = sum([row[3] for row in CVprof]); # Sum of x2 values
    Ey2 = sum([row[4] for row in CVprof]); # Sum of y2 values

    c =  ( (Ey*Ex2)-(Ex*Exy) )/ ( (len(CVprof[0])*Ex2)-(Ex**2) ); # Calculate tau intercept
    m = ( (len(CVprof[0])*Exy) - (Ex*Ey) ) / ( (len(CVprof[0])*Ex2)-(Ex**2) ); # calculate tau gradient

    tau = (m*(Icc/I_1C)) + c

    Xmax = -c/m; # Maximum Charging current to allow

    T = inf;  # hours
    dT = 1/3600;     # model sample time: seconds
    t = 0

    # Constant Current Period
    DoDinit = depth_of_discharge #Battery DoD at start: 
    Vbatt = 2.76

    while Vbatt < (Vmax*1):
        If = -Icc
        It = ((DoDinit/100)*Q)+(If*t)     # Extracted Capacity: Ah
        Vbatt = batt_chg_cell(It, If)
        Ibatt = Icc
        tcc = t
        t = t+dT
    
    return t