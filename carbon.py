"carbon.py contains the main class Carbon, from which all transport modes will inherit"

import os
import json

class Carbon(object):
    """Main class to calculate CO2 emmissions for different modes of transportation."""


    def dict_from_json(self, relative_path):
        """relative_path must include a leading slash and the format of the file, as well as any possible subfolders:
            '/subfolder/onefile.json' """

        json_folder = os.path.dirname(os.path.abspath(__file__))
        json_path = json_folder + relative_path

        with open(json_path) as json_data:

            json_as_dict = json.loads(json_data.read())

            json_data.close()

        return json_as_dict


    def ci_in_country(self, country_code):
        """Return the carbon intensity of a country"""

        relative_path = '/sources/electricity_emission_factors.json'
        ci_in_country_dict = self.dict_from_json(relative_path)

        try:
            ci_factor = ci_in_country_dict["factors"][country_code]["gCO2"]
        except KeyError as e:
            print('country_code not found. Taking average value instead')
            ci_factor = 295.8 #avg EU according to https://www.eea.europa.eu/data-and-maps/daviz/co2-emission-intensity-5/download.table

        return ci_factor
