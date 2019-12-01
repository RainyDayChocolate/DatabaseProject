"""This script is designed for normalizing accidents
"""

from .relations import Accidents, AccidentAnnotations, Locations
from .utils import Normalizer, STATE_ABR_TO_NAME, TRICK_CITIES

class AccidentNormalizer(Normalizer):

    def __init__(self,
                 locations=None,
                 accidents=None,
                 accident_annotations=None):
        super().__init__()
        self.locations = locations if locations else Locations()
        self.accidents = accidents if accidents else Accidents()
        self.accident_annotations = (accident_annotations if accident_annotations
                                     else AccidentAnnotations())
        self.relations = [self.locations,
                          self.accidents,
                          self.accident_annotations]
        self.accident_columns =['ID', 'Severity', 'Start_Time', 'End_Time',
                                'Distance(mi)',
                                'Street', 'Side', 'City', 'State',
                                'Visibility(mi)', 'Weather_Condition', 'Sunrise_Sunset']

        self.annotations_columns = ['Amenity', 'Bump', 'Crossing',
                                    'Give_Way', 'Junction', 'No_Exit',
                                    'Railway', 'Roundabout', 'Station',
                                    'Stop', 'Traffic_Calming', 'Traffic_Signal',
                                    'Turning_Loop']

        self.columns_kept = self.accident_columns + self.annotations_columns

    def _normalize_annotation(self, record):
         accident_id = record['ID']
         for annotation in self.annotations_columns:
             if record[annotation]:
                 self.accident_annotations.add_entity(accident_id=accident_id,
                                                      annotation=annotation.lower())

    def _normalize_accident(self, record):
        self.accidents.add_entity(accident_id=record['ID'],
                                  city=record['City'],
                                  state=STATE_ABR_TO_NAME[record['State']],
                                  street=record['Street'],
                                  severity=record['Severity'],
                                  start_time=record['Start_Time'],
                                  end_time=record['End_Time'],
                                  distance=record['Distance(mi)'],
                                  side=record['Side'],
                                  visibility=record['Visibility(mi)'],
                                  weather_condition=record['Weather_Condition'],
                                  sunrise_sunset=record['Sunrise_Sunset'])

    def _normalize_location(self, record):
        city = record['City']
        state_abr = record['State']
        state = STATE_ABR_TO_NAME[record['State']]
        self.locations.add_entity(city=city,
                                  state_abr=state_abr,
                                  state=state)

    def _normalize_record(self, record):
        if record['City'] not in TRICK_CITIES:
            return
        if TRICK_CITIES[record['City']] != \
            STATE_ABR_TO_NAME[record['State']]:
            return
        if record['Start_Time'][:4] != '2016': #Hard code Trick here
            return
        self._normalize_accident(record)
        self._normalize_annotation(record)
        self._normalize_location(record)


