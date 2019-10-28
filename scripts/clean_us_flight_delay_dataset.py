#! /usr/bin/env python

import pandas as pd

class Clean_US_flight_delay_dataset:
    def __init__(self, inputCSVFile):
        imported_dataset = pd.read_csv( inputCSVFile )

        print('Received a dataset of dimension: {}'.format(imported_dataset.shape ) )

        # Display the attributes
        # print( list(imported_dataset) )

        cleaned_dataset = imported_dataset[['FL_DATE'
                                          , 'UNIQUE_CARRIER'
                                          , 'FL_NUM'
                                          , 'ORIGIN_AIRPORT_ID'
                                          , 'ORIGIN_CITY_NAME'
                                          , 'ORIGIN_STATE_NM'
                                          , 'DEST_AIRPORT_ID'
                                          , 'DEST_CITY_NAME'
                                          , 'DEST_STATE_NM'
                                          , 'DEP_TIME'
                                          , 'DEP_DELAY'
                                          , 'ARR_TIME'
                                          , 'ARR_DELAY'
                                          , 'CRS_ELAPSED_TIME'
                                          , 'ACTUAL_ELAPSED_TIME'
                                          , 'CARRIER_DELAY'
                                          , 'WEATHER_DELAY'
                                          , 'NAS_DELAY'
                                          , 'SECURITY_DELAY'
                                          , 'LATE_AIRCRAFT_DELAY'
                                          , 'FIRST_DEP_TIME'
                                          ]]
        
        outFile = inputCSVFile + '_cleaned_dataset.csv'
        print('The trimmed dataset has dimension {} and saved to \n{}'.format(cleaned_dataset.shape, outFile) )
        cleaned_dataset.to_csv(outFile, index = False)