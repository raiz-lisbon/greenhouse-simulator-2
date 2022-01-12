from typing import NewType

# Mass
g = NewType('grams', float)
kg = NewType('kilograms', float)

# Length
m = NewType('m', float)

# Surface
cm2 = NewType('cm2', float)
m2 = NewType('m2', float)

# Volume
m3 = NewType('m3', float)

# Temperature
C = NewType('Celsius', float)

# Time
s = NewType('seconds', float)
h = NewType('hour', float)

# Power
W = NewType('Watts', float)

# Energy
J = NewType('Joules', float)
kWh = NewType('kWh', float)

# Liquid volume
l = NewType('liters', float)

# Amount of substance
umol = NewType('micro mole', float)
mol = NewType('mole', float)

# Enthalpy
kJ = NewType('kJ', float)

# Specific Enthalpy
J_per_kg = NewType('J / kg', float)

# Pressure
mmHg = NewType('mmHg', float)
Pa = NewType('Pa', float)

# Angle
deg = NewType('degrees', float)
rad = NewType('radians', float)


# Concentration
ppm = NewType('ppm', float)
mol_CO2_per_mol_air = NewType('mol CO2 / mol air', float)

# Molar volume
m3_per_mol = NewType('m3 / mol', float)

# Humidity
RH = NewType('RH%', float)
g_per_m3 = NewType('g / m3', float)
kg_H2O_per_kg_air = NewType('kg water vapor / kg air', float)
kg_H2O_per_kg_air_per_s = NewType('kg_H2O_per_kg_air_per_s', float)

# Density
kg_per_l = NewType('kg / l', float) # liquids
kg_per_m3 = NewType('kg / m3', float) # gases

# Heat capacity
J_per_K = NewType('J / K', float)

# Specific heat capacity
J_per_kg_K = NewType('J / kg * K', float) # fluids, solids
J_per_m3_K = NewType('J / m3 * K', float) # gases

# Irradiance
W_per_m2 = NewType('W / m2', float)

# Photon flux
mol_per_m2 = NewType('mol / m2', float)
umol_per_m2 = NewType('umol / m2', float)
mol_per_m2_s = NewType('mol / m2 * s', float)
mol_per_m2_hours = NewType('mol / m2 * hour', float)
mol_per_m2_day = NewType('mol / m2 * day', float)
umol_per_m2_s = NewType('umol / m2 s', float)

# Insulation efficiency
W_per_m2_K = NewType('W / (m2 K)', float)

# Absolute humidity
kg_per_m3 = NewType('kg / m3', float)

# Photosynthetic rate
umol_per_m2_s = NewType('umol CO2 / m2 leaf * s', float)
umol_per_s = NewType('umol CO2 / s', float)

# Transpiration rate
mmol_per_m2_s = NewType('mmol H2O / m2 leaf * s', float)
mmol_per_s = NewType('mmol H2O / s', float)

# Airflow
m3_per_s = NewType('m3 / s', float)

# Substance flow
mol_per_s = NewType('mol / s', float)

# Mass flow
g_per_s = NewType('g / s', float)
kg_per_s = NewType('kg / s', float)

# Enthalpy flow
J_per_s = NewType('J / s', float)
kJ_per_s = NewType('kJ / s', float)

# Specific heat
kJ_per_kg_C = NewType('kJ / kg * C', float)

# Evaporation heat
J_per_g = NewType('J / g', float)
kJ_per_kg = NewType('kJ / kg', float)

# Concentration change
ppm_per_s = NewType('ppm / s', float)

# Humidity change
RH_per_s = NewType('RH / s', float)

# Temp change
C_per_s = NewType('C / s', float)

# Daily Light Integral
mol_per_m2_day = NewType('mol / m2 * day', float)

# LED energy efficiency
umol_per_joule = NewType('umol / Joule', float)

# Dehumidifier params
l_per_kWh = NewType('liter / kWh', float)
l_per_s = NewType('liter / s', float)

# AC efficiency
BTU_per_kWh = NewType('BTU / kWh', float)
BTU = NewType('British Thermal Unit', float)

# Prices
EUR = NewType('Euros', float)
EUR_per_kWh = NewType('Euros / kWh', float)
EUR_per_kg = NewType('Euros / kg', float)

# Speed
km_per_h = NewType('km / h', float)