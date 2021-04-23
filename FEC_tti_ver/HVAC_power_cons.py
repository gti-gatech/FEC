# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from collections import OrderedDict

# The inputs assumed by this module (The following variable are there for testing purposes and not used by the module)
# ambient_temperature_degree_f = 87.3
# relative_humidity = 53.8

# The deviation from Excel sheet in this module is that this module assumes the ASHRAE Pychometric chart is constant
# So it skips some of the initial computations

# <codecell>

COMFORT_ZONE_TD_F = 75
COMFORT_ZONE_RHD_PERCENT = 50
DELTA_H_BY_DELTA_T = OrderedDict( 
                       ((10, 0.7083333333333), 
                       (30, 1.0138888888888), 
                       (50, 1.3194444444444), 
                       (70, 1.625), 
                       (90, 1.9305555555555)) 
                      )

DELTA_H_BY_DELTA_RH = OrderedDict( 
                       ((32, 0.10), 
                        (50, 0.1875), 
                        (68, 0.3625), 
                        (86, 0.70), 
                        (104, 1.20)) 
                      )

# <codecell>

def get_hvac_power_cons(ambient_temperature_degree_f, relative_humidity):
    temp_diff = ambient_temperature_degree_f - COMFORT_ZONE_TD_F
    h_for_cooling = 0.0
    for relative_humidity_cutoff_point in DELTA_H_BY_DELTA_T.keys():
        if relative_humidity <= relative_humidity_cutoff_point:
            h_for_cooling = temp_diff * DELTA_H_BY_DELTA_T[relative_humidity_cutoff_point]
            break
    adjusted_h_for_cooling = 0.0
    if h_for_cooling > 0:
        adjusted_h_for_cooling = h_for_cooling * (1 + (1.0/2.75))
    humidity_diff = relative_humidity - COMFORT_ZONE_RHD_PERCENT
    h_for_dehumidif = 0.0
    for temp_cutoff_point in DELTA_H_BY_DELTA_RH.keys():
        if ambient_temperature_degree_f <= temp_cutoff_point:
            h_for_dehumidif = humidity_diff * DELTA_H_BY_DELTA_RH[temp_cutoff_point]
            break
    adjusted_h_for_dehumidif = 0.0
    if h_for_dehumidif > 0:
        adjusted_h_for_dehumidif = h_for_dehumidif
    sum_h = adjusted_h_for_cooling + adjusted_h_for_dehumidif
    power_consumption_for_heating_and_or_ac = 1.15 * 0.28 * sum_h/2.0
    electic_drive_coolant_hot_enough = 1.15 * 0.28 * abs(h_for_cooling)/2.0
    electic_drive_coolant_not_hot_enough = 1.15 * 0.28 * (abs(h_for_cooling) + abs(h_for_dehumidif))/2.0
    return power_consumption_for_heating_and_or_ac, electic_drive_coolant_hot_enough, electic_drive_coolant_not_hot_enough

# <codecell>


