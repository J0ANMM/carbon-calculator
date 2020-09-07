"carbon-ferry.py calculates the emissions of passengers taking a ferry"

try:
    from carbon import Carbon
except ImportError:
    from results.carbon_calculator_git.carbon import Carbon #complete path inside Django project needed to make it work in Django Framework


class CarbonFerry(Carbon):
    """Class to calculate CO2 emmissions in ferries."""

    def __init__(self):
        self.avg_speed_kmh = 30 #according to Rome2rio, ferry from Menorca to Mallorca is 189.3km in 6h --> 31.55 km/h (https://www.rome2rio.com/map/Palma/Mahon-Airport-MAH) --> Rounding up to 30 km/h


    def calculate_co2(self, dist_km, vehicle_ferry, trip_type):
        """Calculate the CO2 eq emission of a ride by ferry."""

        pax_qty = 1 #possibility to expand to more than one person per trip for future calculations. Additional emissions due to vehicle would be divided by number of travellers

        ferry_co2_dict = self.ferry_co2_dict_from_json()
        g_co2_foot_pax = ferry_co2_dict['footPax']

        if vehicle_ferry == 'with-vehicle':
            g_co2_car_pax = ferry_co2_dict['carPax']
            g_co2_km = g_co2_car_pax + g_co2_foot_pax * (pax_qty-1)

        else:
            g_co2_km = g_co2_foot_pax * pax_qty

        gr_co2_person = int(dist_km * g_co2_km)

        if trip_type == "round-trip":
            gr_co2_person = gr_co2_person*2

        return int(gr_co2_person)


    def calculate_co2_from_duration(self, duration_in_minutes, vehicle_ferry, trip_type):
        """Calculate the CO2 eq emission of a ride by ferry, given a duration as input."""

        dist_km = self.estimate_distance_from_duration(duration_in_minutes)
        gr_co2_person = self.calculate_co2(dist_km, vehicle_ferry, trip_type)

        return int(gr_co2_person)


    def ferry_co2_dict_from_json(self):
        """Return a dictionary with the data for ferries from a given source."""

        relative_path = '/sources/gov_uk.json'
        gov_uk_dict = self.dict_from_json(relative_path)

        co2_dict = gov_uk_dict["gCO2"]["ferry"]

        return co2_dict


    def estimate_distance_from_duration(self, duration_in_minutes):
        """Given duration as input, estimate distance covered."""

        avg_speed_kmh = self.avg_speed_kmh
        dist_km = int(duration_in_minutes * avg_speed_kmh/60)

        return dist_km
