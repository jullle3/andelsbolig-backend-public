from pyproj import Transformer


def parse_long_lat(easting, northing):
    # Create a Transformer object from UTM Zone 32N (EPSG:25832) to WGS84 (EPSG:4326)
    transformer = Transformer.from_crs("EPSG:25832", "EPSG:4326", always_xy=True)
    long, lat = transformer.transform(easting, northing)
    return long, lat
