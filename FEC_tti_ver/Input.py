# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# Naming conventions
# All names are taken completely from the excel sheet without any abbreviations 
# to avoid any confusion in understanding variable's purpose or meaning
# So for example Average Passenger Loading per Bus per Run is represnted by the variable
# average_passenger_loading_per_bus_per_run
# Spaces in Field/variable names are replaced by '_'
# Camel Case in used while represnting classes
# All names(whether naming files or variables) are always taken exactly from the Excel Sheet
class Scenario:
    """
    Represents an object representing all fields related to scenario. 
    The scenario is typically input by the user.
    """
    def __init__(self):
        self.city = ""
        self.state = ""
        # Could be "Winter" or "Summer"
        self.season = ""
        # Severity index ranges from 1 to 6
        self.severity_index = None
        self.inventory_year = None
        self.duty_cycle = ""
        self.vehicle_classification = ""
        route_length = None
        average_passenger_loading_per_bus_per_run = None
        number_of_buses = None

        
class VehicleRoute:
    """
    Encancapsulates vehicle technology and route related options
    """
    def __init__(self):
        self.vehicle_technology = ""
        self.fuel_type = ""
        self.fuel_type_greet = ""
        self.revenue_route = None
        self.model_year = None
        self.roughness = ""

# <codecell>

a = object()

# <codecell>


# <codecell>

import os

# <codecell>

os.path.exists('/home/ravikant')

# <codecell>


