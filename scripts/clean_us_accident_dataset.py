#! /usr/bin/env python

import pandas as pd
import datetime as dt

class Clean_US_Accident_dataset:
    def __init__(self, inputCSVFile):
        date_attribute = ['Start_Time']
        imported_dataset = pd.read_csv( inputCSVFile, parse_dates = date_attribute )
        print('The reeived raw dataset has dimension {}'.format(imported_dataset.size))

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

        # Keep only tuples with dates falling in 2016
        print('Keep those tuples which fell into the year 2016...')
        cleaned_dataset = cleaned_dataset[ cleaned_dataset['Start_Time'].dt.year == int(2016) ]
        print('Done.')

        # Just for showing
        print('Showing the first 5 rows of the entire dataset...')
        print( cleaned_dataset.head() )

        outFile = inputCSVFile + '_cleaned_dataset.csv'

        print('The trimmed dataset has dimension {} and saved to \n{}'.format(cleaned_dataset.size, outFile) )
        cleaned_dataset.to_csv(outFile, index = False)