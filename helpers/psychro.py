import psychrolib

import sys
sys.path.insert(0, '/work/greenhouse-simulator-2/')

from helpers.types import *


def get_humid_air_specific_enthalpy(temp: C, humidity: RH, pressure=101325) -> J_per_kg:
    humidity_ratio: kg_H2O_per_kg_air = psychrolib.GetHumRatioFromRelHum(temp, humidity / 100, pressure)
    specific_enthalpy_of_moist_air: J_per_kg = psychrolib.GetMoistAirEnthalpy(temp, humidity_ratio)
    return specific_enthalpy_of_moist_air