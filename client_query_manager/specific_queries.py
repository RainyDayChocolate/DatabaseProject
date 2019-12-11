#!/usr/in/env python3

from app.explorations import Explorations
from client_query_manager.query_enum import Query_enum
from client_query_manager.helper_class import Helper_class, NumberValidator

from app.explorations import Explorations

class Specific_queries:
    query_table = dict()
    helper = Helper_class()
    explorer = Explorations()

    def import_query_table(self, queryDict):
        self.query_table = queryDict

    def sendQueryReq(self, request):
        '''
        The request sent in as a phrase in the string format.
        Look up the string phrase to its corresponding key, and 
        have the requested query executed.
        '''
        if request is Query_enum.ARRV_OR_DEP_DELAY_RATIO_AT_AIRPORT:
            self.arrv_or_dep_delay_ratio_at_airport()
        elif request is Query_enum.CAREER_DELAY_PROPORTION_IN_DAY_OR_HOUR:
            self.career_delay_proportion_in_day_or_hour()
        elif request is Query_enum.CAREER_AVERAGE_DIST_FROM_AIRPPORT:
            self.career_average_dist_from_airpport()
        elif request is Query_enum.HIGHEST_ACCIDENT_RATE_ON_STREET:
            self.highest_accident_rate_on_street()
        elif request is Query_enum.AVERAGE_ACCIDENT_SEVERITY_IN_CITY:
            self.average_accident_severity_in_city()
        elif request is Query_enum.TOTAL_GUN_VIOLENCE_OCC_ON_PARTICULAR_DAY:
            self.total_gun_violence_occ_on_particular_day()
        elif request is Query_enum.RATIO_OF_GUN_VIOLENCE_SUSPECTS_TO_ALL_SUSPECTS:
            self.ratio_of_gun_violence_suspects_to_all_suspects()
        elif request is Query_enum.PROP_DELAY_BY_WEATHER_VS_ALL_DELAYS:
            self.prop_delay_by_weather_vs_all_delays()
        elif request is Query_enum.PROP_ACIDENTS_DUE_TO_WEATHER_VS_ALL:
            self.prop_acidents_due_to_weather_vs_all()
        elif request is Query_enum.GET_ACCIDENT_INCIDENT_SEVERITY:
            self.get_accident_incident_severity()
        else:
            raise ValueError( 'Specific_queries::sendQueryReq(): Unknown query request.' )

    # The queries
    def arrv_or_dep_delay_ratio_at_airport(self):
        stateAndAbbrList = self.helper.getAllStatesAndAbbr()
        hub_states = self.helper.getAnswersFromQuestionSet( [
            {
                'type' : 'list',
                'name' : 'dep_state',
                'message' : 'Choose your departure state',
                'choices' : stateAndAbbrList
            },
            {
                'type' : 'list',
                'name' : 'arrv_state',
                'message' : 'Choose your arrival state',
                'choices' : stateAndAbbrList
            }
        ]
        ) # End of getAnswersFromQuestionSet

        dep_state_abbr = hub_states['dep_state'].split()[1]
        arrv_state_abbr = hub_states['arrv_state'].split()[1]

        answer = self.explorer.get_delay_ratio(dep_state_abbr, arrv_state_abbr)

        print(answer)

    # WIP
    def career_delay_proportion_in_day_or_hour(self):
        resp = self.helper.getAnswersFromQuestionSet([
            {
                'type' : 'rawlist',
                'name' : 'time_dimension',
                'message' : 'Do you want to inquirer the delay in hours or days?',
                'choices': ['hours', 'week']
            }
        ])

        # Set up time_dimension_id. 0 = hour, 1 = day
        time_dimension_id = None
        if (resp['time_dimension'] == 'hours'):
            time_dimension_id = 0
        else:
            time_dimension_id = 1
        
        # Set up carrier
        # TODO Correspondence of carrier full name to abbrevition relation
        carrier_abbr = 'AA'

        answer = self.explorer.get_carrier_delay_distribution(time_dimension_id, carrier_abbr)
        print(answer)

    def career_average_dist_from_airpport(self):
        airportAbbrList = self.helper.get_all_airports_abbr()
        resp = self.helper.getAnswersFromQuestionSet( [
            {
                'type' : 'list',
                'name' : 'dep_airport',
                'message' : 'Choose your departure state',
                'choices' : airportAbbrList
            }
        ])

        dep_airport_abbr = resp['dep_airport']

        answer = self.explorer.get_carrier_avg_distance(dep_airport_abbr)
        print(answer)

    def highest_accident_rate_on_street(self):
        citiesAndStatesList = self.helper.get_all_cities_and_states_list()

        resp = self.helper.getAnswersFromQuestionSet([
            {
                'type' : 'list',
                'name' : 'city_and_state',
                'message' : 'Which city to investigate?',
                'choices' : citiesAndStatesList
            },
            {
                'type' : 'input',
                'name' : 'limit_items',
                'message' : 'How many top ranks do you want to keep?',
                'validate' : NumberValidator,
                'default' : '1',
                'filter' : lambda val : int(val)
            }
        ])

        city, state = self.helper.get_city_and_state_tuple( resp['city_and_state'] )
        limit_items_num = resp['limit_items']

        answer = self.explorer.get_accident_street(city, state, limit_items_num)
        print(answer)

    def average_accident_severity_in_city(self):
        cityAndStateList = self.helper.get_all_cities_and_states_list()

        resp = self.helper.getAnswersFromQuestionSet([
            {
                'type' : 'list',
                'name' : 'city_and_state',
                'message' : 'Choose the city to investigate',
                'choices' : cityAndStateList
            },
            {
                'type' : 'rawlist',
                'name' : 'day_of_week',
                'message' : 'Choose the day of the week',
                'choices' : ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            }
        ])

        city, state = self.helper.get_city_and_state_tuple( resp['city_and_state'] )
        day_of_week = resp['day_of_week']

        day_id = None
        day_dict = {
            {'Monday'       : 1},
            {'Tuesday'      : 2},
            {'Wednesday'    : 3},
            {'Thursday'     : 4},
            {'Friday'       : 5},
            {'Saturday'     : 6},
            {'Sunday'       : 7}
        }

        day_id = day_dict[day_of_week]

        answer = self.explorer.get_avg_severity(city, state, day_id)
        print(answer)

    def total_gun_violence_occ_on_particular_day(self):
        cityAndStateList = self.helper.get_all_cities_and_states_list()

        resp = self.helper.getAnswersFromQuestionSet([
            {
                'type' : 'list',
                'name' : 'city_and_state',
                'message' : 'Choose the city to investigate',
                'choices' : cityAndStateList
            }
        ])

        city, state = self.helper.get_city_and_state_tuple( resp['city_and_state'] )

        answer = self.explorer.get_gun_dayofweek_occurance(city, state)
        print(answer)

    # TODO: Convert to percentage
    def ratio_of_gun_violence_suspects_to_all_suspects(self):
        cityAndStateList = self.helper.get_all_cities_and_states_list()

        resp = self.helper.getAnswersFromQuestionSet([
            {
                'type' : 'list',
                'name' : 'city_and_state',
                'message' : 'Choose the city to investigate',
                'choices' : cityAndStateList
            }
        ])

        city, state = self.helper.get_city_and_state_tuple( resp['city_and_state'] )
        print('State : {}'.format(state))
        answer = self.explorer.get_suspect_arrested_ratio(state)
        print(answer)

    def prop_delay_by_weather_vs_all_delays(self):
        resp = self.helper.getAnswersFromQuestionSet([
            {
                'type' : 'confirm',
                'name' : 'is_departure_flight',
                'message' : 'Is it a departuring flight?',
                'default' : False
            },
            {
                'type' : 'input',
                'name' : 'delay_minutes',
                'message' : 'Search for dealays of how many minutes?',
                'validate' : NumberValidator,
                'default' : '20',
                'filter' : lambda val : int(val)
            }
        ])

        is_departure = resp['is_departure_flight']
        delay_minutes = resp['delay_minutes']
        
        airportAbrList = self.helper.get_all_airports_abbr()
        airport = None
        if is_departure:
            from_which_airport = self.helper.getAnswersFromQuestionSet([
                {
                    'type' : 'list',
                    'name' : 'departure_airport',
                    'message' : 'Choose the airport of departure.',
                    'choices' : airportAbrList
                }
            ])
            airport = from_which_airport['departure_airport']
        else:
            to_which_airport = self.helper.getAnswersFromQuestionSet([
                {
                    'type' : 'list',
                    'name' : 'arrival_airport',
                    'message' : 'Choose the airport of departure.',
                    'choices' : airportAbrList
                }
            ])
            airport = to_which_airport['arrival_airport']
        
        answer = self.explorer.get_delay_weather_description(airport, is_departure, delay_minutes)
        print(answer)
            

    def prop_acidents_due_to_weather_vs_all(self):
        cityAndStateList = self.helper.get_all_cities_and_states_list()
        weatherList = self.helper.get_weather_list()

        resp = self.helper.getAnswersFromQuestionSet([
            {
                'type' : 'list',
                'name' : 'city_and_state',
                'message' : 'Choose the city to investigate',
                'choices' : cityAndStateList
            },
            {
                'type' : 'list',
                'name' : 'weather_condition',
                'message' : 'Choose the weather to investigate',
                'choices' : weatherList
            }
        ])

        city, state = self.helper.get_city_and_state_tuple( resp['city_and_state'] )
        weather_cond = resp['weather_condition']

        answer = self.explorer.get_avg_accident_with_weather(city, state, weather_cond)
        print(answer)

    def get_accident_incident_severity(self):
        answer = self.explorer.get_accident_incident_severity()
        print(answer)
