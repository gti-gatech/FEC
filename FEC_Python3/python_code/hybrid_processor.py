# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# This cell shall need to be removed once the development on this module is done.
#import data_reader as dr
import constants as c
#import math
import pandas as pd
import bin_processor
#import bin_processor_series
#import numpy as np
#import pandas as pd
import util

from HVAC_power_cons import get_hvac_power_cons


# Constants defined here
POWER = 'Power(kW)'
ACC = 'Acc'
JERK = 'Jerk'
COASTING = 'Coasting'
BRAKING = 'Braking'
IDLE = 'Idle'
CRUISE = 'Cruise'
GEN_FLAG_1 = 'GEN flag1'
GEN_FLAG_2 = 'GEN flag2'
EE_A = 'EE A'
EE_RB1 = 'EE RB1'
EE_RB2 = 'EE RB2'
EE_GEN = 'EE GEN'
ENG_TRACT = 'Eng_Tract'
FUEL_FLAG = 'Fuel flag'
SOC = 'SOC'
OLD_BIN = 'Old Bin'
NEW_BIN = 'New Bin'
B_OUT = 'B_out'
RB_FLAG = 'RB_Flag'
ENG = 'Eng'
B_IN = 'B_in'
SOC = 'SOC'
SOC_LOW = 'SOC_low'
SOC_HG = 'SOC_hg'
DERR = 'dErr'
SIGERR = 'sigErr'
NEW_BIN_1 = 'new_bin_1'

# Column Names for series
B_OUT_SERIES      = 'B_out_series'
RB_FLAG_SERIES    = 'RB_Flag_series'
ENG_SERIES        = 'Eng_series'
B_IN_SERIES       = 'B_in_series'
SOC_SERIES        = 'SOC_series'
SOC_LOW_SERIES    = 'SOC_low_series'
SOC_HG_SERIES     = 'SOC_hg_series'
DERR_SERIES       = 'dErr_series'
SIGERR_SERIES     = 'sigErr_series'
NEW_BIN_SERIES    = 'New Bin_series'
NEW_BIN_1_SERIES  = 'New Bin 1_series'
ENG_TMP_SERIES    = 'Eng_tmp_series'
CYCLE_OBSERVED_WORK = 'CycleObservedWork'

ABS_TRACTIVE_POWER = 'Abs Trctv Pwr'


# Some constants from the Hybrid Processor sheet for Parallel
BUS_LENGTH_PARALLEL = 40
#BUS_WEIGHT_PARALLEL = c.SOURCE_MASS_METRIC_TONNES * c.HEV_TO_SI_CI_WEIGHT_FACTOR
SPD_WIN_1_MPH_PARALLEL = 10
SPD_WIN_2_MPH_PARALLEL = 20
SPD_WIN_3_MPH_PARALLEL = 30
SPD_WIN_4_MPH_PARALLEL = 40
ACC_THRSH_1_MPHS_PARALLEL = 2.5
ACC_THRSH_2_MPHS_PARALLEL = ACC_THRSH_1_MPHS_PARALLEL * 0.25
ACC_THRSH_3_MPHS_PARALLEL = ACC_THRSH_2_MPHS_PARALLEL * 0.25
ACC_THRSH_4_MPHS_PARALLEL = ACC_THRSH_3_MPHS_PARALLEL * -0.25
EM_CRUISE_BLEND_PARALLEL = 0.0
GEN_COEFF_1_PARALLEL = 7.00
GEN_COEFF_2_PARALLEL = 8.00
SOC_BASE_PERCENT_PARALLEL = 60
SOC_MIN_PERCENT_PARALLEL = 50
SOC_DELTA_PERCENT_PARALLEL = 8
EPT_EFFICIENCY_PERCENT_PARALLEL = 86.6
EM_PWR_KW = 280
ENG_PWR_KW = 280
BATT_CAP_KW_SEC = 576000
SOC_START_VALUE = 60.0


