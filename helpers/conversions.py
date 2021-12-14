from helpers.types import *

def J_to_kWh(energy: J) -> kWh:
    return energy / 3.6e+6

def kWh_to_J(energy: kWh) -> J:
    return energy * 3.6e+6

def ppm_to_amount(concentration: ppm, volume: m3) -> mol:
    molar_volume_air: m3_per_mol = 0.024465 # TODO: take temperature (and pressure) into account
    air_amount: mol = volume / molar_volume_air

    concentration_mol_per_mol = concentration / 1e6
    amount: mol = concentration_mol_per_mol * air_amount
    return amount


def amount_to_ppm(amount: mol, volume: m3) -> ppm:
    molar_volume_air: m3_per_mol = 0.024465 # TODO: take temperature (and pressure) into account
    air_amount: mol = volume / molar_volume_air

    concentration_mol_per_mol = amount / air_amount
    new_concentration: ppm = concentration_mol_per_mol * 1e6
    return new_concentration
    
# TODO: Validations