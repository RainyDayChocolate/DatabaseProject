"""This package normalize data downloaded from kaggle to csv format

"""
import argparse
import json
import os
from xml.dom.minidom import parseString

import dicttoxml
import pandas as pd

from .accident import AccidentNormalizer
from .flight_delay import FlightDelayNormalizer
from .gun_violence import GunViolenceNormalizer
from .weather import WeatherNormalizer

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--dataset', type=str, default='../dataset_test',
                     help='The main path of whole datas')
args = parser.parse_args()
dataset = args.dataset


def normalize(datast):

    dataset_helper = lambda p: os.path.join(dataset, p)

    flight = 'flight_data.csv'
    flight_normalizer = FlightDelayNormalizer()
    locations, airports, delays, flight_operations = \
        flight_normalizer.normalize(dataset_helper(flight))
    airports.to_csv()
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

def refresh():
    # Hard code modification. Very ugly!!!
    accident_csv = pd.read_csv('./normalized_dataset/accidents')
    accident_csv['start_time'] = pd.to_datetime(accident_csv['start_time'])
    accident_csv['end_time'] = pd.to_datetime(accident_csv['end_time'])
    accident_csv['visibility'] = accident_csv['visibility'].fillna(10.0)
    accident_csv['weather_condition'] = accident_csv['weather_condition'].fillna('Unknown')

    incident_csv = pd.read_csv('./normalized_dataset/incidents')
    incident_csv['date'] = pd.to_datetime(incident_csv['date'])
    incident_csv['participants'] = \
        incident_csv['participants'].apply(lambda s: eval(s))

    helper = incident_csv.set_index(['incident_id'])
    helper = helper['participants']
    partipants_dict = helper.to_dict()
    partipants_dict = [{'incident_id': _id, 'participants': participant}
                        for _id, participant in partipants_dict.items()]

    my_item_func = lambda x: x[:-1]
    xml = dicttoxml.dicttoxml(partipants_dict,
                              custom_root='incidents',
                              attr_type=True,
                              item_func=my_item_func)
    pretty_xml = parseString(xml).toprettyxml()
    with open("./normalized_dataset/incident_participants.xml", "w") as f:
        f.write(pretty_xml)

    weather_csv = pd.read_csv('./normalized_dataset/weathers')
    weather_csv['date'] = pd.to_datetime(weather_csv['date'])
    weather_csv['temperature'] = \
        weather_csv['temperature'].apply(lambda s: 32 + (s - 273) * 1.8 if s > 100 else s)
    location_csv = pd.read_csv('./normalized_dataset/locations')

    weather_csv.to_csv('./normalized_dataset/Weathers', index=False)
    accident_csv.to_csv('./normalized_dataset/Accidents', index=False)
    incident_csv.to_csv('./normalized_dataset/Incidents', index=False)


if __name__ == '__main__':
    #normalize(dataset)
    refresh()