# Some Constants for the Series case
BUS_LENGTH_SERIES = 40
EM1_PWR_KW_SERIES = 280
ENG_PWR_KW_SERIES = 280
BATT_CAP_KW_SEC_SERIES = 576000
CP1_SERIES = 2.00
CP2_SERIES = 5.00
#BUS_WEIGHT_TONNES_SERIES = c.SOURCE_MASS_METRIC_TONNES * c.HEV_TO_SI_CI_WEIGHT_FACTOR
SOC_BASE_PERCENT_SERIES = 60.0
SOC_MIN_PERCENT_SERIES = SOC_BASE_PERCENT_SERIES - 5
SOC_DELTA_PERCENT_SERIES = 1
EPT_EFFICIENCY_PERCENT_SERIES = 86.6
CD1_SERIES = 2.00
CD2_SERIES = 3.00
CI1_SERIES = 1.00
CI2_SERIES = 7.00

# <codecell>

def get_eng_value(rb_flag, power, prev_soc, prev_to_prev_soc, eng_tmp, prev_eng, prev_power, old_bin, dErr_prev, sigErr_prev):
    if rb_flag:
        value = 0.0
    else:
        term1 = max((1.1 * max(dErr_prev/100.0, 0)*BATT_CAP_KW_SEC_SERIES) + CP1_SERIES*(SOC_BASE_PERCENT_SERIES - prev_soc) + CI1_SERIES*sigErr_prev + CD1_SERIES * max(dErr_prev, 0), eng_tmp)
        term = min(term1, 200)
        term2 = max((1.1 * max(dErr_prev/100.0, 0)*BATT_CAP_KW_SEC_SERIES) + CP2_SERIES*(SOC_BASE_PERCENT_SERIES - prev_soc) + CI2_SERIES*sigErr_prev + CD2_SERIES * max(dErr_prev, 0), eng_tmp)
        term22 = min(term2, 200)

        if prev_soc < SOC_MIN_PERCENT_SERIES:
            if power>0 and old_bin != 1:
                if power == prev_power or term22 < 1.1 * eng_tmp:
                        value = eng_tmp
                else:
                        value = term22
            else:
                value = 0.0
        else:
            if (prev_to_prev_soc < SOC_BASE_PERCENT_SERIES) and \
               (prev_to_prev_soc < (SOC_BASE_PERCENT_SERIES - SOC_DELTA_PERCENT_SERIES)) and \
               (prev_soc < SOC_BASE_PERCENT_SERIES) and \
               (prev_soc < (SOC_BASE_PERCENT_SERIES - SOC_DELTA_PERCENT_SERIES)) and \
               (prev_soc >= SOC_MIN_PERCENT_SERIES):

                if power>0 and old_bin != 1:
                    if power == prev_power or term < 1.1 * eng_tmp:
                            value = eng_tmp
                    else:
                            value = term
                else:
                        value = 0.0
    
            else:
                if (power > 0) and \
                   (old_bin != 1) and \
                   (prev_to_prev_soc < SOC_BASE_PERCENT_SERIES + 1.2) and \
                   (prev_to_prev_soc > (SOC_BASE_PERCENT_SERIES - SOC_DELTA_PERCENT_SERIES)) and \
                   (prev_soc < SOC_BASE_PERCENT_SERIES + 1.2) and \
                   (prev_soc > (SOC_BASE_PERCENT_SERIES - SOC_DELTA_PERCENT_SERIES)) and \
                   (prev_soc >= SOC_MIN_PERCENT_SERIES):
                    value = min(max(1.1 * power, eng_tmp), 200)
                else:
                    if (power <= 0 or ((prev_to_prev_soc > SOC_BASE_PERCENT_SERIES+1.2) and (prev_soc > SOC_BASE_PERCENT_SERIES+1.2))):
                        value =0.0
                    else:
                        value = max(eng_tmp, prev_eng)
    return min(ENG_PWR_KW_SERIES, value)

# <codecell>

