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

import pandas as pd
from preprocess.business import Processor

class ReviewProcessor(Processor):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def extract_useful_data(self, data):
        data = json.loads(data)
        if 'text' in data:
            data.pop('text')
        return data

    def handle_batch_data(self, batch_data):
        cleaned_lines = []
        table_path = os.path.join(self._dir_path, 'review_table.csv')
        is_header = (self._batch_iter == 0)
        if is_header and os.path.exists(table_path):
            os.remove(table_path)

        for data in batch_data:
            useful = self.extract_useful_data(data)
            cleaned_lines.append(useful)

        cleaned_df = pd.DataFrame(cleaned_lines)
        table_path = os.path.join(self._dir_path, 'review_table.csv')
        mode = 'w' if is_header else 'a'
        cleaned_df.to_csv(table_path,
                          mode=mode,
                          header=is_header)

        self._batch_iter += 1

if __name__ == '__main__':

    processor = ReviewProcessor()
    file_path = sys.argv[1]
    processor.process_data(file_path)