import psychrolib

import sys
sys.path.insert(0, '/work/greenhouse-simulator-2/')

from helpers.types import *
from helpers.psychro import *
from helpers.conversions import *

psychrolib.SetUnitSystem(psychrolib.SI)


pressure: Pa = 101325 # TODO: get this from weather data
air_density: kg_per_m3 = 1.1839 # TODO: take humidity into account with psychrolib
water_evaporation_heat: J_per_g = 2501


def get_airflow(rel_humidity: RH, ambient_humidity_at_inside_temp: RH, temp: C, ambient_data) -> m3_per_s:
    hum_airflow: m3_per_s = abs(rel_humidity - 70) * 0.1
    temp_airflow: m3_per_s = abs(temp - 25) * 0.1

    if ambient_humidity_at_inside_temp >= 80:
        return 0

    airflow_offset: m3_per_s = max(hum_airflow, temp_airflow)

    if airflow_offset < 0:
        airflow_offset = 0

    return 0.1 + airflow_offset


def derive_H2O(airflow: m3_per_s, humidity_ratio: kg_H2O_per_kg_air, ambient_humidity_ratio: kg_H2O_per_kg_air, humidity: RH, temp: C, input_values) -> RH_per_s:
    # Unpack input values
    H2O_mass_evaporation_rate: g_per_s = input_values["H2O_mass_evaporation_rate"]
    structure_volume: m3 = input_values["structure_volume"]

    # Get mass air inflow
    mass_airflow: kg_per_s = air_density * airflow

    # Define dehumidification rate
    dehum_rate: g_per_s = 0

    if airflow == 0:
        dehum_factor = 1 + (humidity - 70) * 0.1
        dehum_rate = H2O_mass_evaporation_rate * dehum_factor
        water_content_change_rate: g_per_s = H2O_mass_evaporation_rate - dehum_rate
    else:
        H2O_inflow: g_per_s = ambient_humidity_ratio * mass_airflow * 1000
        H2O_outflow: g_per_s = humidity_ratio * mass_airflow * 1000
        water_content_change_rate: g_per_s = H2O_inflow - H2O_outflow + H2O_mass_evaporation_rate - dehum_rate

    humidity_ratio_change_rate: kg_H2O_per_kg_air_per_s = water_content_change_rate / 1000 / structure_volume * air_density

    return humidity_ratio_change_rate, dehum_rate


def derive_temp(airflow: m3_per_s, humidity: RH, temp: C, input_values, dehum_rate: g_per_s) -> C_per_s:
    # Unpack input values
    ambient_temp = input_values["ambient_data"]["temp"]
    ambient_humidity = input_values["ambient_data"]["humidity"]
    H2O_mass_evaporation_rate = input_values["H2O_mass_evaporation_rate"]
    power_irradiated = input_values["power_irradiated"]
    get_heat_transfer_rate = input_values["get_heat_transfer_rate"]

    # To avoid psychrolib errors
    if humidity > 100:
        humidity = 100

    mass_airflow: kg_per_s = air_density * airflow

    # Ambient air
    enthalpy_of_airflow_in: J_per_s = get_humid_air_specific_enthalpy(ambient_temp, ambient_humidity) * mass_airflow

    # Inside air
    enthalpy_of_airflow_out: J_per_s = get_humid_air_specific_enthalpy(temp, humidity) * mass_airflow

    # Sunlight
    radiation_loss = 0.2
    equipment_absorption_factor = 0.2
    enthalpy_absorbed_by_plants_and_air: J_per_s = power_irradiated * (1 - radiation_loss - equipment_absorption_factor)
    enthalpy_absorbed_by_evapotranspiration: J_per_s = H2O_mass_evaporation_rate * water_evaporation_heat
    enthalpy_absorbed_by_air: J_per_s = enthalpy_absorbed_by_plants_and_air - enthalpy_absorbed_by_evapotranspiration

    # Conductive loss
    conductive_enthalpy_loss: J_per_s = get_heat_transfer_rate(temp - ambient_temp)

    # Condensation heat in dehumidifier
    condensation_heating_rate: J_per_s = water_evaporation_heat * dehum_rate

    # Net enthalpy change of air
    enthalpy_change_rate: J_per_s = enthalpy_of_airflow_in - enthalpy_of_airflow_out + enthalpy_absorbed_by_air - conductive_enthalpy_loss + condensation_heating_rate

    new_heating_rate: J_per_s = 0
    # if airflow == 0 and enthalpy_change_rate > 0 and temp >= self.target_temp[1]:
    #     new_heating_rate: J_per_s = enthalpy_change_rate
    #     enthalpy_change_rate: J_per_s = 0

    return enthalpy_change_rate, new_heating_rate


