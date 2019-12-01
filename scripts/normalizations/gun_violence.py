"""This script is designed for normalizing gun violence
"""

import re

import numpy as np

from .relations import Incidents, Locations
from .utils import STATE_NAME_TO_ABR, TRICK_CITIES, Normalizer


def record_to_dict(record):
    if isinstance(record, float):
        record = ''
    if record:
        sep = '||' if '||' in record else '|'
        records = record.split(sep)
        detail_sep = '::' if '::' in record else ':'
        records = [re.split(detail_sep, rec)
                   for rec in records]
        records = dict(records)
        return records
    return {}


def add_client_message(information_table,
                       records_dict, tag):
    for parti_id, record  in records_dict.items():
        if tag == 'age':
            record = eval(record)
        information_table[int(parti_id)][tag] = record


class GunViolenceNormalizer(Normalizer):

    def __init__(self, locations=None,
                       incidents=None):
        super().__init__()
        self.incidents = incidents if incidents else Incidents()
        self.locations = locations if locations else Locations()
        self.columns_kept = ['incident_id', 'date', 'state', 'city_or_county', 'address',
                             'n_killed', 'n_injured', 'n_guns_involved', 'state_house_district',
                             'participant_age', 'participant_age_group',
                             'participant_gender', 'participant_name',
                             'participant_status', 'participant_type']
        self.relations =  [self.incidents, self.locations]

    def _normalize_record(self, record):
        record = record.fillna(0)
        city = record['city_or_county']
        if city not in TRICK_CITIES:
            return
        if record['date'][:4] != '2016': #Hard code Trick here
            return
        date=record['date']
        state = record['state']
        if TRICK_CITIES[city] != state:
            return

        state_abr = STATE_NAME_TO_ABR[record['state']]
        self.locations.add_entity(city=city,
                                  state_abr=state_abr,
                                  state=state)

        tags = ['participant_age', 'participant_age_group',
                'participant_gender',
                'participant_status', 'participant_type']

        message_params = {}
        for tag in tags:
            try:
                record[tag] = record_to_dict(record[tag])
                tag_split = '_'.join(tag.split('_')[1:] + ['record'])
                message_params[tag_split] = record[tag]
            except:
                return

        participants_message = self.participants_to_dict(**message_params)
        self.incidents.add_entity(incident_id=record['incident_id'],
                                  state_house_district=record['state_house_district'],
                                  date=record['date'],
                                  city=city,
                                  state=state,
                                  address=record['address'],
                                  kill_num=record['n_killed'],
                                  injured_num=record['n_injured'],
                                  n_guns_involved=record['n_guns_involved'],
                                  participants=participants_message)

    @staticmethod
    def participants_to_dict(gender_record,
                             age_record,
                             age_group_record,
                             type_record,
                             status_record):
        """Return a List of Participant information
        {'age': XX, 'name': ss, 'Type': sss}
        """
        clients_messages = [{} for _ in type_record]

        add_client_message(clients_messages,
                           gender_record,
                           'gender')

        add_client_message(clients_messages,
                           age_record,
                           'age')

        add_client_message(clients_messages,
                           age_group_record,
                           'age_group')

        add_client_message(clients_messages,
                           type_record,
                           'type')

        status_record = {parti: status.split(',')
                         for parti, status in status_record.items()}

        add_client_message(clients_messages, status_record,
                           'status')

        return clients_messages
