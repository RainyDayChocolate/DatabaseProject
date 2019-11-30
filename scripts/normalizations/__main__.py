"""This package normalize data downloaded from kaggle to csv format

"""
import argparse
import os

from .accident import AccidentNormalizer
from .flight_delay import FlightDelayNormalizer
from .gun_violence import GunViolenceNormalizer
from .weather import WeatherNormalizer


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--dataset', type=str, default='./dataset_test',
                     help='The main path of whole datas')


if __name__ == '__main__':
    args = parser.parse_args()
    dataset = args.dataset

    dataset_helper = lambda p: os.path.join(dataset, p)

    flight = 'flight_data.csv'
    flight_normalizer = FlightDelayNormalizer()
    locations, airports, flights, delays, flight_operations = \
        flight_normalizer.normalize(dataset_helper(flight))
    airports.to_csv()
    flights.to_csv()
    delays.to_csv()
    flight_operations.to_csv()

    gun = 'gun-violence-data_01-2013_03-2018.csv'
    gun_normalizer = GunViolenceNormalizer(locations=locations)
    incidents, locations = \
        gun_normalizer.normalize(dataset_helper(gun))
    incidents.to_csv()

    accident = 'US_Accidents_May19.csv'
    accident_normalizer = AccidentNormalizer(locations=locations)
    locations, accidents, accident_annotations = \
        accident_normalizer.normalize(dataset_helper(accident))
    locations.to_csv()
    accidents.to_csv()
    accident_annotations.to_csv()

    weather = 'weather'
    weather_normalier = WeatherNormalizer()
    weathers = weather_normalier.normalize(dataset_helper(weather))[0]
    weathers.to_csv()