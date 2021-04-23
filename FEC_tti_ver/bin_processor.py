# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

"""
Given a speed profile(speed values at various points in time) this module returns bin information 
by assigning a MOVES STP bin to each input point. It returns a table with
CycleBinCounts	Fraction	STPOMBin
as columns
"""
#import data_reader as dr
import constants as c
import math
import pandas as pd
#import os
import util

# XXX: TBD Add the input Idle Speed range by removing the constant used
def get_binned_data(speeds, number_of_passengers, roughness_index, idle_speed_range, FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR, stp=None):

 #   print idle_speed_range
    speeds = speeds[~speeds.isnull()]
    accelerations = speeds - speeds.shift()
    accelerations_br = speeds - speeds.shift() + (c.GRAVITY/0.44704) * math.sin(roughness_index/100.0)
 #   accelerations.round(2)

    accelerations.iloc[0]=accelerations.iloc[1]
    accelerations_br.iloc[0]=accelerations_br.iloc[1]    
    # Convert speeds from mph to m/s
    speeds_mps = speeds * c.MPH_TO_MPS_CONVERSION_FACTOR
    accelerations_mps = speeds_mps - speeds_mps.shift()
    
    accelerations_mps.iloc[0] = accelerations_mps.iloc[1]
 #   print accelerations_mps
    
    if stp is None:
        stp =  (speeds_mps     * FORMULA_B1) + \
              ((speeds_mps**2) * FORMULA_B2) + \
              ((speeds_mps**3) * FORMULA_B3) + \
                  (   (    SOURCE_MASS_METRIC_TONNES + \
                           c.POUNDS_TO_METRIC_TONS * number_of_passengers * c.PER_PASSENEGER_AVERAGE_WEIGHT \
                      ) / FIXED_MASS_FACTOR \
                  ) * \
                  (   accelerations_mps + c.GRAVITY * math.sin(roughness_index/100.0) \
                  ) * speeds_mps    
    
    # Join all relevant columns together in a table so that we can classify them in different bins and get the bin counts
    stp_df = pd.DataFrame(stp.values)
    speeds_df = pd.DataFrame(speeds.values)
    accelerations_df = pd.DataFrame(accelerations.values)
    accelerations_br_df = pd.DataFrame(accelerations_br.values)
    accelerations_br_df.columns=['acceleration_break']
#    util.df_to_csv_debug(accelerations_df,"acceleration.csv")
    data_table = pd.DataFrame.join(speeds_df, accelerations_df, how='left', lsuffix='speed', rsuffix='acceleration')
    data_table = pd.DataFrame.join(data_table, stp_df, how='left', lsuffix='stp')
    data_table.columns=['speed', 'acceleration', 'stp']

    
    data_table.acceleration=data_table.acceleration.round(12)
    accelerations_br_df.acceleration_break = accelerations_br_df.acceleration_break.round(12)
#    data_table.acceleration.multiply(0.0001)
    # Bin the data and save thes counts
    # Bin0 is when accleration is less than -2 or the last three acclerations(including the current one) have been less than -1
    # This is considered the decelerating state
    decel_criteria = accelerations_br_df.acceleration_break < -1.0
    
    # We shall shift the rows by one. This will thus form the condition - acceleration in the the previous row is less than -1
    decel_criteria1 = decel_criteria.shift(1)
    
    # The previous operation shall set the last value as NaN. We should set it to false so that operations ahead do not fail
    decel_criteria1[len(decel_criteria1)-1] = False
    
    # Shift the row again by 1. This shall then form the condition - acceleration in the previous to previous row is less than -1
    decel_criteria2 = decel_criteria1.shift(1)
    decel_criteria2[len(decel_criteria2)-1] = False

    bins = [None] * 41

    bins[0] = (accelerations_br_df.acceleration_break <= -2.0) | ((decel_criteria) & (decel_criteria1) & (decel_criteria2))

    # Bin1 - When the machine is de-accelerating and the velocity is between 1 and -1. This is considered the idle state.
#    bins[1] = (~bins[0] & (data_table.speed >= -1) & (data_table.speed < 1))
#    bins[11] = (~bins[0] & ~bins[1] & (data_table.speed >= 1) & (data_table.speed < 25) & (data_table.stp < 0))
    bins[1] = (~bins[0] & (data_table.speed >= -1 * idle_speed_range) & (data_table.speed < idle_speed_range))
