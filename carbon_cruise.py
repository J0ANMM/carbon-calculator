"carbon_cruise.py calculates the emissions of passengers travelling on a cruise"

try:
    from carbon import Carbon
except ImportError:
    from results.carbon_calculator_git.carbon import Carbon #complete path inside Django project needed to make it work in Django Framework


class CarbonCruise(Carbon):
    """Class to calculate CO2 emmissions in cruises."""

    def __init__(self):
        self.avg_speed_kmh = 40 #based on the information on this page: https://www.cruisemapper.com/wiki/762-cruise-ship-cruising-speed


    def calculate_co2(self, dist_km, trip_type):
        """Calculate the CO2 eq emission of a ride by cruise."""

        pax_qty = 1 #possibility to expand to more than one person per trip for future calculations. Additional emissions due to vehicle would be divided by number of travellers

        cruise_co2_dict = self.cruise_co2_dict_from_json()
        g_co2_foot_pax = cruise_co2_dict['footPax']
        g_co2_km = g_co2_foot_pax * pax_qty

        gr_co2_person = int(dist_km * g_co2_km)

        if trip_type == "round-trip":
            gr_co2_person = gr_co2_person*2

        return int(gr_co2_person)


    def calculate_co2_from_duration(self, duration_in_days, trip_type):
        """Calculate the CO2 eq emission of a ride by cruise, given a duration as input."""

        dist_km = self.estimate_distance_from_duration(duration_in_days)
        gr_co2_person = self.calculate_co2(dist_km, trip_type)

        return int(gr_co2_person)


    def cruise_co2_dict_from_json(self):
        """Return a dictionary with the data for cruises from a given source."""

        relative_path = '/sources/cruise_emissions.json'
        cruise_emissions_dict = self.dict_from_json(relative_path)

        co2_dict = cruise_emissions_dict["gCO2"]["cruise"]

        return co2_dict


    def estimate_distance_from_duration(self, duration_in_days):
        """Given duration as input, estimate distance covered."""

        avg_speed_kmh = self.avg_speed_kmh
        dist_km = int(duration_in_days * avg_speed_kmh * 24)

        return dist_km
