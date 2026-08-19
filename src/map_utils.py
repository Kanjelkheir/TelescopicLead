import utm
from geopy.geocoders import Nominatim


def get_place_coordinates_and_zone(place_name):
    # Initialize the Geopy locator (always include a descriptive user_agent)
    geolocator = Nominatim(user_agent="coordinate_zone_finder")

    try:
        # Geocode the string address to find latitude and longitude
        location = geolocator.geocode(place_name)

        if location is None:
            return f"Error: Could not find the location '{place_name}'."

        lat = location.latitude
        lon = location.longitude

        # Convert latitude and longitude to UTM map coordinates and zone
        # Returns: (Easting, Northing, Zone Number, Zone Letter)
        easting, northing, zone_number, zone_letter = utm.from_latlon(lat, lon)

        return {
            "Place": location.address,
            "latitude": lat,
            "longitude": lon,
            "UTM Easting (m)": round(easting, 2),
            "UTM Northing (m)": round(northing, 2),
            "UTM Zone": f"{zone_number}{zone_letter}",
        }

    except Exception as e:
        return f"An error occurred: {e}"
