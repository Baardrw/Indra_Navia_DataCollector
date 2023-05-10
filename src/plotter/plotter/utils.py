from math import radians, sqrt, sin, cos

def wgs84_to_ecef(lat, long, alt):
    lat_rad = radians(lat)
    long_rad = radians(long)

    a = 6378137.0  # earth equatorial radius in meters
    b = 6356752.3142  # earth polar radius in meters
    e2 = (a**2 - b**2) / a**2

    N = a / sqrt(1 - e2 * sin(lat_rad) ** 2)

    x = (N + alt) * cos(lat_rad) * cos(long_rad)
    y = (N + alt) * cos(lat_rad) * sin(long_rad)
    z = (N * (1 - e2) + alt) * sin(lat_rad)
    return (x, y, z)