from types import *

class Polycarbonate:
    # 8mm twin-wall polycarbonate
    def __init__(self):
        self.U_value: W_per_m2_K = 0.63 # source: https://www.greenhousecatalog.com/greenhouse-insulation

class Insolight:
    def __init__(self):
        self.U_value: W_per_m2_K = 0.8 # TODO: get real value

class Plywood:
    # 18mm marine plywood
    def __init__(self):
        self.U_value: W_per_m2_K = 0.6 # source: http://www.xor.org.uk/unimog/mymog/insulation.htm

class BrickWall:
    # 8" brick wall
    def __init__(self):
        self.U_value: W_per_m2_K = 0.41 # source: https://www.combustionresearch.com/U-Values_for_common_materials.html
