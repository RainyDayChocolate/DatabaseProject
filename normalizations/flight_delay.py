"""This script is designed for normalizing Flight Delay.
"""
import re

from .relations import Airports, Delays, Flights, FlightsOperations, Locations
from .utils import Normalizer, convert_timeint, TRICK_CITIES


class FlightDelayNormalizer(Normalizer):

    def __init__(self,
                 locations=None,
                 airports=None,
                 flights=None,
                 delays=None,
                 flight_operations=None):
        super().__init__()
        self.locations = locations if locations else Locations()
        self.airports = airports if airports else Airports()
        self.delays = delays if delays else Delays()
        self.flight_operations = flight_operations if flight_operations else FlightsOperations()
        self.relations = [self.locations, self.airports,
                          self.delays, self.flight_operations]

        self.columns_kept = ['FL_DATE', 'UNIQUE_CARRIER', 'FL_NUM',
                             'ORIGIN', 'ORIGIN_CITY_NAME', 'ORIGIN_STATE_ABR', 'ORIGIN_STATE_NM',
                             'DEST', 'DEST_CITY_NAME', 'DEST_STATE_ABR', 'DEST_STATE_NM',
                             'CRS_DEP_TIME', 'DEP_TIME', 'DEP_DELAY',
                             'CRS_ARR_TIME', 'ARR_TIME', 'ARR_DELAY',
                             'CRS_ELAPSED_TIME', 'ACTUAL_ELAPSED_TIME',
                             'AIR_TIME', 'DISTANCE',
                             'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY',
                             'LATE_AIRCRAFT_DELAY']

    def _normalize_location_airport(self, **location_params):
        for city in location_params['cities']:
            self.locations.add_entity(city=city,
                                      state_abr=location_params['state_abr'],
                                      state=location_params['state'])
            self.airports.add_entity(city=city,
                                     state=location_params['state'],
                                     airport=location_params['airport'])

    def _normalize_flight_operation(self, record):
        flight_date = record['FL_DATE']
        crs_dep_date = convert_timeint(flight_date, record['CRS_DEP_TIME'])
        dep_date = convert_timeint(flight_date, record['DEP_TIME'])
        crs_arr_date = convert_timeint(flight_date, record['CRS_ARR_TIME'])
        arr_date = convert_timeint(flight_date, record['ARR_TIME'])

        flight_operation_id = self.flight_operations.index
        self.flight_operations.add_entity(carrier=record['UNIQUE_CARRIER'],
                                          flight_num=record['FL_NUM'],
                                          dep=record['ORIGIN'],
                                          arr=record['DEST'],
                                          crs_dep_date=crs_dep_date,
                                          dep_date=dep_date,
                                          crs_arr_date=crs_arr_date,
                                          arr_date=arr_date,
                                          crs_elapsed_time=record['CRS_ELAPSED_TIME'],
                                          actual_elapsed_time=record['ACTUAL_ELAPSED_TIME'],
                                          air_time=record['AIR_TIME'],
                                          distance=record['DISTANCE'])

        for reason in ['CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 'SECURITY_DELAY',
                        'LATE_AIRCRAFT_DELAY']:
            if record[reason] <= 0:
                continue
            self.delays.add_entity(flight_operation_id=flight_operation_id,
                                   delay_reason=reason.split('_')[0],
                                   delay=record[reason])

    def _normalize_record(self, record):
        record = record.fillna(0)
        departure_cities = re.split('/|, ', record['ORIGIN_CITY_NAME'])[:-1]
        arrive_cities = re.split('/|, ', record['DEST_CITY_NAME'])[:-1]
        if (len(departure_cities) * len(arrive_cities)) > 1:
            return
        if departure_cities[0] not in TRICK_CITIES:
            return
        if arrive_cities[0] not in TRICK_CITIES:
            return
        if TRICK_CITIES[departure_cities[0]] != record['ORIGIN_STATE_NM']:
            return
        if TRICK_CITIES[arrive_cities[0]] != record['DEST_STATE_NM']:
            return
        self._normalize_location_airport(cities=departure_cities,
                                         state=record['ORIGIN_STATE_NM'],
                                         state_abr=record['ORIGIN_STATE_ABR'],
                                         airport=record['ORIGIN'])

        self._normalize_location_airport(cities=arrive_cities,
                                         state=record['DEST_STATE_NM'],
                                         state_abr=record['DEST_STATE_ABR'],
                                         airport=record['DEST'])
        self._normalize_flight_operation(record)
