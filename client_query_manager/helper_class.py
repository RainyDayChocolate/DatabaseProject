#!/usr/bin/env python3

import re
from pprint import pprint

import regex
from PyInquirer import ValidationError, Validator, prompt

from database_operation.querier import Querier
from client_query_manager import custom_style_3


class Helper_class:
    def getKey_from_dict(self, in_dict, value):
        if not in_dict:
            raise ValueError('The input dictionary is empty.')

        try:
            key_list = list( in_dict.keys() )
            val_list = list( in_dict.values() )
            return key_list[ val_list.index(value) ]
        except Exception as err:
            print('Helper_class::getKey_from_dict(): {}'.format(err))
            return None

    def getAnswersFromQuestionSet(self, question_set):
        return prompt( question_set, style = custom_style_3 )

    def getAllStatesAndAbbr(self):
        inquirer = Querier()

        sql_query = """
                    SELECT state, state_abr
                    FROM locations
                    """
        allstateAndAbbr = inquirer.query_sql(sql_query)

        allStateAndAbbrList = []
        for state, state_abr in allstateAndAbbr:
            allStateAndAbbrList.append(str(state) + ', ' + str(state_abr))

        return allStateAndAbbrList

    def get_all_cities_and_states_list(self):
        sql_query = """
                    SELECT city, state
                    FROM locations ;
                    """

        inquirer = Querier()
        city_state_tuple = inquirer.query_sql(sql_query)

        city_list = []
        for city, state in city_state_tuple:
            city_list.append( str(city + ', ' + state) )

        return city_list

    def get_weather_list(self):
        sql_query = """
                    SELECT DISTINCT weather_description
                    FROM weathers ;
                    """
        inquirer = Querier()

        weather_list = []
        for i in inquirer.query_sql( sql_query ):
            weather_list.append( i[0] )

        return weather_list

    def get_carriers_and_abbr(self):
        sql_query = """
                    SELECT carrier, carrier_name
                    FROM carriers
                    """
        inquirer = Querier()
        airports_and_abbr_tuple = inquirer.query_sql(sql_query)

        airportAndAbbrList = {}
        for abbr, airport in airports_and_abbr_tuple:
            airportAndAbbrList.update( {airport : abbr} )

        return airportAndAbbrList

    def get_all_airports_abbr(self):
        sql_query = """
                    SELECT airport
                    FROM airports
                    """
        airportAbbrList = []

        inquirer = Querier()
        for abbr in inquirer.query_sql( sql_query ):
            airportAbbrList.append( abbr[0] )

        return airportAbbrList

    def get_city_and_state_tuple(self, city_and_state_string, pattern = ', '):
        city_state_tuple = re.split(pattern, city_and_state_string)
        return city_state_tuple[0], city_state_tuple[1]

# PyInquirer related classes
class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end
