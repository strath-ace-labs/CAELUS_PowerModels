from math import mean
from .charge_prof import charge_prof

# %% Read Input for Landings
# landings = [[2021 08 17 00 00 00] 60 1;
#             [2021 08 17 01 00 00] 60 1;
#             [2021 08 17 02 00 00] 99 1;
#             [2021 08 17 03 00 00] 20 2;
#             [2021 08 17 04 00 00] 90 1;
#             [2021 08 17 05 00 00] 50 2;
#             [2021 08 17 06 00 00] 30 1;
#             [2021 08 17 07 00 00] 10 1;
#             [2021 08 17 08 00 00] 90 1;
#             [2021 08 17 09 00 00] 80 2;
#             [2021 08 17 10 00 00] 50 1;
#             [2021 08 17 11 00 00] 10 0.5;
#             [2021 08 17 12 00 00] 60 1;
#             [2021 08 17 13 00 00] 60 1;
#             [2021 08 17 14 00 00] 99 1;
#             [2021 08 17 15 00 00] 20 2;
#             [2021 08 17 16 00 00] 90 1;
#             [2021 08 17 17 00 00] 50 2;
#             [2021 08 17 18 00 00] 30 1;
#             [2021 08 17 19 00 00] 10 1;
#             [2021 08 17 20 00 00] 90 1;
#             [2021 08 17 21 00 00] 80 2;
#             [2021 08 17 22 00 00] 50 1;
#             [2021 08 17 23 00 00] 10 0.5
#             ];
 
# %         landings = [[2021 08 17 00 00 00] 99 1
# %             ];

"""
Make the timestamp right
"""
def balance_time(timestamp_array):
    pass

def hour(timestamp_array):
    return timestamp_array[3]
    
def demand_schedule(landings, base_load = 0):
    #  Define Auxilliary (Base Load)

    # Build Demand Profile
    GC_temp = []
    GC_prof = []
    GC_prof_temp = []
    for x in range(24):
        # 0 hour profile
        # 1 Average power profile
        # 2 Peak power profile
        # 3 Energy Profile
        GC_prof.append([x, 0, 0, 0])
        GC_prof_temp.append([x, 0, 0, 0])

    for i in range(len(landings)):
        
        tstart, DoD, Crate = landings[i]
        GC_temp = charge_prof(tstart, DoD, Crate) 
        
        for j in range(len(GC_temp)):
            tstamp = balance_time(GC_temp[j][0])
            avg_power_prof = [row[1] for row in GC_temp]
            GC_prof_temp[hour(tstamp)][1] = mean(avg_power_prof) # Update Average Power
            GC_prof_temp[hour(tstamp)][2] = max(avg_power_prof) # Update Peak Power Demand
            GC_prof_temp[hour(tstamp)][3] = GC_prof_temp[hour(tstamp)][3] + GC_temp[j][3] # Update Energy Demand

        custom_add = lambda r0, r1: [r0[0]] + sum(zip(r0[1:], r1[1:]))

        GC_prof = [
            custom_add(gc_prof_row, gc_prof_temp_row) for gc_prof_row, gc_prof_temp_row in zip(GC_prof, GC_prof_temp)
        ]
        
    return GC_prof

# % yyaxis left
# plot(GC_prof(:, 1), GC_prof(:, 4))  % plot Energy Demand
# hold on

# % yyaxis right
# % plot(GC_prof(:, 1), GC_prof(:, 2))  % plot Average Power Demand
# % hold on
# grid on;