def get_eng_temp(prev_soc, oldbin,FIXED_MASS_FACTOR):
    if prev_soc > (SOC_BASE_PERCENT_SERIES + 1):
        return 0
    else:
        lookup = {
                     1      :     0*FIXED_MASS_FACTOR*1.5,
                    12      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 3),
                    13      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 6),
                    14      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 9),
                    15      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 12),
                    16      :     min(ENG_PWR_KW_SERIES, 0.8 * FIXED_MASS_FACTOR * 15),
                    22      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 3),
                    23      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 6),
                    24      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 9),
                    25      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 12),
                    27      :     min(ENG_PWR_KW_SERIES, 0.8 * FIXED_MASS_FACTOR * 15),
                    28      :     min(ENG_PWR_KW_SERIES, 0.8 * FIXED_MASS_FACTOR * 21),
                    29      :     min(ENG_PWR_KW_SERIES, 0.8 * FIXED_MASS_FACTOR * 27),
                    30      :     min(ENG_PWR_KW_SERIES, 0.8 * FIXED_MASS_FACTOR * 30),
                    33      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 5.5),
                    35      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 12),
                    37      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 15),
                    38      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 21),
                    39      :     min(ENG_PWR_KW_SERIES, FIXED_MASS_FACTOR * 27),
                    40      :     min(ENG_PWR_KW_SERIES, 0.8 * FIXED_MASS_FACTOR * 30)
                 }
        try:
            if oldbin in (1, 12, 13, 14, 15, 16):
                if prev_soc < (SOC_BASE_PERCENT_SERIES+1):
                    return lookup[oldbin]
                else:
                    return 0
            else:
                return lookup[oldbin]
        except Exception as excep:
            #print "EXCEPTION " + str(e)
            return 0
    return 0

# <codecell>

def get_binned_data_hybrid(speeds, 
                           number_of_passengers,
                           ambient_temperature_degree_f,
                           relative_humidity,
                           idle_speed_range,
                           roughness_index,
                           FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR):
    AUX_E_LOAD = get_hvac_power_cons(ambient_temperature_degree_f, relative_humidity)[0] * c.PARALLEL_MECHANICAL_ELECTRICAL_EFFICIENCY_TRANSIT_BUS
    AUX_E_LOAD_SERIES = get_hvac_power_cons(ambient_temperature_degree_f, relative_humidity)[0]
    binned_data_df, bins, data_table =  bin_processor.get_binned_data(speeds, number_of_passengers, idle_speed_range, roughness_index,FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR)
    # Add the fields (columns) as mentioned in the HybridProcessor module (The same naming convention has been used)
    data_table[POWER] = data_table.stp * FIXED_MASS_FACTOR
    data_table[ACC] = data_table.speed - data_table.speed.shift()
    data_table.loc[0, ACC] = data_table.loc[1, ACC]
    data_table[JERK] = data_table[ACC] - data_table[ACC].shift()
    data_table.loc[data_table[ACC].shift() < 0, JERK] = 0.0
    data_table.loc[0, JERK] = 0.0
    # OLD BIN Calculation
    data_table[OLD_BIN] = data_table.BinNo
    # Coasting calculation
    # If the bin number was 11 or 21, the coasting is True (represented by Y in Excel sheet)
    data_table[COASTING] = data_table.speed.astype(bool)
    data_table[COASTING] = False
    data_table.loc[(data_table[OLD_BIN] == 11) | (data_table[OLD_BIN] == 21), COASTING] = True
    # Braking Calculation
    data_table[BRAKING] = data_table[COASTING]
    data_table[BRAKING] = False
    data_table.loc[data_table[OLD_BIN] == 0, BRAKING] = True
    # Idle Calculation
    data_table[IDLE] = data_table[COASTING]
    data_table[IDLE] = False
    data_table.loc[data_table[OLD_BIN] == 1, IDLE] = True
    # Cruise Calculation
    data_table[CRUISE] = data_table[COASTING]
    data_table[CRUISE] = False
    data_table.loc[(data_table[OLD_BIN] != 11)      & (data_table[OLD_BIN] != 21) & \
                       (data_table[OLD_BIN] != 0)       & (data_table[OLD_BIN] != 1)  & \
                       (data_table.acceleration <= 1.0) & (data_table[JERK] <= 1.0), CRUISE] = True
    # GEN flag1, GEN flag2, EE A ... SOC have circular dependency and thus can't 
    # simply be written in Pandas high level statements (If it can be done I do not know about it)

    data_table[GEN_FLAG_1] = data_table[COASTING]
    data_table[GEN_FLAG_2] = data_table[COASTING]
    data_table[EE_A] = data_table[POWER]
    data_table[EE_RB1] = data_table[POWER]
    data_table[EE_RB2] = data_table[POWER]
    data_table[EE_GEN] = data_table[POWER]
    data_table[ENG_TRACT] = data_table[POWER]
    data_table[SOC] = data_table[POWER]
    data_table[FUEL_FLAG] = data_table[COASTING]

    # Start out by initlializing values some assumed values (This hardcoding is as per excel sheet)
    data_table.loc[0, GEN_FLAG_1] = False
    data_table.loc[0, GEN_FLAG_2] = False
