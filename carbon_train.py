"carbon-train.py calculates the emissions of passengers taking a train"

try:
    from carbon import Carbon
except ImportError:
    from results.carbon_calculator_git.carbon import Carbon #complete path inside Django project needed to make it work in Django Framework


class CarbonTrain(Carbon):
    """Class to calculate CO2 emmissions travelling by train."""

    def __init__(self):
        self.gr_co2_diesel = 74 #source = https://www.railplus.com.au/pdfs/ATOC-rail-is-greener-report.pdf


    def calculate_co2(self, dist_km, train_energy, train_country, trip_type):
        """Calculate the CO2 eq emission of a ride by train."""

        if train_energy == 'electric':
            # print('Train is powered by electricity')
            gr_co2 = self.electric_rail_emissions(train_country)
        else:
            # print('Train is powered by diesel')
            gr_co2 = self.gr_co2_diesel

        # infrastructure_footprint = 0 #not yet considered
        # vehicle_production_footprint = 0 #not yet considered

        gr_co2_person = gr_co2 * dist_km

        if trip_type == "round-trip":
            gr_co2_person = gr_co2_person*2

        return int(gr_co2_person)


    def electric_rail_emissions(self, country_code):
        """Return gr CO2 / pkm for electric trains depending on the country."""

        electric_consumption = 0.108 #kWh / pkm for electric trains. Source: https://www.railplus.com.au/pdfs/ATOC-rail-is-greener-report.pdf

        if country_code == 'DE':
            # gCO2_per_kWh = 230 #2019 #https://www.deutschebahn.com/resource/blob/5029910/5bdee6f2cac4fc869ad491d141539be9/Integrierter-Bericht-2019-data.pdf
            gCO2_per_kWh = self.calculate_ci_in_grid("deutsche-bahn")
        elif country_code == 'AT':
            # gCO2_per_kWh = 59 # See https://docs.google.com/spreadsheets/d/1gxMfqTNyyo8oJEU3__MqZ68T97Hl0466mDHsCTvGbE0
            gCO2_per_kWh = self.calculate_ci_in_grid("oebb")
        else:
            #Spain is 80% electric and 20% diesel: https://www.renfe.com/es/es/grupo-renfe/transporte-sostenible/eficiencia-energetica.html
            gCO2_per_kWh = self.ci_in_country(country_code)

        carbon_emissions = electric_consumption * gCO2_per_kWh

        return carbon_emissions


    def calculate_ci_in_grid(self, grid_name):
        """Calculate the Carbon Intensity of a grid. Units: g CO2 / kWh"""

        e_mix = self.electricity_mix_perc(grid_name)

        ci_by_source_dict = self.ci_by_source_dict_from_json()

        ci_grid = 0
        for energy_source, percent in e_mix.items():
            ci_this_source = ci_by_source_dict[energy_source] * (percent/100)
            ci_grid = ci_grid + ci_this_source

        return ci_grid


    def electricity_mix_perc(self, grid_name):
        """Return a dictionary with the percentages of electricity generation by source."""

        relative_path = '/sources/electricity_mixes.json'
        ci_by_source_dict = self.dict_from_json(relative_path)

        e_grids = ci_by_source_dict["electricityGrid"]

        this_grid = next((item for item in e_grids if item["gridOwner"] == grid_name), None) #find dict in the list of dicts

        e_mix = this_grid["electricityMix"]

        return e_mix



    def ci_by_source_dict_from_json(self):
        """Return a dictionary with the data for flights from a given source."""

        relative_path = '/sources/ci_by_source.json'
        ci_by_source_dict = self.dict_from_json(relative_path)

        source_cis = ci_by_source_dict["energySource"]

        return source_cis
