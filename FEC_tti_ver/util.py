# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import os
def df_to_csv_debug(df, filename):
    if not os.path.exists("debug"):
        os.makedirs("debug")
    df.to_csv("debug/" + str(filename))
    os.system("chmod -R 777 debug")

# <codecell>


