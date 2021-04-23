# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from pandas import read_csv
def fetch_data_table(table_name, from_sql=False):
    df = None
    if not from_sql:
        if table_name == "CityLookup":
            df = read_csv('CityLookup.csv', sep='\t', encoding='utf-16')
        else:
            df = read_csv(table_name + ".csv", sep='\t')
    return df

# <codecell>


