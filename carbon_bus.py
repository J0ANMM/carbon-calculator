"carbon-bus.py calculates the emissions of passengers taking a bus"

try:
    from carbon import Carbon
except ImportError:
    from results.carbon_calculator_git.carbon import Carbon #complete path inside Django project needed to make it work in Django Framework

class CarbonBus(Carbon):
    """Class to calculate CO2 emmissions in a bus."""

    def calculate_co2(self, dist_km, trip_type):
        """Calculate the CO2 eq emission of a ride by bus."""

        bus_co2_dict = self.bus_co2_dict_from_json()
        g_co2_km = bus_co2_dict["coach"]
        gr_co2_person = dist_km * g_co2_km

        if trip_type == "round-trip":
            gr_co2_person = gr_co2_person*2

        return int(gr_co2_person)


    def bus_co2_dict_from_json(self):
        """Return a dictionary with the data for buses from a given source."""

        relative_path = '/sources/gov_uk.json'
        gov_uk_dict = self.dict_from_json(relative_path)

        co2_dict = gov_uk_dict["gCO2"]["bus"]

        return co2_dict