#    data_table.ix[1, GEN_FLAG_1] = False
#    data_table.ix[1, GEN_FLAG_2] = False

    data_table.loc[0, SOC] = 60.00
    prev_eng_tract = 0.0
    prev_soc = 60.0
 
    data_table_dict = data_table.to_dict()
    for index_no in range(len(data_table)):
        coasting   = data_table_dict[COASTING][index_no]
        braking    = data_table_dict[BRAKING][index_no]
        idle       = data_table_dict[IDLE][index_no]
        cruise     = data_table_dict[CRUISE][index_no]
        gen_flag_1 = data_table_dict[GEN_FLAG_1][index_no]
        power      = data_table_dict[POWER][index_no]
        speed      = data_table_dict['speed'][index_no]
        acceleration = data_table_dict['acceleration'][index_no]

#        if index_no != 0 and index_no != 1:
        if index_no != 0:
            # GEN FLAG 1
            if(braking):
                data_table_dict[GEN_FLAG_1][index_no] = False
            else:
                if prev_soc >= (SOC_MIN_PERCENT_PARALLEL + SOC_DELTA_PERCENT_PARALLEL):
                    data_table_dict[GEN_FLAG_1][index_no] = False
                else:
                    data_table_dict[GEN_FLAG_1][index_no] = True
            # GEN FLAG 2
            if(prev_soc >= SOC_BASE_PERCENT_PARALLEL or not data_table_dict[GEN_FLAG_1][index_no]):
                data_table_dict[GEN_FLAG_2][index_no] = False
            else:
                data_table_dict[GEN_FLAG_2][index_no] = True
#        print data_table_dict[GEN_FLAG_1]
    
        # EE A
        if(not coasting and not braking and not idle and not data_table_dict[GEN_FLAG_2][index_no]):
            if((speed < SPD_WIN_1_MPH_PARALLEL  and acceleration < ACC_THRSH_1_MPHS_PARALLEL) or \
               (speed >= SPD_WIN_1_MPH_PARALLEL and speed < SPD_WIN_2_MPH_PARALLEL and acceleration < ACC_THRSH_2_MPHS_PARALLEL) or 
               (speed >= SPD_WIN_2_MPH_PARALLEL and speed < SPD_WIN_3_MPH_PARALLEL and acceleration < ACC_THRSH_3_MPHS_PARALLEL) or
               (speed >= SPD_WIN_3_MPH_PARALLEL and speed < SPD_WIN_4_MPH_PARALLEL and acceleration < ACC_THRSH_4_MPHS_PARALLEL)):
                data_table_dict[EE_A][index_no]  = min(power, EM_PWR_KW * EPT_EFFICIENCY_PERCENT_PARALLEL/100.0)
            else:
                if cruise:
                    data_table_dict[EE_A][index_no] = power * (EM_CRUISE_BLEND_PARALLEL/100.0)
                else:
                    data_table_dict[EE_A][index_no] = 0.0
        else:
            data_table_dict[EE_A][index_no] = 0.0

        # EE RB1
        if braking:
            if (abs(power)*EPT_EFFICIENCY_PERCENT_PARALLEL/100.0) < EM_PWR_KW:
                data_table_dict[EE_RB1][index_no] = abs(power)
            else:
                data_table_dict[EE_RB1][index_no] = EM_PWR_KW/(EPT_EFFICIENCY_PERCENT_PARALLEL/100.0)
        else:
            data_table_dict[EE_RB1][index_no] = 0.0

        # EE RB2
        if braking:
            if( data_table_dict[EE_RB1][index_no] + ((prev_soc/100.0) * BATT_CAP_KW_SEC) > BATT_CAP_KW_SEC):
                data_table_dict[EE_RB2][index_no] = BATT_CAP_KW_SEC - ((prev_soc/100.0) * BATT_CAP_KW_SEC)
            else:
                data_table_dict[EE_RB2][index_no] = data_table_dict[EE_RB1][index_no]
        else:
            data_table_dict[EE_RB2][index_no] = 0.0

        # EE GEN
        if data_table_dict[GEN_FLAG_2][index_no]:
            data_table_dict[EE_GEN][index_no] = min(EM_PWR_KW, GEN_COEFF_1_PARALLEL * (SOC_BASE_PERCENT_PARALLEL - prev_soc))
        else:
            data_table_dict[EE_GEN][index_no] = 0.0

        # ENG Tract
        if not braking:
            if (data_table_dict[EE_GEN][index_no] > 0.0):
                if coasting:
                    data_table_dict[ENG_TRACT][index_no] = prev_eng_tract
                else:
                    data_table_dict[ENG_TRACT][index_no] = power + data_table_dict[EE_GEN][index_no]
            else:
                data_table_dict[ENG_TRACT][index_no] = max(power - data_table_dict[EE_A][index_no], 0)
        else:
            data_table_dict[ENG_TRACT][index_no] = 0.0

        # Fuel Flag
        if not braking:
            if data_table_dict[ENG_TRACT][index_no] > 0:
                data_table_dict[FUEL_FLAG][index_no] = True
            else:
                data_table_dict[FUEL_FLAG][index_no] = False 
        else:
            data_table_dict[FUEL_FLAG][index_no] = False

        # SOC
        if index_no != 0:
            data_table_dict[SOC][index_no] = prev_soc + \
                ((( \
                    (data_table_dict[EE_RB2][index_no] + data_table_dict[EE_GEN][index_no]) * \
                    (EPT_EFFICIENCY_PERCENT_PARALLEL/100.0) \
                  ) \
                 - \
                  ( (((data_table_dict[EE_A][index_no])/(EPT_EFFICIENCY_PERCENT_PARALLEL/100.0)) + AUX_E_LOAD) \
                  ) \
                 ) / BATT_CAP_KW_SEC \
                ) * 100.0

        prev_eng_tract = data_table_dict[ENG_TRACT][index_no]
        prev_soc       = data_table_dict[SOC][index_no]
    
    data_table = pd.DataFrame.from_dict(data_table_dict)
