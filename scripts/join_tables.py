#! /usr/bin/env python

import argparse
import pandas as pd

node_name = 'join_tables'

if __name__=='__main__':
    parser = argparse.ArgumentParser( prog = node_name
                                    , description = 'This file joins the date and city attributes of two tables' )
    
    parser.add_argument( 'first_dataset'
                        , help = 'The first dataset. Suppose to be the US-accident dataset' )
    
    parser.add_argument( 'second_dataset'
                        , help = 'The second dataset. Suppose to be the US Flight Delay dataset' )
    
    args = parser.parse_args()

    firstDataset = args.first_dataset
    secondDataset = args.second_dataset

    print('I received...')
    print('The first dataset: {}\nThe second dataset: {}'.format(firstDataset, secondDataset) )

    print('Importing files...')
    firstData = pd.read_csv( firstDataset )
    secondData = pd.read_csv( secondDataset)
    print('The first dataset has dimension {}.\nThe second dataset has dimension {}.'.format(firstData.shape, secondData.shape) )
    print('Done.')

    print('Extract only the needed attributes...')
    firstData = firstData[[ 'Start_Time', 'City' ]]
    secondData = secondData[[ 'FL_DATE', 'ORIGIN_CITY_NAME' ]]

    finalConCatData = firstData
    finalConCatData.append( secondData )
    print('Done concatenating datasets.')

    print('The final dataset has dimension {}.'.format(finalConCatData.shape) )
    print('Just showing the first 20 tuples of the concatenated table')
    print( finalConCatData.head(20) )

    saveCSVFile = '../joined_table.csv'
    print('save data to {}'.format(saveCSVFile))
    finalConCatData.to_csv(saveCSVFile, index = False)


    
    