"""This script is designed for normalizing Weather Data
"""

import os

import pandas as pd

from .relations import Weathers
from .utils import Normalizer


class WeatherNormalizer(Normalizer):

    def __init__(self,
                 weathers=None):
        super().__init__()
        self.weathers = weathers if weathers else Weathers()
        self.relations =  [self.weathers]

    def read_data(self, data_path, **params):

        path_helper = lambda p: os.path.join(data_path, p + '.csv')
        weather_attributes = ['humidity', 'pressure',
                              'temperature', 'weather_description',
                              'wind_direction', 'wind_speed']
        to_concated = []
        for attribute in weather_attributes:
            attribute_table = pd.read_csv(path_helper(attribute))
            attribute_table.fillna(method='ffill', inplace=True)
            attribute_table.fillna(method='bfill', inplace=True)
            attribute_table.set_index('datetime', inplace=True)
            attribute_table = attribute_table.unstack()
            attribute_table.index.names = ['city', 'date']
            attribute_table.name = attribute

            to_concated.append(attribute_table)

        weather_table = pd.concat(to_concated, axis=1)
        weather_table = weather_table.reset_index()
        city_desc = pd.read_csv(path_helper('city_attributes'))
        city_desc = city_desc[(city_desc.Country == 'United States')]

        weather_table = weather_table[weather_table['city'].isin(city_desc['City'])]
        return weather_table

    def _normalize_record(self, record):
        if record['date'][:4] !='2016': #Hard code Trick here
            return
        record = record.to_dict()
        self.weathers.add_entity(**record)



