#! /usr/bin/env python

from clean_us_accident_dataset import *

node_name = 'schema_cleaner'

if __name__=='__main__':
    print('{} is launched !!'.format(node_name))

    print('Clean the US Accident dataset...')

    # The test dataset
    # USAccidentDatasetFile = '/home/charly_huang/Documents/RPI_ITWS_coursework/ITWS 6960 Database Systems/Final Project/DatabaseProject/us-accidents/US_Accidents_May19.csv_trimmed.csv'

    # The real dataset
    USAccidentDatasetFile = '../us-accidents/US_Accidents_May19.csv'
    Clean_US_Accident_dataset(USAccidentDatasetFile)
