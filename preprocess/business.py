"""This script is designed to handle business(shop) data.

Each record is in the format of
{"business_id":"gbQN7vr_caG_A1ugSmGhWg",
"name": "Supercuts",
"address": "4545 E Tropicana Rd Ste 8, Tropicana",
"city": "Las Vegas",
"state": "NV",
"postal_code": "89121",
"latitude": 36.099872,
"longitude": -115.074574,
"stars": 3.5,
"review_count": 3,
"is_open": 1,
"attributes":
    {"RestaurantsPriceRange2": "3",
    "GoodForKids": "True",
    "BusinessAcceptsCreditCards": "True",
    "ByAppointmentOnly": "False",
    "BikeParking":"False"},
"categories":"Hair Salons,
             Hair Stylists,
             Barbers,
             Men's Hair Salons,
             Cosmetics & Beauty Supply,
             Shopping, Beauty & Spas",
"hours":{"Monday": "10:0-19: 0",
        "Tuesday":"10:0-19: 0",
        "Wednesday":"10:0-19:0",
        "Thursday":"10:0-19:0",
        "Friday":"10:0-19:0",
        "Saturday":"10:0-19:0",
        "Sunday":"10:0-18:0"}}

We'd like to transform each record to 2 parts

1st: basic_information, A relational table
{"business_id":"gbQN7vr_caG_A1ugSmGhWg",
"name": "Supercuts",
"address": "4545 E Tropicana Rd Ste 8, Tropicana",
"city": "Las Vegas",
"state": "NV",
"postal_code": "89121",
"latitude": 36.099872,
"longitude": -115.074574,
"stars": 3.5,
"review_count": 3,
"is_open": 1}

2nd extension:
Database attribute and categories.
{business_id: 'gbQN7vr_caG_A1ugSmGhWg'
"attributes":
    {"RestaurantsPriceRange2": "3",
    "GoodForKids": "True",
    "BusinessAcceptsCreditCards": "True",
    "ByAppointmentOnly": "False",
    "BikeParking":"False"},
"categories":"Hair Salons,
             Hair Stylists,
             Barbers,
             Men's Hair Salons,
             Cosmetics & Beauty Supply,
             Shopping, Beauty & Spas"}

"""


__author__ = "Kuangzheng Li"
__project__ = 'ITWS Database'
__email__ = 'lik15@rpi.edu'


import json
import os
import re
import sys
from itertools import islice

import pandas as pd


class Processor:

    def __init__(self, dir_path='./cleaned_dataset', batch_size=10000):
        self._batch_size = batch_size
        self._batch_iter = 0
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        self._dir_path = dir_path

    def handle_attributes_categories(self, data):
        attributes = data['attributes']
        if attributes is None:
            attributes = []
        categories = data['categories']
        if categories is not None:
            categories = re.split(', ', categories)
        data['categories'] = categories
        data['attributes'] = attributes

        return data

    def split_data(self, data):
        data = json.loads(data)
        if 'business_id' not in data:
            return None, None
        basic_infor = {}
        basic_keys = ['business_id', 'name', 'address',
                      'city', 'state', 'postal_code',
                      'latitude', 'longitude',
                      'stars', 'review_count', 'is_open']
        for to_add_key in basic_keys:
            basic_infor[to_add_key] = data.get(to_add_key, '')

        extension_infor = {'business_id': data['business_id'],
                           'attributes': data.get('attributes', []),
                           'categories': data.get('categories', '')}
        return basic_infor, extension_infor

    def handle_batch_data(self, batch_data):
        cleaned_lines, cleaned_jsons = [], []

        json_path = os.path.join(self._dir_path,
                                'business_attributes.json')
        table_path = os.path.join(self._dir_path, 'business_table.csv')

        is_header = (self._batch_iter == 0)
        if is_header:
            if os.path.exists(table_path):
                os.remove(table_path)
            if os.path.exists(json_path):
                os.remove(json_path)

        if os.path.exists(json_path) and self._batch_iter == 0:
            os.remove(json_path)
        for data in batch_data:
            basic_infor, extension_infor = self.split_data(data)
            if not basic_infor:
                continue
            cleaned_lines.append(basic_infor)
            handled = self.handle_attributes_categories(extension_infor)
            with open(json_path, 'a') as f:
                f.write(json.dumps(handled))
                f.write('\n')

        mode = 'w' if is_header else 'a'
        cleaned_df = pd.DataFrame(cleaned_lines)
        cleaned_df.to_csv(table_path,
                          mode=mode,
                          header=is_header)
        self._batch_iter += 1

    def process_data(self, file_path):
        with open(file_path) as f:
            finished = 0
            while True:
                batch_datas = list(islice(f, self._batch_size))  # need list to do len, 3 lines down
                self.handle_batch_data(batch_datas)
                finished += len(batch_datas)
                print('{} lines have been cleaned'.format(finished))
                if len(batch_datas) < self._batch_size:
                    break


if __name__ == '__main__':

    processor = Processor()
    file_path = sys.argv[1]
    processor.process_data(file_path)