def derive_CO2(airflow, CO2_concentration: ppm, input_values):
    ambient_CO2: ppm = 410
    structure_volume = input_values["structure_volume"]
    CO2_assimilation_rate: mol_per_s = input_values["CO2_assimilation_rate"]

    CO2_inflow: mol_per_s = ppm_to_amount(ambient_CO2, airflow)
    CO2_outflow: mol_per_s = ppm_to_amount(CO2_concentration, airflow)
    net_change_amount: mol_per_s = CO2_inflow - CO2_assimilation_rate - CO2_outflow
    net_change_concentration: ppm_per_s = amount_to_ppm(net_change_amount, structure_volume)

    CO2_release_rate: mol_per_s = 0
    # if airflow == 0:
    #     net_change_concentration = 0
    #     CO2_release_rate = CO2_assimilated_per_s

    return net_change_concentration, CO2_release_rate


def airflow_model(t, y, t_max, input_values, control_register):
    # Destructure y values (== measured variables)
    humidity_ratio, temp, CO2_concentration = y

    if temp > 200:
        temp = 200
    if temp < -100:
        temp = -100
        
    humidity = psychrolib.GetRelHumFromHumRatio(temp, humidity_ratio, pressure) * 100

    # Get ambient humidity ratio and rel humidity at inside temp
    ambient_temp: C = input_values["ambient_data"]["temp"]
    ambient_humidity: RH = input_values["ambient_data"]["humidity"]
    ambient_humidity_ratio: kg_H2O_per_kg_air = psychrolib.GetHumRatioFromRelHum(ambient_temp, ambient_humidity / 100, pressure)
    ambient_humidity_at_inside_temp: RH = psychrolib.GetRelHumFromHumRatio(temp, ambient_humidity_ratio, pressure) * 100

    # Determine airflow
    airflow: m3_per_s = get_airflow(humidity, ambient_humidity_at_inside_temp, temp, input_values["ambient_data"])

    # Calculate change rate of measured variables
    humidity_ratio_change_rate, dehum_rate = derive_H2O(airflow, humidity_ratio, ambient_humidity_ratio, humidity, temp, input_values)
    temp_change_rate, heating_rate = derive_temp(airflow, humidity, temp, input_values, dehum_rate)
    CO2_concentration_change_rate, CO2_release_rate = derive_CO2(airflow, CO2_concentration, input_values)

    if airflow < 0:
        print(airflow)

    # Avoid duplicates to ensure strictly monotonically increasing list as it is a requirement of InterpolatedUnivariateSpline
    if t not in [x["t"] for x in control_register]: 
        control_register.append({
            "t": t,
            "dehum_rate_g_per_s": dehum_rate,
            "heating_rate_J_per_s": heating_rate,
            "CO2_release_rate_mol_per_s": CO2_release_rate,
            "airflow_m3_per_s": airflow,
            "ambient_humidity_at_inside_temp_RH": ambient_humidity_at_inside_temp
        })

    return [
        humidity_ratio_change_rate, 
        temp_change_rate, 
        CO2_concentration_change_rate, 
    ]