#    print bins
    bins[11] = (~bins[0] & ~bins[1] & (data_table.speed >= idle_speed_range) & (data_table.speed < 25) & (data_table.stp < 0))
    speed_lower_limit = idle_speed_range
    speed_upper_limit = 25
    stp_lower_limit = 0
    stp_upper_limit = 3

    for bin_no in range(12,16):
        bins[bin_no] = (~bins[0] & ~bins[1] & (data_table.speed >= speed_lower_limit) & (data_table.speed < speed_upper_limit) & \
                        (data_table.stp >= stp_lower_limit) & (data_table.stp < stp_upper_limit))
        stp_lower_limit += 3
        stp_upper_limit += 3

    bins[16] = (~bins[0] & ~bins[1] & (data_table.speed >= 1) & (data_table.speed < 25) & (data_table.stp >= 12))
    bins[21] = (~bins[0] & ~bins[1] & (data_table.speed >= 25) & (data_table.speed < 50) & (data_table.stp < 0))

    speed_lower_limit = 25
    speed_upper_limit = 50
    stp_lower_limit = 0
    stp_upper_limit = 3

    for bin_no in [22,23,24,25]:
        bins[bin_no] = (~bins[0] & ~bins[1] & (data_table.speed >= speed_lower_limit) & (data_table.speed < speed_upper_limit) & \
                        (data_table.stp >= stp_lower_limit) & (data_table.stp < stp_upper_limit))
        stp_lower_limit += 3
        stp_upper_limit += 3

    stp_lower_limit = 12
    stp_upper_limit = 18

    for bin_no in [27,28,29]:
        bins[bin_no] = (~bins[0] & ~bins[1] & (data_table.speed >= speed_lower_limit) & (data_table.speed < speed_upper_limit) & \
                        (data_table.stp >= stp_lower_limit) & (data_table.stp < stp_upper_limit))
        stp_lower_limit += 6
        stp_upper_limit += 6

    bins[30] = (~bins[0] & ~bins[1] & (data_table.speed >= 25) & (data_table.speed < 50) & (data_table.stp >= 30))
    bins[33] = (~bins[0] & ~bins[1] & (data_table.speed >= 50) & (data_table.stp < 6))

    stp_lower_limit = 6
    stp_upper_limit = 12
    speed_lower_limit = 50


    for bin_no in [35,37,38,39]:
        bins[bin_no] = (~bins[0] & ~bins[1] & (data_table.speed >= speed_lower_limit)  & \
                        (data_table.stp >= stp_lower_limit) & (data_table.stp < stp_upper_limit))
        stp_lower_limit += 6
        stp_upper_limit += 6

    bins[40] = (~bins[0] & ~bins[1] & (data_table.speed >= 50) & (data_table.stp >= 30))

    bin_counts = [None] * 41
    fractions = [None] * 41
    # Reducing by 1 is just a HACK
    table_length = float(len(data_table) - 1)
    for bin_no, this_bin in enumerate(bins):
        if this_bin is not None:
            bin_counts[bin_no] = len(data_table[this_bin])
            # HACK - Reduce bin 1 count by 1
            if bins[bin_no][0] == True:
                bin_counts[bin_no] -= 1
            fractions[bin_no] = bin_counts[bin_no]/ table_length * 100.0


    bin_counts_series = pd.Series(bin_counts)
    fractions_series = pd.Series(fractions)
    bins_series =pd.Series(range(41))
    binned_data_df = pd.DataFrame({'CycleBinCounts' : bin_counts_series, 'Fraction' : fractions_series, 'STPOMBin' : bins_series})
    binned_data_df = binned_data_df[~binned_data_df.CycleBinCounts.isnull()]
    

    # In the data table add a direct mapping of the index to the BIN no it has been mapped to
    # Just initialize the old bin array with the speed values (just for the sake of initialization)
    data_table['BinNo'] = data_table.speed.astype(int)
    for bin_no, bin_bool in enumerate(bins):
        if bins[bin_no] is not None:            
            data_table.loc[bins[bin_no] == True, 'BinNo'] = int(bin_no)
    
#    util.df_to_csv_debug(data_table, "bin_processor_binned_data.csv")
#    util.df_to_csv_debug(stp,"stptest.csv")


    return binned_data_df, bins, data_table




