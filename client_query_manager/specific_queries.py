#!/usr/in/env python3

from app.explorations import Explorations
from client_query_manager.query_enum import Query_enum
from client_query_manager.helper_class import Helper_class

class Specific_queries:
    query_table = dict()
    queryKey = None
    queryResp = None
    helper = Helper_class()

    def import_query_table(self, queryDict):
        self.query_table = queryDict

    def setQueryReq(self, request):
        '''
        The request sent in as a phrase in the string format.
        Look up the string phrase to its corresponding key, and 
        have the requested query executed.
        '''
        try:
            self.queryKey = self.helper.getKey_from_dict(self.query_table, request)
        except Exception as err:
            print('Specific_queries::setQueryReq(): {}'.format(err))
            return

        if self.queryKey is Query_enum.ARRV_OR_DEP_DELAY_RATIO_AT_AIRPORT:
            self.arrv_or_dep_delay_ratio_at_airport()
        elif self.queryKey is Query_enum.CAREER_DELAY_PROPORTION_IN_DAY_OR_HOUR:
            self.career_delay_proportion_in_day_or_hour()
        elif self.queryKey is Query_enum.CAREER_AVERAGE_DIST_FROM_AIRPPORT:
            self.career_average_dist_from_airpport()
        elif self.queryKey is Query_enum.HIGHEST_ACCIDENT_RATE_ON_STREET:
            self.highest_accident_rate_on_street()
        elif self.queryKey is Query_enum.AVERAGE_ACCIDENT_SEVERITY_IN_CITY:
            self.average_accident_severity_in_city()
        elif self.queryKey is Query_enum.TOTAL_GUN_VIOLENCE_OCC_ON_PARTICULAR_DAY:
            self.total_gun_violence_occ_on_particular_day()
        elif self.queryKey is Query_enum.RATIO_OF_GUN_VIOLENCE_SUSPECTS_TO_ALL_SUSPECTS:
            self.ratio_of_gun_violence_suspects_to_all_suspects()
        elif self.queryKey is Query_enum.PROP_DELAY_BY_WEATHER_VS_ALL_DELAYS:
            self.prop_delay_by_weather_vs_all_delays()
        elif self.queryKey is Query_enum.PROP_ACIDENTS_DUE_TO_WEATHER_VS_ALL:
            self.prop_acidents_due_to_weather_vs_all()

    # The queries
    def arrv_or_dep_delay_ratio_at_airport(self):
        pass

    def career_delay_proportion_in_day_or_hour(self):
        pass

    def career_average_dist_from_airpport(self):
        pass

    def highest_accident_rate_on_street(self):
        pass

    def average_accident_severity_in_city(self):
        pass

    def total_gun_violence_occ_on_particular_day(self):
        pass

    def ratio_of_gun_violence_suspects_to_all_suspects(self):
        pass

    def prop_delay_by_weather_vs_all_delays(self):
        pass

    def prop_acidents_due_to_weather_vs_all(self):
        pass

    def getQueryResp(self):
        return self.queryResp
