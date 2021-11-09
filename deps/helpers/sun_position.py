import sys
from pysolar import solar
from datetime import datetime, timezone

sys.path.insert(0, '../..')
from deps.types import *
from math_helpers import *


# =============================================================================================================================================================

def get_elevation_angle(coordinates, timestamp) -> deg:
    """
    Calculates the sun elevation angle (α, alpha) using pysolar.

    Parameters
    ----------
    coordinates: dict
        Dictionary with coordinates stored under 'latitude' and 'longitude' keys.
    timestamp: datetime
        Timestamp including timezone information to get the elevation angle at.

    Returns
    -------
    elevation_angle: deg
        Angle of the sun above the horizon.

    """
    elevation_angle: deg = solar.get_altitude(coordinates["latitude"], coordinates["longitude"], timestamp)

    # If elevation angle is negative (in the night), return 0.
    if elevation_angle < 0:
        elevation_angle = 0

    return elevation_angle

### VALIDATION

# Lisbon coordinates
coordinates = { "latitude": 38.7436883, "longitude": -9.1393}

sc = "1: 0° at sunrise (minus 4 min)."
sunrise = datetime(2021, 3, 22, 6, 40, 0, tzinfo=timezone.utc)
assert round(get_elevation_angle(coordinates, sunrise)) == 0, f"get_elevation_angle validation FAILED - {sc}"

sc = "2: 0° at sunset (plus 4 min)."
sunset = datetime(2021, 9, 22, 18, 31, 0, tzinfo=timezone.utc)
assert round(get_elevation_angle(coordinates, sunset)) == 0, f"get_elevation_angle validation FAILED - {sc}"

sc = "3: 90° at solar noon at Tropic of Cancer on the summer solstice."
coordinates = { "latitude": 23.43645, "longitude": 0}
sunset = datetime(2021, 6, 21, 12, 2, 0, tzinfo=timezone.utc)
assert round(get_elevation_angle(coordinates, sunset)) == 90, f"get_elevation_angle validation FAILED - {sc}"

print("Validation PASSED: get_elevation_angle")


# =============================================================================================================================================================

def get_azimuth_angle(coordinates, timestamp) -> deg:
    """
    Calculates the sun azimuth angle (Θ, theta) using pysolar. 

    Parameters
    ----------
    coordinates: dict
        Dictionary with coordinates stored under 'latitude' and 'longitude' keys.
    timestamp: datetime
        Timestamp including timezone information to get the azimuth angle at.

    Returns
    -------
    azimuth_angle: deg
        Azimuth angle at given location and time, indicating the sun's position during the day. North == 0°, East == 90°, South == 180°, and West == 270°.

    """
    azimuth_angle: deg = solar.get_azimuth(coordinates["latitude"], coordinates["longitude"], timestamp)

    return azimuth_angle

### VALIDATION

# Lisbon coordinates
coordinates = { "latitude": 38.7436883, "longitude": -9.1393}

sc = "1: At solar noon, the azimuth is 180° (on northern hemisphere)."
solar_noon = datetime(2021, 6, 20, 12, 38, 0, tzinfo=timezone.utc)
assert round(get_azimuth_angle(coordinates, solar_noon)) == 180, f"get_azimuth_angle validation FAILED - {sc}"

sc = "2: At the equinoxes, the azimuth is 90° at sunrise."
sunrise = datetime(2021, 3, 22, 6, 44, 0, tzinfo=timezone.utc)
assert round(get_azimuth_angle(coordinates, sunrise)) == 90, f"get_azimuth_angle validation FAILED - {sc}"

sc = "3: At the equinoxes, the azimuth is 270° at sunset."
sunset = datetime(2021, 9, 22, 18, 27, 0, tzinfo=timezone.utc)
assert round(get_azimuth_angle(coordinates, sunset)) == 270, f"get_azimuth_angle validation FAILED - {sc}"

print("Validation PASSED: get_azimuth_angle")


