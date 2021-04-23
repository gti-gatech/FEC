# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# Imports

# <codecell>

# File Name Constants
CUSTOM_FILE = "CustomInput"
SOURCE_TYPE_PHYSICS= "sourceusetypephysics"
MOVES_ER_FILE = "MovesER"
CYCLE_LOOKUP_FILE = "CycleLookup"
RAW_CYCLE_LOOKUP_FILE = "RawCycleLookup"
GREET_LOOKUP_FILE = "Full_Greet_Lookup"
EGRID_LOOKUP_FILE = "eGridLookup"
CITY_LOOKUP_FILE = "CityLookup"
FUEL_TYPE_ID_NAME_MAP_FILE = "FuelTypeIDNameMap"
POLLUTANTS_FILE = "Pollutants"

FORMULA_B1 = 0.064
FORMULA_B2 = 0.000
FORMULA_B3 = 0.0002097673
FORMULA_B4 = 0.9681871345
MPH_TO_MPS_CONVERSION_FACTOR = 1609.34/3600
PER_PASSENEGER_AVERAGE_WEIGHT = 150
POUNDS_TO_METRIC_TONS = 0.000453592
SOURCE_MASS_METRIC_TONNES = 16.556
FIXED_MASS_FACTOR = 17.1
GRAVITY = 9.8
KWH_TO_MMBTU = 0.003412


FUEL_UPSTREAM_CALCULATION_CONSTANT = 0.003412
HEV_TO_SI_CI_WEIGHT_FACTOR = 1.0
PARALLEL_MECHANICAL_ELECTRICAL_EFFICIENCY_TRANSIT_BUS = 0.5
INVERTER_EFFICIENCY = 0.97
MOTOR_EFFICIENCY = 0.86
BATTERY_EFFICIENCY = 0.9
FUEL_CELL_EFFICIENCY = 0.5

# <codecell>

# String constants
ATMOSPHERIC_CO2 = "Atmospheric CO2"
METHANE_CH4 = "Methane (CH4)"
NITROUS_OXIDE_N2O = "Nitrous Oxide(N2O)"
ELEMENTAL_CARBON = "Primary PM2.5 - Elemental Carbon"
CO2_EQUIVALENT = "CO2 Equivalent"
CARBON_MONOXIDE = "Carbon Monoxide(CO)"
VOLATILE_ORGANIC_COMPOUNDS = "Volatile Organic Compounds"
OXIDES_OF_NITROGEN = "Oxides of Nitrogen(NOx)"
PRIMARY_EXHAUST_25 = "Primary Exhaust PM2.5 - Total"
PRIMARY_EXHAUST_10 = "Primary Exhaust PM10 - Total"
SULPHUR_DIOXIDE_SO2 = "Sulphur Dioxide (SO2)"
END_OF_RUN = "End_of_Run"
TRAIN_ARCHITECTURE_SERIES = "Series"
TRAIN_ARCHITECTURE_PARALLEL = "Parallel"

KG = "kg"
GM = "g"
METRIC_TONNES = "metric tonnes"
HEV_TO_SI_CI_WEIGHT_FACTOR = 1.00
LBS_TO_KG = 0.453592
LBS_TO_G = 453.592

# <codecell>

GHG_EMISSIONS = [ATMOSPHERIC_CO2, 
                 METHANE_CH4,
                 NITROUS_OXIDE_N2O,
                 ELEMENTAL_CARBON,
                 CO2_EQUIVALENT,
                 CARBON_MONOXIDE,
                 VOLATILE_ORGANIC_COMPOUNDS,
                 OXIDES_OF_NITROGEN,
                 PRIMARY_EXHAUST_10,
                 PRIMARY_EXHAUST_25,
                 SULPHUR_DIOXIDE_SO2]

GHG_EMISSIONS_TO_ID_MAP = {
                                ATMOSPHERIC_CO2 : 90,
                                METHANE_CH4 : 5,
                                NITROUS_OXIDE_N2O : 6,
                                ELEMENTAL_CARBON : 112,
                                CARBON_MONOXIDE : 2,
                                VOLATILE_ORGANIC_COMPOUNDS : 87,
                                OXIDES_OF_NITROGEN : 3,
                                PRIMARY_EXHAUST_10 : 100,
                                PRIMARY_EXHAUST_25 : 110,
                                SULPHUR_DIOXIDE_SO2 : 31
                           }

GHG_EMISSIONS_SHORTNAMES = {
                                ATMOSPHERIC_CO2     : "CO2",
                                METHANE_CH4         : "CH4",
                                NITROUS_OXIDE_N2O   : "N2O",
                                CARBON_MONOXIDE     : "CO",
                                VOLATILE_ORGANIC_COMPOUNDS : "VOC",
                                OXIDES_OF_NITROGEN  : "NOx",
                                PRIMARY_EXHAUST_25  : "PM2.5",
                                PRIMARY_EXHAUST_10  : "PM10",
                                SULPHUR_DIOXIDE_SO2 : "SO2"
                            }


#EV_EMISSIONS_MAP = {
#                                ATMOSPHERIC_CO2 : 15.77295727,
#                                METHANE_CH4 : 0.2002164865,
#                                CO2_EQUIVALENT : 0.01585837864,
#                                NITROUS_OXIDE_N2O : 0.2698522035,
#                                ELEMENTAL_CARBON : 0.0,
#                                CARBON_MONOXIDE : 13.88897632,
#                                VOLATILE_ORGANIC_COMPOUNDS : 0.2936402864,
#                                OXIDES_OF_NITROGEN : 10.85597085,
#                                PRIMARY_EXHAUST_10 : 1.438847625,
#                                PRIMARY_EXHAUST_25 : 0.7865382802,
#                                SULPHUR_DIOXIDE_SO2 : 40.5269952
#                           }


GHG_EMISSIONS_UNITS = [KG,
                       GM,
                       GM,
                       GM,
                       METRIC_TONNES,
                       GM,
                       GM,
                       GM,
                       GM,
                       GM,
                       GM]

ANNUAL_GHG_EMISSIONS_UNITS = [KG,
                              GM,
                              GM,
                              GM,
                              METRIC_TONNES,
                              KG,
                              KG,
                              KG,
                              KG,
                              KG,
                              KG]
# <codecell>


