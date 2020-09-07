"carbon-car.py calculates the emissions of passengers taking a car"

try:
    from carbon import Carbon
except ImportError:
    from results.carbon_calculator_git.carbon import Carbon #complete path inside Django project needed to make it work in Django Framework

class CarbonCar(Carbon):
    """Class to calculate CO2 emmissions in a car."""

    def __init__(self):
        self.diesel_well_to_tank = 2.58+0.62 #kg CO2/l #also considering emissions well-to-tank: https://www.nexxtlab.lu/co2-emissions-calculator/
        self.petrol_well_to_tank = 2.3+0.5 #kg CO2/l


    def calculate_co2(self, dist_km, fuel_type, fuel_consumption, electricity_consumption, electricity_country_code, pax_in_car, trip_type):
        """Calculate the CO2 eq emission of a ride by car."""

        if fuel_type == 'electric':
            # avg_consumption = 19.0 #kWh/100km

            kWh_per_100km = int(electricity_consumption)/0.83 #We consider a grid-to-battery conversion efficiency of 83%: http://publications.lib.chalmers.se/records/fulltext/179113/local_179113.pdf

            # this can be further improved by using more factors like here: https://www.nexxtlab.lu/co2-emissions-calculator/

            gCO2_per_kWh = self.ci_in_country(electricity_country_code)

            gr_co2_driving = int(kWh_per_100km * gCO2_per_kWh / 100.0)

        elif fuel_type == 'diesel' or fuel_type == 'petrol':
            kgCO2_per_litre = {
                                'diesel': self.diesel_well_to_tank,
                                'petrol': self.petrol_well_to_tank,
                                }

            gr_co2_driving = int( kgCO2_per_litre[fuel_type] * float(fuel_consumption) * 10.0 )

        else:
            print("fuel_type value is not valid. It must be one of the following: ['electric', 'diesel', 'petrol']")

        # gr_co2_infrastructure = 0
        # gr_co2_manufacturing = 0 #check how the other tm are calculated: https://docs.google.com/spreadsheets/d/1LzrAnx-NK0panXBKFvsqJUwYQPOv10FN

        gr_co2_person = gr_co2_driving * dist_km

        if trip_type == "round-trip":
            gr_co2_person = gr_co2_person*2

        if int(pax_in_car) > 1:
            gr_co2_person = gr_co2_person//pax_in_car + (gr_co2_person % pax_in_car > 0) #divide emissions of the car by number of passengers to get the footprint per person

        return int(gr_co2_person)