#    util.df_to_csv_debug(data_table,"datatable.csv")
    # Calculate NEW Bin
    new_stp = data_table[ENG_TRACT]/FIXED_MASS_FACTOR
    binned_data_df_parallel, bins, data_df =  bin_processor.get_binned_data(speeds, number_of_passengers, idle_speed_range,
                                                                            roughness_index, FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR, new_stp)
    data_table[NEW_BIN] = data_df.BinNo
 #   util.df_to_csv_debug(data_df, "rawbins.csv")
    # Also Calculate the Modified New Bin Column (this field is unnamed in the Excel Sheet)
    data_table[NEW_BIN_1] = data_table[NEW_BIN]
    data_table.loc[data_table[ENG_TRACT] <= 0, NEW_BIN_1] = -1
#    print data_table[NEW_BIN_1]

    # Now adjust the binned_data_df because this is required by energy_consumption module 
    # We shall decrement the count of bins which shall get re-distributed to bin -1 because ENG was <=0
    negative_count = 0
#    print binned_data_df_parallel['CycleBinCounts']

    for index_no in range(len(data_table[NEW_BIN])-1):
        if data_table.loc[index_no+1, ENG_TRACT] <= 0:
 #           if binned_data_df_parallel.ix[data_table.ix[index_no+1, NEW_BIN], 'CycleBinCounts'] > 0:
            binned_data_df_parallel.loc[data_table.loc[index_no+1, NEW_BIN], 'CycleBinCounts'] -= 1
            negative_count += 1
#    if data_table[NEW_BIN_1][0]==-1:
#        binned_data_df_parallel.ix[data_table.BinNo[0], 'CycleBinCounts'] += 1
    
        
#    print negative_count
    # Now adjust the fractions accordingly
