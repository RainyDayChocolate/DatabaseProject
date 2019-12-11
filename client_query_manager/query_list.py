#!/usr/bin/env python3

from client_query_manager.specific_queries import *
from client_query_manager.query_type import Query_type

class Query_list:
    queryDict = dict()
    queryList = []

    def create_query_set(self, query_type):
        '''
        Help build both the queryDict and the queryList.
        '''
        if query_type is Query_type.CAREER_DEP_ARRV_DELAY_IN_AIRPORT:
            self.create_USFlightDelay_set()
        elif query_type is Query_type.US_ACCIDENT_OCURRENCE:
            self.create_USAccidents_set()
        elif query_type is Query_type.US_GUN_VIOLENCE:
            self.create_USGunViolence_set()
        else:
            raise ValueError('Query_list::create_query_set(): There is no query_type provided.')

    def create_USFlightDelay_set(self):
        '''
        Generate a tuple list to have the correspondence between key and values ready
        '''
        question1 = 'The ratio of delayed arrivals or departures at certain airport.'
        question2 = 'The average distance covered by certain career from certain airport.'
        question3 = 'The proportion of delays in hours or days by a certain career.'
        question4 = 'The percentage of flight delays due to severe weather conditions against all delays'

        self.queryDict = {
            Query_enum.ARRV_OR_DEP_DELAY_RATIO_AT_AIRPORT : question1,
            Query_enum.CAREER_AVERAGE_DIST_FROM_AIRPPORT : question2,
            Query_enum.CAREER_DELAY_PROPORTION_IN_DAY_OR_HOUR : question3,
            Query_enum.PROP_DELAY_BY_WEATHER_VS_ALL_DELAYS : question4
        }

        self.queryList = [question1,
                          question2,
                          question3,
                          question4
                         ]


    def create_USAccidents_set(self):
        question1 = 'The top accident rate ranking on the street in certain city'
        question2 = 'The average accident severity in a city in a particular day of the week'
        question3 = 'The percentage of accidents due to severe weather conditions vs all other accidents'
        question4 = 'The correlation between accident and gun violence nationwise'

        self.queryDict = {
            Query_enum.HIGHEST_ACCIDENT_RATE_ON_STREET : question1,
            Query_enum.AVERAGE_ACCIDENT_SEVERITY_IN_CITY : question2,
            Query_enum.PROP_ACIDENTS_DUE_TO_WEATHER_VS_ALL : question3,
            Query_enum.GET_ACCIDENT_INCIDENT_SEVERITY : question4
        }

        self.queryList = [question1,
                          question2,
                          question3
                         ]


    def create_USGunViolence_set(self):
        question1 = 'Total gun violence occurences on a particular day of the week'
        question2 = 'Percentage of arrested suspects due to gun violence against all other suspects'

        self.queryDict = {
            Query_enum.TOTAL_GUN_VIOLENCE_OCC_ON_PARTICULAR_DAY : question1,
            Query_enum.RATIO_OF_GUN_VIOLENCE_SUSPECTS_TO_ALL_SUSPECTS : question2
        }

        self.queryList = [  question1,
                            question2
                         ]


    def getQueryHashTable(self):
        return self.queryDict


    def getQueryList(self):
        return self.queryList