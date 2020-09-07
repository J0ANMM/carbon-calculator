"""
    Run this file via the command file to test if the calculations are running as expected.

    > python3 tester.py
"""

from carbon_flight import CarbonFlight
from carbon_train import CarbonTrain
from carbon_bus import CarbonBus
from carbon_car import CarbonCar
from carbon_ferry import CarbonFerry


class CarbonCalculatorTester(object):
    """Class to test all Carbon objects."""

    def compare_flight_ferry(self):
        """"""

        dist_km = 400
        pax_class = "economy-class"
        trip_type = "round-trip"

        co2_flight = CarbonFlight().calculate_co2(dist_km, pax_class, trip_type)


        vehicle_ferry = "without-vehicle"
        hours_trip = 8
        duration_in_minutes = hours_trip*60

        co2_ferry = CarbonFerry().calculate_co2(duration_in_minutes, vehicle_ferry, trip_type)

        print("---- Travel FLIGHT vs FERRY", dist_km, " km or ", hours_trip, " hours ", trip_type, "passenger ----")
        print("Carbon footprint flying ", pax_class, ": ", co2_flight, "gCO2")
        print("Carbon footprint by ferry ", vehicle_ferry, ": ", co2_ferry, "gCO2")
        print()


    def compare_flight_train(self):
        """"""

        dist_km = 600
        trip_type = "one-way"
        pax_class = "economy-class"

        co2_flight = CarbonFlight().calculate_co2(dist_km, pax_class, trip_type)


        train_energy = "electric"
        train_country = "DE"

        co2_train = CarbonTrain().calculate_co2(dist_km, train_energy, train_country, trip_type)

        print("---- Travel FLIGHT vs TRAIN", dist_km, " km", trip_type, "----")
        print("Carbon footprint flight ", pax_class, ": ", co2_flight, "gCO2")
        print("Carbon footprint train ", train_energy, train_country, ": ", co2_train, "gCO2")
        print()


    def compare_train_bus_car(self):
        """"""

        dist_km = 600
        trip_type = "round-trip"
        pax_qty = 1
        train_energy = "electric"
        train_country = "DE"

        co2_train = CarbonTrain().calculate_co2(dist_km, train_energy, train_country, trip_type)
        co2_bus = CarbonBus().calculate_co2(dist_km, trip_type)

        print("---- Travel TRAIN vs BUS vs CAR", dist_km, " km", trip_type, "----")
        print("Carbon footprint train", "electric", "DE", "=", co2_train, "gCO2")
        print("Carbon footprint bus", "=", co2_bus, "gCO2")
        print()


    def compare_trains(self):
        """"""

        dist_km = 500
        trip_type = "one-way"

        co2_train_e_at = CarbonTrain().calculate_co2(dist_km=dist_km, train_energy="electric", train_country="AT", trip_type=trip_type)
        co2_train_e_de = CarbonTrain().calculate_co2(dist_km=dist_km, train_energy="electric", train_country="DE", trip_type=trip_type)
        co2_train_d_de = CarbonTrain().calculate_co2(dist_km=dist_km, train_energy="diesel", train_country="DE", trip_type=trip_type)
        co2_train_e_es = CarbonTrain().calculate_co2(dist_km=dist_km, train_energy="electric", train_country="ES", trip_type=trip_type)

        print("---- Travel TRAINs", dist_km, " km", trip_type, "----")
        print("Carbon footprint train", "electric", "AT", ": ", co2_train_e_at, "gCO2")
        print("Carbon footprint train", "electric", "DE", ": ", co2_train_e_de, "gCO2")
        print("Carbon footprint train", "diesel", "DE", ": ", co2_train_d_de, "gCO2")
        print("Carbon footprint train", "electric", "ES", ": ", co2_train_e_es, "gCO2")
        print()


    def compare_cars(self):
        """"""

        dist_km = 800
        trip_type = "one-way"

        co2_car_petrol_1 = CarbonCar().calculate_co2(dist_km=dist_km, fuel_type="petrol", fuel_consumption=8, energy_consumption=None, electricity_country_code=None, pax_in_car=1, trip_type=trip_type)
        co2_car_petrol_2 = CarbonCar().calculate_co2(dist_km=dist_km, fuel_type="petrol", fuel_consumption=8, energy_consumption=None, electricity_country_code=None, pax_in_car=2, trip_type=trip_type)
        co2_car_diesel = CarbonCar().calculate_co2(dist_km=dist_km, fuel_type="diesel", fuel_consumption=8, energy_consumption=None, electricity_country_code=None, pax_in_car=1, trip_type=trip_type)
        co2_car_e_ch_18 = CarbonCar().calculate_co2(dist_km=dist_km, fuel_type="electric", fuel_consumption=None, energy_consumption=18, electricity_country_code="CH", pax_in_car=1, trip_type=trip_type)
        co2_car_e_es_18 = CarbonCar().calculate_co2(dist_km=dist_km, fuel_type="electric", fuel_consumption=None, energy_consumption=18, electricity_country_code="ES", pax_in_car=1, trip_type=trip_type)
        co2_car_e_es_21 = CarbonCar().calculate_co2(dist_km=dist_km, fuel_type="electric", fuel_consumption=None, energy_consumption=21, electricity_country_code="ES", pax_in_car=1, trip_type=trip_type)
        co2_car_e_xx_21 = CarbonCar().calculate_co2(dist_km=dist_km, fuel_type="electric", fuel_consumption=None, energy_consumption=21, electricity_country_code="XX", pax_in_car=1, trip_type=trip_type)

        print("---- Travel CARs", dist_km, " km", trip_type, "----")
        print("Carbon footprint car", "petrol 8l", "1 pax", "=", co2_car_petrol_1, "gCO2")
        print("Carbon footprint car", "petrol 8l", "2 pax", "=", co2_car_petrol_2, "gCO2")
        print("Carbon footprint car", "diesel 8l", "1 pax", "=", co2_car_diesel, "gCO2")
        print("Carbon footprint car", "electric CH 18kWh/100km", "1 pax", "=", co2_car_e_ch_18, "gCO2")
        print("Carbon footprint car", "electric ES 18kWh/100km", "1 pax", "=", co2_car_e_es_18, "gCO2")
        print("Carbon footprint car", "electric ES 21kWh/100km", "1 pax", "=", co2_car_e_es_21, "gCO2")
        print("Carbon footprint car", "electric XX 21kWh/100km", "1 pax", "=", co2_car_e_xx_21, "gCO2")
        print()

    # def compare_cars(self):


if __name__ == "__main__":

    cct = CarbonCalculatorTester()

    cct.compare_flight_ferry()
    cct.compare_flight_train()
    cct.compare_trains()
    cct.compare_train_bus_car()
    cct.compare_cars()