#    print negative_count -1 + binned_data_df_parallel['CycleBinCounts'].sum()
    binned_data_df_parallel['Fraction'] = binned_data_df_parallel['CycleBinCounts']/ (negative_count + binned_data_df_parallel['CycleBinCounts'].sum()) *100
    # Now we are going to do the series computation
    data_table[RB_FLAG_SERIES] = data_table[BRAKING]
    data_table[SOC_LOW_SERIES] = data_table[BRAKING]
    data_table[SOC_HG_SERIES] = data_table[BRAKING]
    data_table[B_OUT_SERIES] = data_table[POWER]
    data_table[ENG_TMP_SERIES] = data_table[POWER]
    data_table[SOC_SERIES] = data_table[POWER]
    data_table[DERR_SERIES] = data_table[POWER]
    data_table[SIGERR_SERIES] = data_table[POWER]
    data_table[ENG_SERIES] = data_table[POWER]
    data_table[B_IN_SERIES] = data_table[POWER]

    # The first index has not been defined in the Excel sheet. We shall assume it to be zero
    data_table.loc[0, ENG_TMP_SERIES] = 0
    data_table.loc[0, SOC_SERIES] = SOC_BASE_PERCENT_SERIES
    data_table.loc[0, SOC_HG_SERIES] = False
    data_table.loc[0, DERR_SERIES] = 0
    data_table.loc[0, SIGERR_SERIES] = 0
    derr = 0.0
    # XXX: This value is garbage for the first entry in the Excel. I am assuming it to be 60.0. This can be rechecked.
    prev_to_prev_soc = 60.00
    # Initial ENG values are garbage in the excel sheet. Assuming 0 here
    prev_eng = 0.0
    prev_power = 0.0
    prev_soc = 60.00
    dErr_prev = 0.0
    sigErr_prev = 0.0
    
    data_table_dict = data_table.to_dict()
    # Again we are going to use a For Loop owing to the complexity of the formulae
    for index_no in range(len(data_table)):
        power      = data_table_dict[POWER][index_no]
        speed      = data_table_dict['speed'][index_no]
        acceleration = data_table_dict['acceleration'][index_no]
        rb_flag      = data_table_dict[RB_FLAG_SERIES][index_no]

        # B_out calculation
        data_table_dict[B_OUT_SERIES][index_no] = min(((max(power, 0) / (0.86 * 0.97 * 0.9)) + (AUX_E_LOAD_SERIES/0.9)) , EM1_PWR_KW_SERIES + AUX_E_LOAD_SERIES)  

        # ENG Tmp Calculation
        if index_no != 0:
            data_table_dict[ENG_TMP_SERIES][index_no] = get_eng_temp(prev_soc, data_table_dict[OLD_BIN][index_no], FIXED_MASS_FACTOR)

        data_table_dict[ENG_SERIES][index_no] = get_eng_value(rb_flag, power, prev_soc, prev_to_prev_soc,
                                                         data_table_dict[ENG_TMP_SERIES][index_no], prev_eng, prev_power, 
                                                         data_table_dict[OLD_BIN][index_no], 
                                                         dErr_prev, sigErr_prev)

        # B_in Calculation
        data_table_dict[B_IN_SERIES][index_no] = abs(power * 0.9) if rb_flag else data_table_dict[ENG_SERIES][index_no] * 0.9

        # SOC Calculation
        if index_no != 0:
            data_table_dict[SOC_SERIES][index_no] = 100.0 * ((BATT_CAP_KW_SEC_SERIES * (prev_soc/100.0) - data_table_dict[B_OUT_SERIES][index_no] + data_table_dict[B_IN_SERIES][index_no]) / BATT_CAP_KW_SEC_SERIES)

        # SOC_LOW calculation
        if index_no != 0:
            if prev_soc_low and prev_soc_hg:
                data_table_dict[SOC_LOW_SERIES][index_no] = False
            else:
                if prev_soc_low or prev_soc < SOC_MIN_PERCENT_SERIES:
                    data_table_dict[SOC_LOW_SERIES][index_no] = True
                else:
                    data_table_dict[SOC_LOW_SERIES][index_no] = False
        else:
            if data_table_dict[SOC_SERIES][index_no] < SOC_MIN_PERCENT_SERIES:
                data_table_dict[SOC_LOW_SERIES][index_no] = True
            else:
                data_table_dict[SOC_LOW_SERIES][index_no] = False

        # SOC HG Calculation
        if index_no != 0:
            temp_sum = SOC_MIN_PERCENT_SERIES + SOC_DELTA_PERCENT_SERIES
            if (prev_soc < temp_sum) and (data_table_dict[SOC_SERIES][index_no] >= temp_sum):
                data_table_dict[SOC_HG_SERIES][index_no] = True
            else:
                if data_table_dict[SOC_SERIES][index_no] >= SOC_BASE_PERCENT_SERIES:
                    data_table_dict[SOC_HG_SERIES][index_no] = True
                else:
                    data_table_dict[SOC_HG_SERIES][index_no] = False
        # D Err calculation
        if index_no != 0:
            data_table_dict[DERR_SERIES][index_no] = prev_soc - data_table_dict[SOC_SERIES][index_no]
            derr = derr + data_table_dict[DERR_SERIES][index_no]
            data_table_dict[SIGERR_SERIES][index_no] = derr
        prev_soc_low = data_table_dict[SOC_LOW_SERIES][index_no]
        prev_soc_hg  = data_table_dict[SOC_HG_SERIES][index_no]
        prev_to_prev_soc = prev_soc
        prev_soc     = data_table_dict[SOC_SERIES][index_no]
        prev_eng     = data_table_dict[ENG_SERIES][index_no]
        prev_power   = power
        dErr_prev    = data_table_dict[DERR_SERIES][index_no]
        sigErr_prev  = data_table_dict[SIGERR_SERIES][index_no]
    
    data_table = pd.DataFrame.from_dict(data_table_dict)
    # Calculate NEW Bin
    new_stp = data_table[ENG_SERIES]/(FIXED_MASS_FACTOR * 1.1)
    binned_data_df_series, bins, data_df_series =  bin_processor.get_binned_data(speeds, number_of_passengers, idle_speed_range,
                                                                                        roughness_index, FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR, new_stp)
    data_table[NEW_BIN_SERIES] = data_df_series.BinNo

    # Also Calculate the Modified New Bin Column (this field is unnamed in the Excel Sheet)
    data_table[NEW_BIN_1_SERIES] = data_table[NEW_BIN_SERIES]
    data_table.loc[data_table[ENG_SERIES] <= 0, NEW_BIN_1_SERIES] = -1

    # Now adjust the binned_data_df because this is required by energy_consumption module 
    # We shall decrement the count of bins which shall get re-distributed to bin -1 because ENG was <=0
    negative_count = 0
 #   print binned_data_df_series['CycleBinCounts']
    #util.df_to_csv_debug(data_df_series, "hybrid_processor_data_series.csv")
    for index_no in range(len(data_table[NEW_BIN_SERIES])-1):
        if data_table.loc[index_no+1, ENG_SERIES] <= 0:
            if binned_data_df_series.loc[data_table.loc[index_no+1, NEW_BIN_SERIES], 'CycleBinCounts'] > 0:
                binned_data_df_series.loc[data_table.loc[index_no+1, NEW_BIN_SERIES], 'CycleBinCounts'] -= 1
            negative_count += 1
    # Now adjust the fractions accordingly
