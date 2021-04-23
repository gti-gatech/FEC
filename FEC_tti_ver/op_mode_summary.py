# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import bin_processor
import hybrid_processor
#import pandas as pd
import util

# <codecell>

def get_op_mode_summary(speeds, number_of_passengers, ambient_temperature_degree_f, relative_humidity, roughness_index, idle_speed_range,FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR):

    binned_data_df, bins, data_table = bin_processor.get_binned_data(speeds, number_of_passengers, roughness_index, idle_speed_range,FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR)
    
    binned_data_df_parallel, binned_data_df_series = hybrid_processor.get_binned_data_hybrid(speeds, 
                                                                                             number_of_passengers,
                                                                                             ambient_temperature_degree_f,
                                                                                             relative_humidity,
                                                                                             roughness_index,
                                                                                             idle_speed_range,
                                                                                             FORMULA_B1,FORMULA_B2,FORMULA_B3,SOURCE_MASS_METRIC_TONNES,FIXED_MASS_FACTOR)
                                                                                            
    #print binned_data_df
    #print "hello there" 
#    util.df_to_csv_debug(data_table, "bin_processor_trouble.csv")
#    df=pd.DataFrame([data_table])
#    df.to_csv('bindistribution.csv',sep='\t')
#    print binned_data_df_parallel

#    print bins
    return binned_data_df, binned_data_df_parallel, binned_data_df_series

# <codecell>


