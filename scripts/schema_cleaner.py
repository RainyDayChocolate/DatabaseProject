#! /usr/bin/env python

from clean_us_accident_dataset import *

node_name = 'schema_cleaner'

if __name__=='__main__':
    print('{} is launched !!'.format(node_name))

    print('Clean the US Accident dataset...')

    USAccidentDatasetFile = '../us-accidents/US_Accidents_May19.csv'
    Clean_US_Accident_dataset(USAccidentDatasetFile)
