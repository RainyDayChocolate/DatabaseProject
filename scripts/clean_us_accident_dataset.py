#! /usr/bin/env python

import pandas as pd

class Clean_US_Accident_dataset:
    def __init__(self, inputCSVFile):
        imported_dataset = pd.read_csv( inputCSVFile )
        
        cleaned_dataset = imported_dataset[ [ 'Severity'
                                            , 'Start_Time'
                                            , 'City'
                                            , 'State'
                                            , 'Zipcode'
                                            , 'Temperature(F)'
                                            , 'Wind_Chill(F)'
                                            , 'Humidity(%)'
                                            , 'Pressure(in)'
                                            , 'Visibility(mi)'
                                            , 'Wind_Direction'
                                            , 'Wind_Speed(mph)'
                                            , 'Precipitation(in)'
                                            , 'Weather_Condition'
                                            , 'Amenity'
                                            , 'Bump'
                                            , 'Crossing'
                                            , 'Give_Way'
                                            , 'Junction'
                                            , 'No_Exit'
                                            , 'Railway'
                                            , 'Roundabout'
                                            , 'Station'
                                            , 'Stop'
                                            , 'Traffic_Calming'
                                            , 'Traffic_Signal'
                                            , 'Turning_Loop'
                                            , 'Sunrise_Sunset'
                                            , 'Civil_Twilight'
                                            , 'Nautical_Twilight'
                                            , 'Astronomical_Twilight'
                                            ]]

        outFile = inputCSVFile + '_cleaned_dataset.csv'
        cleaned_dataset.to_csv(outFile, index = False)