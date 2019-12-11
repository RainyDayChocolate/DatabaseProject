#!/usr/bin/env python3

import unittest

from client_query_manager.specific_queries import Specific_queries

class Specific_queries_testCase(unittest.TestCase):
    def setUp(self):
        self.inquirer = Specific_queries()

    def test_arrv_or_dep_delay_ratio_at_airport(self):
        self.inquirer.arrv_or_dep_delay_ratio_at_airport()

    def test_career_delay_proportion_in_day_or_hour(self):
        self.inquirer.career_delay_proportion_in_day_or_hour()

    def test_career_average_dist_from_airpport(self):
        self.inquirer.career_average_dist_from_airpport()

    def test_highest_accident_rate_on_street(self):
        self.inquirer.highest_accident_rate_on_street()

    def test_average_accident_severity_in_city(self):
        self.inquirer.average_accident_severity_in_city()

    def test_total_gun_violence_occ_on_particular_day(self):
        self.inquirer.total_gun_violence_occ_on_particular_day()

    def test_ratio_of_gun_violence_suspects_to_all_suspects(self):
        self.inquirer.ratio_of_gun_violence_suspects_to_all_suspects()

    def test_prop_delay_by_weather_vs_all_delays(self):
        self.inquirer.prop_delay_by_weather_vs_all_delays()

    def test_prop_acidents_due_to_weather_vs_all(self):
        self.inquirer.prop_acidents_due_to_weather_vs_all()

    def test_get_accident_incident_severity(self):
        self.inquirer.get_accident_incident_severity()


if __name__=='__main__':
    unittest.main()