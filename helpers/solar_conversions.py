from helpers.types import *


def irradiance_to_PPFD(irradiance: W_per_m2) -> umol_per_m2_s:
    # Approx conversion of W to umol TODO: make this more accurate, based on spectrum
    # https://www.researchgate.net/post/Can-I-convert-PAR-photo-active-radiation-value-of-micro-mole-M2-S-to-Solar-radiation-in-Watt-m2/59ca6422217e201e2b23415f/citation/download
    PPFD: umol_per_m2_s = irradiance * 2.1

    return PPFD


def PPFD_to_projected_DLI(PPFD: umol_per_m2_s, photoperiod: h) -> mol_per_m2_day:
    PAR_photon_amount: mol_per_m2_s = PPFD * 1e-6

    return PAR_photon_amount * photoperiod * 3600


def projected_DLI_to_PPFD(dli: mol_per_m2_day, photoperiod: h) -> umol_per_m2_s:
    PAR_photon_amount: mol_per_m2_s = dli / (photoperiod * 3600)

    return PAR_photon_amount / 1e-6

def PAR_amount_to_projected_DLI(PAR_photon_amount: mol_per_m2, time_period: s, photoperiod: h) -> mol_per_m2_day:
    return PAR_photon_amount * (photoperiod * 3600 / time_period)

def projected_DLI_to_PAR_amount(projected_DLI: mol_per_m2_day, time_period: s) -> mol_per_m2:
    return (projected_DLI * time_period) / (photoperiod * 3600)


### VALIDATION
# With online calculator: https://scynceled.com/dli-calculator/
assert round(PPFD_to_projected_DLI(900, 16), 2) == 51.84, "Error while validating `PPFD_to_projected_DLI`"
assert round(projected_DLI_to_PPFD(13, 16), 2) == 225.69, "Error while validating `projected_DLI_to_PPFD`"


print("Validation PASSED: solar_conversions.py")
