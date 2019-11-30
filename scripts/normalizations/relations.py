"""This script defines basic relations for furthur use"""

import os

from pandas import DataFrame, Series


class Relation:

    def to_dataframe(self):
        columns = tuple()
        if '_keys_names' in self.__dict__:
            columns = self._keys_names
        if '_values_names' in self.__dict__:
            columns += self._values_names
        if isinstance(self.table, set):
            table = DataFrame(self.table, columns=columns)
        elif isinstance(self.table, dict):
            helper = [key + value
                      for key, value in self.table.items()]
            try:
                table = DataFrame(helper, columns=columns)
            except:
                import pdb; pdb.set_trace()

        return table

    def to_csv(self, path=None):
        relation_name = self.__class__.__name__
        if not path:
            # Hard code for the path, lazy to optimize.
            data_dir = './normalized'
            if not os.path.exists(data_dir):
                os.mkdir(data_dir)

            path = os.path.join(data_dir, relation_name)

        df = self.to_dataframe()
        header = not os.path.exists(path)
        if header:
            df.to_csv(path, index=False, header=header)
        else:
            df.to_csv(path, index=False, header=header, mode='a')

    def clear_table(self):
        self.table.clear()

    def auto_save(self):
        max_table_size = 100000
        if len(self.table) >= max_table_size:
            self.to_csv()
            self.clear_table()


class Locations(Relation):

    def __init__(self):
        self.table = {}
        self._keys_names = ('city', 'state_abr')
        self._values_names = ('state', )

    def add_entity(self, city=None,
                         state_abr=None,
                         state=None):
        key = (city, state_abr)
        value = (state, )
        if key not in value:
            self.table[key] = value
        elif self.table[key] != value:
            raise ValueError('City State_Abr FD violated')

    def is_key_in(self, city, state_abr):
        if city is None or state_abr is None:
            raise ValueError('City and State ABR should not be None')
        return (city, state_abr) in self.table


class Airports(Relation):

    def __init__(self):
        self.table = set()
        self._keys_names = ('city', 'state_abr', 'airport')

    def add_entity(self, city=None,
                         state_abr=None,
                         airport=None):
        self.table.add((city, state_abr, airport))

    def is_key_in(self, city, state_abr, airport):
        return (city, state_abr, airport) in self.table


class Delays(Relation):

    def __init__(self):
        """This Relation could be saved along with normalization"""
        self.table = {}
        self._keys_names = ('flight_operation_id', 'delay_reason')
        self._values_names = ('delay', )

    def add_entity(self, flight_operation_id,
                         delay_reason,
                         delay):

        key = (flight_operation_id, delay_reason)
        values = (delay,)
        self.table[key] = values


class Flights(Relation):

    def __init__(self):
        """This Relation could be saved along with normalization"""
        self.index = 0
        self.table = set()
        self._keys_names = ('carrier', 'flight_num',
                            'dep', 'arr')

    def add_entity(self, carrier,
                         flight_num,
                         dep, arr):
        values = (carrier, flight_num, dep, arr)
        self.table.add(values)
        # Hard code for chunksize............
        self.auto_save()


class FlightsOperations(Relation):

    def __init__(self):
        self.index = 0
        self.table = set()
        self._values_names = ('flight_id',
                              'carrier',
                              'flight_num',
                              'crs_dep_date', 'dep_date',
                              'crs_arr_date', 'arr_date',
                              'crs_elapsed_time',
                              'actual_elapsed_time',
                              'air_time',
                              'distance')

    def add_entity(self, carrier,
                         flight_num,
                         crs_dep_date,
                         dep_date,
                         crs_arr_date,
                         arr_date,
                         crs_elapsed_time,
                         actual_elapsed_time,
                         air_time,
                         distance):

        values = (self.index, carrier, flight_num,
                  crs_dep_date, dep_date,
                  crs_arr_date, arr_date,
                  crs_elapsed_time, actual_elapsed_time,
                  air_time, distance)
        self.table.add(values)
        self.index += 1

        self.auto_save()


class Incidents(Relation):

    def __init__(self):
        self.table = {}
        self._keys_names = ('incident_id', )
        self._values_names = ('date', 'city', 'state', 'address',
                             'state_house_district',
                             'killed_num', 'injured_num',
                             'n_guns_involved', 'participants')

    def add_entity(self, incident_id,
                   date, city, state, address, state_house_district,
                   kill_num, injured_num,
                   n_guns_involved, participants):

        key = (incident_id, )
        value = (date, city, state, address, state_house_district,
                 kill_num, injured_num,
                 n_guns_involved, participants)

        self.table[key] = value
        self.auto_save()


class Weathers(Relation):

    def __init__(self):
        self.table = {}
        self._keys_names = ('city', 'date')
        self._values_names = ('humidity',
                              'pressure',
                              'temperature',
                              'wind_speed',
                              'wind_direction',
                              'weather_description')

    def add_entity(self, city, date,
                   humidity, pressure,
                   temperature, wind_speed,
                   wind_direction,
                   weather_description):
        key = (city, date)
        values = (humidity, pressure,
                  temperature, wind_speed,
                  wind_direction,
                  weather_description)
        self.table[key] = values
        self.auto_save()


class Accidents(Relation):

    def __init__(self):
        self.table = {}
        self._keys_names = ('accident_id', )
        self._values_names = ('city', 'state', 'street',
                              'severity', 'start_Time', 'end_Time',
                              'distance', 'side',
                              'visibility', 'weather_condition',
                              'sunrise_sunset')

    def add_entity(self, accident_id, city, state, street,
                   severity, start_time, end_time,
                   distance, side, visibility, weather_condition,
                   sunrise_sunset):

        key = (accident_id, )
        values = (city, state, street,
                  severity, start_time, end_time,
                  distance, side, visibility, weather_condition,
                  sunrise_sunset)

        self.table[key] = values
        self.auto_save()

class AccidentAnnotations(Relation):

    def __init__(self):
        self.table = set()
        self._keys_names = ('accident_id', 'annotation')

    def add_entity(self, accident_id, annotation):
        self.table.add((accident_id, annotation))
        self.auto_save()