#    print negative_count
    binned_data_df_series['Fraction'] = binned_data_df_series['CycleBinCounts']/ (negative_count + binned_data_df_series['CycleBinCounts'].sum()) * 100
#    print negative_count -1 + binned_data_df_series['CycleBinCounts'].sum()
    # We need to also Absolute Tractive Power which shall be used to calculate the Cycle Observed Work(kW) 
    # Please not the calculation of Cycle Observed Work happens in OpModeSummary(our equivalent EnergyConsumption) in Excel but we have done it here
    # because its more convinient and saves passing of a few variables across modules
    data_table[ABS_TRACTIVE_POWER] = data_table.stp.abs() * FIXED_MASS_FACTOR
    # Initlialize the new column to be created
    binned_data_df_series[CYCLE_OBSERVED_WORK] = binned_data_df_series.Fraction
    for bin_no in binned_data_df_series.STPOMBin.values:
        binned_data_df_series.loc[bin_no, CYCLE_OBSERVED_WORK] = data_table.loc[data_table[NEW_BIN_1_SERIES] == bin_no, ABS_TRACTIVE_POWER].sum() /3600.0
    
#    util.df_to_csv_debug(binned_data_df_parallel, "hybrid_processor_binned_data_parallel.csv")
#    util.df_to_csv_debug(data_table, "hybrid_processor_binned_data_series.csv")
    
    return binned_data_df_parallel, binned_data_df_series