# =============================================================================================================================================================

def get_intensity_coeff(coordinates, timestamp, panel_tilt, panel_azimuth):
    """
    Calculates the ratio of the incident solar radiation which is perpendicular to the panel surface.
    The panel can have an arbitrary orientation and tilt.
    Source: https://www.pveducation.org/pvcdrom/properties-of-sunlight/arbitrary-orientation-and-tilt

    Params
    ------
    coordinates: dict
        Dictionary with coordinates stored under 'latitude' and 'longitude' keys.
    timestamp: datetime
        Timestamp including timezone information to get the azimuth angle at.
    panel_tilt: deg
        Panel tilt angle measured from Earth's surface. A panel lying flat on the ground has a tilt of 0°, and a vertical panel has a tilt of 90°.
    panel_azimuth: deg
        Orientation of the panel expressed as azimuth angle. A panel facing North has 0°, East has 90°, South has 180°, and West has 270° azimuth angle.

    Returns
    -------
    intensity_coeff: float
        Intensity coefficient corresponding to the ratio of the incident sunlight which is perpendicular to the panel surface.
        A panel perpendicular to the sunlight has intensity_coeff of 1, while a panel parallel to it has intensity_coeff of 0.
    """
    alpha: deg = get_elevation_angle(coordinates, timestamp)# sun elevantion angle
    beta: deg = panel_tilt # panel tilt angle
    theta: deg = get_azimuth_angle(coordinates, timestamp) # sun azimuth
    psi: deg = panel_azimuth # panel azimuth

    intensity_coeff = cos(alpha) * sin(beta) * cos(psi - theta) + sin(alpha) * cos(beta)

    if intensity_coeff < 0:
        intensity_coeff = 0

    return intensity_coeff

### VALIDATION

sc = "1: get_intensity_coeff is 1 if panel tilt equals sun's zenith angle and panel faces the sun directly."
coordinates = { "latitude": 23.43645, "longitude": 0}
date = datetime(2021, 6, 21, 16, 26, 0, tzinfo=timezone.utc)

assert round(get_intensity_coeff(coordinates, date, 60, 284), 2) == 1, f"get_intensity_coeff validation FAILED - {sc}"

sc = "2: get_intensity_coeff is 1 if panel lays flat on the ground and the sun is directly overhead."
coordinates = { "latitude": 23.43645, "longitude": 0}
date = datetime(2021, 6, 21, 12, 2, 0, tzinfo=timezone.utc)

assert round(get_intensity_coeff(coordinates, date, 0, 0), 2) == 1, f"get_intensity_coeff validation FAILED - {sc}"

sc = "3: get_intensity_coeff is 0 if panel is vertical and the sun is directly overhead."
coordinates = { "latitude": 23.43645, "longitude": 0}
date = datetime(2021, 6, 21, 12, 2, 0, tzinfo=timezone.utc)

assert round(get_intensity_coeff(coordinates, date, 90, 0), 2) == 0, f"get_intensity_coeff validation FAILED - {sc}"

sc = "4: get_intensity_coeff is 0.5 if panel tilt is 60° and the sun is directly overhead."
coordinates = { "latitude": 23.43645, "longitude": 0}
date = datetime(2021, 6, 21, 12, 2, 0, tzinfo=timezone.utc)

assert round(get_intensity_coeff(coordinates, date, 60, 0), 2) == 0.5, f"get_intensity_coeff validation FAILED - {sc}"

sc = "5: get_intensity_coeff is 0.5 if panel lays flat on the ground and the sun elevation angle is 30°."
coordinates = { "latitude": 23.43645, "longitude": 0}
date = datetime(2021, 6, 21, 16, 26, 0, tzinfo=timezone.utc)

assert round(get_intensity_coeff(coordinates, date, 0, 0), 2) == 0.5, f"get_intensity_coeff validation FAILED - {sc}"

print("Validation PASSED: get_intensity_coeff")
