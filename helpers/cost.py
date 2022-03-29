import numpy as np

from helpers.types import *
from helpers.conversions import *


electricity_cost: EUR_per_kWh = 0.145

def get_total_cost(df, greenhouse):
        time_period = greenhouse.time_period
        # Fan
        auc_airflow: m3 = np.trapz(df["airflow_m3_per_s"], dx=time_period)  # auc: Area Under Curve
        energy_used_by_fan: J = greenhouse.fan.get_energy_usage(auc_airflow)

        # Heating
        auc_heating: J = np.trapz(df["heating_rate_J_per_s"], dx=time_period)
        energy_used_by_heating: J = greenhouse.heatpump.get_energy_usage(auc_heating)

        # Dehumidification
        auc_dehum: g = np.trapz(df["dehum_rate_g_per_s"], dx=time_period)
        energy_used_by_dehum, _ = greenhouse.dehumidifier.run(auc_dehum)

        # Lighting
        energy_used_by_lighting: J = df['energy_used_by_lighting_J'].sum()

        total_energy: J = energy_used_by_fan + energy_used_by_heating + energy_used_by_dehum + energy_used_by_lighting

        # Energy generated
        total_energy_generated: kWh = df['total_energy_generated_kWh'].sum()

        total_cost: EUR = (J_to_kWh(total_energy) - total_energy_generated) * electricity_cost
        total_yield: kg = df['harvested_weight_g'].sum() / 1000
        total_harvested_plant_count = df["harvested_plant_count"].sum()
        
        return total_cost, total_yield, total_harvested_plant_count