#!/usr/bin/env python3

from enum import Enum, auto

class Query_enum(Enum):
    ARRV_OR_DEP_DELAY_RATIO_AT_AIRPORT = auto()
    CAREER_DELAY_PROPORTION_IN_DAY_OR_HOUR = auto()
    CAREER_AVERAGE_DIST_FROM_AIRPPORT = auto()
    HIGHEST_ACCIDENT_RATE_ON_STREET = auto()
    AVERAGE_ACCIDENT_SEVERITY_IN_CITY = auto()
    TOTAL_GUN_VIOLENCE_OCC_ON_PARTICULAR_DAY = auto()
    RATIO_OF_GUN_VIOLENCE_SUSPECTS_TO_ALL_SUSPECTS = auto()
    PROP_DELAY_BY_WEATHER_VS_ALL_DELAYS = auto()
    PROP_ACIDENTS_DUE_TO_WEATHER_VS_ALL = auto()
    GET_ACCIDENT_INCIDENT_SEVERITY = auto()
    