import math
import numpy as np

from helpers.types import *
from helpers.conversions import *
from helpers.solar_conversions import *



class Crop:
    def __init__(self, time_period: s, initial_weight, initial_leaf_area, grow_period, target_DLI, plants_per_barrel, barrel_count):
        # Init class with structure specific values
        self.plants_per_barrel = plants_per_barrel
        self.barrel_count = barrel_count
        self.time_period = time_period
        self.total_count = self.plants_per_barrel * self.barrel_count

        # Init crop specific variables which should be populated in subclasses
        self.initial_weight: g = initial_weight
        self.initial_leaf_area: cm2 = initial_leaf_area
        self.grow_period: d = grow_period
        self.target_DLI: mol_per_m2_day = target_DLI

        # Init accumulators (for 1 barrel)
        self.weights = []
        self.leaf_areas = []

        # Init accumulators (for all barrels)
        self.harvested_weight: kg = 0

        # Init a vector with one scalar for each plant in a barrel
        self.hours_after_transplant = np.zeros(self.plants_per_barrel)

        # Spread out growth phase evenly
        for i, _ in enumerate(self.hours_after_transplant):
            self.hours_after_transplant[i] = (i / self.plants_per_barrel) * self.grow_period * 24 

        # Init weight and leaf_area
        self._initiate_crops()


    @property
    def total_leaf_area(self) -> m2:
        return self.barrel_count * self.leaf_areas[-1].sum() / 10000


    def grow(self, PAR_photon_amount: mol_per_m2):
        # Add `time_period` in hours to vector of hours after transplant (for each plant)
        self.hours_after_transplant = self.hours_after_transplant + (self.time_period / 3600)

        dli: mol_per_m2_day = PAR_amount_to_projected_DLI(PAR_photon_amount, self.time_period, self.photoperiod)
        self._register_plant_growth(dli)

        CO2_assimilation_rate, CO2_assimilated = self._get_CO2_assimilated(dli)
        H20_evaporation_rate, H2O_evaporated = self._get_H2O_evaporated(dli)

        # Harvest plants that are over their `growth_period`
        harvested_weight, harvested_plant_count = self._harvest()

        return harvested_weight, harvested_plant_count, CO2_assimilation_rate, CO2_assimilated, H20_evaporation_rate, H2O_evaporated


    def _get_CO2_assimilated(self, dli: mol_per_m2_day):
        """
        Calculates total amount (mol) of CO2 assimilated by all plants in the greenhouse in a `time_period` given `dli` irradiance level.
        """
        specific_photosynthetic_rate: umol_per_m2_s = self._get_specific_photosynthetic_rate(dli)
        photosynthetic_rate: umol_per_s = specific_photosynthetic_rate * self.total_leaf_area
        CO2_assimilation_rate: mol_per_s = photosynthetic_rate / 1e6
        CO2_assimilated: mol = CO2_assimilation_rate * self.time_period 

        return CO2_assimilation_rate, CO2_assimilated


    def _get_H2O_evaporated(self, dli: mol_per_m2_day) -> mol:
        """
        Calculates total amount of H2O vapor (mol) evaporated by all plants in the green house in a `time_period` given `dli` irradiance level.
        """
        specific_transpiration_rate: mmol_per_m2_s = self._get_specific_transpiration_rate(dli)
        transpiration_rate: mmol_per_s = specific_transpiration_rate * self.total_leaf_area
        H20_evaporation_rate: mol_per_s = transpiration_rate / 1e3
        H20_evaporated: mol = H20_evaporation_rate * self.time_period

        return H20_evaporation_rate, H20_evaporated


    def _get_growth_coeffs(self):
        """
        Calculates for each plant how many hours elapsed since their transplants at the beginning and end of the current `time_period`.
        """
        growth_coeffs_at_start = []
        growth_coeffs_at_end = []

        for hour_of_plant in self.hours_after_transplant:
            growth_coeffs_at_start.append(self._get_growth_coeff_at(hour_of_plant))
            growth_coeffs_at_end.append(self._get_growth_coeff_at(hour_of_plant + (self.time_period / 3600)))

        return np.array(growth_coeffs_at_start), np.array(growth_coeffs_at_end)


    def _init_property(self, prop_name, final_prop_value):
        """
        Initiates plant properties (such as weight, leaf area) based on initial `hours_after_transplant`.
        """
        growth_coeffs = self._get_growth_coeffs()
        props = growth_coeffs[0] * final_prop_value

        # If prop is under starting value, replace it to starting value.
        # (if actual DLI is higher than target, this will cause minor discrepancies in the beginning of the plants cycle)
        start_value = getattr(self, f"initial_{prop_name}")
        under_start_value = props < start_value
        props[under_start_value] = start_value
        
        getattr(self, prop_name + "s").append(props)


    def _initiate_crops(self):
        final_weight, final_leaf_area = self._get_final_plant_props(self.target_DLI)

        self._init_property("weight", final_weight)
        self._init_property("leaf_area", final_leaf_area)


    def _register_property_change(self, prop_name, final_prop_value):
        """
        Calculates plant property change (such as weight, leaf area) during a `time_period`, and saves it to the appropriate register.
        This way it computes the increment during the time period given a `dli` amount and adds it to the last property of the plant.
        """
        growth_coeffs = self._get_growth_coeffs()
        props_at_start = growth_coeffs[0] * final_prop_value
        props_at_end = growth_coeffs[1] * final_prop_value
        props_delta = props_at_end - props_at_start

        getattr(self, prop_name + "s").append(getattr(self, prop_name + "s")[-1] + props_delta)

    
    def _register_plant_growth(self, dli: mol_per_m2_day):
        final_weight, final_leaf_area = self._get_final_plant_props(dli)

        self._register_property_change("weight", final_weight)
        self._register_property_change("leaf_area", final_leaf_area)


    def _harvest(self):
        """
        Harvest plants that are over their `growth_period`, add their weight to `harvested_weight`, then initialize them to starting `weight` and `leaf_area`.
        """
        # Check which plants needs to be harvested
        plants_to_harvest = self.hours_after_transplant >= (self.grow_period * 24)

        # Sum their weight and add it to harvest accumulator
        harvested_weight: g = self.weights[-1][plants_to_harvest].sum() * self.barrel_count
        self.harvested_weight += harvested_weight

        # Initialize new plants in the place of the harvested ones (==transplant seedlings)
        self.weights[-1][plants_to_harvest] = self.initial_weight
        self.leaf_areas[-1][plants_to_harvest] = self.initial_leaf_area

        # Start over counting `hours_after_transplant` if any plant goes over `grow_period` (== being harvested)
        self.hours_after_transplant = self.hours_after_transplant % (self.grow_period * 24)

        harvested_count = len([p for p in plants_to_harvest if p]) * self.barrel_count

        return harvested_weight, harvested_count


    def _get_final_plant_props(self, dli: mol_per_m2_day) -> g:
        raise NotImplementedError()


    def _get_growth_coeff_at(self, hour: h):
        raise NotImplementedError()


    def _get_specific_photosynthetic_rate(self, dli: mol_per_m2_day) -> umol_per_m2_s:
        raise NotImplementedError()


    def _get_specific_transpiration_rate(self, dli: mol_per_m2_day) -> mmol_per_m2_s:
        raise NotImplementedError()