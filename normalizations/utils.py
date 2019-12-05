"""This date
"""

from datetime import datetime
import pandas as pd

STATE_ABR_TO_NAME = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

# Here is a trick for filitering data
TRICK_CITIES = {'Albuquerque': 'NM',
                'Atlanta': 'GA',
                'Boston': 'MA',
                'Charlotte': 'NC',
                'Chicago': 'IL',
                'Dallas': 'TX',
                'Denver': 'CO',
                'Detroit': 'MI',
                'Houston': 'TX',
                'Indianapolis': 'IN',
                'Jacksonville': 'FL',
                'Kansas City': 'MO',
                'Las Vegas': 'NV',
                'Los Angeles': 'CA',
                'Miami': 'FL',
                'Minneapolis': 'MN',
                'Nashville': 'TN',
                'New York': 'NY',
                'Philadelphia': 'PA',
                'Phoenix': 'AZ',
                'Pittsburgh': 'PA',
                'Portland': 'OR',
                'Saint Louis': 'MO',
                'San Antonio': 'TX',
                'San Diego': 'CA',
                'San Francisco': 'CA',
                'Seattle': 'WA'}

TRICK_CITIES = {city: STATE_ABR_TO_NAME[state_abr]
                for city, state_abr in TRICK_CITIES.items()}
TRICK_YEAR = 2016

STATE_NAME_TO_ABR = {state: abr
                    for abr, state in STATE_ABR_TO_NAME.items()}


def convert_timeint(date, time_int):
    hour = str(int(time_int // 100) % 24)
    minutes = str(int(time_int % 100))
    time_string = '-'.join([date, hour, minutes])
    time_object = datetime.strptime(time_string, '%Y-%m-%d-%H-%M')
    return time_object


class Normalizer:

    def __init__(self, batch_size=10000):
        self.batch_size = batch_size

    def read_data(self, data_path, **params):
        datas_generators = pd.read_csv(data_path,
                                       chunksize=self.batch_size,
                                       usecols=self.columns_kept,
                                       **params)
        return datas_generators

    def _normalize(self, chunk):
        for number, record in chunk.iterrows():
            if not (number % 10000) and number:
                class_name = self.__class__.__name__
                print('{0} {1} Rows have been normalized'.format(class_name,
                                                                 number))
            self._normalize_record(record)

    def normalize(self, path):
        data_chunks = self.read_data(path)
        if isinstance(data_chunks, pd.DataFrame):
            self._normalize(data_chunks)
        else:
            for data_chunk in data_chunks:
                self._normalize(data_chunk)
        return self.relations

