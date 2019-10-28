#! /usr/bin/env python

import pandas as pd
import argparse

'''
This file is used to get only the first N rows from a far bigger dataset.
The output file is a much reduced dataset to ease the testing of the main software.
'''
node_name = 'dataset_partitioner'
if __name__ == '__main__':
    parser = argparse.ArgumentParser( prog = node_name
                                    , description = 'This file is used to get only the first N rows from a far bigger dataset' )
    
    parser.add_argument( 'input_file'
                       , help = 'The input CSV file')
    
    parser.add_argument('first_number_of_tuples'
                        , help = 'The first number of rows to kept in the output file')

    args = parser.parse_args()

    inputFileName = args.input_file
    outputFileName = inputFileName + '_trimmed.csv'
    numberOfSavedRows = args.first_number_of_tuples

    print('Input file: {}'.format(inputFileName))
    print('The first {} rows are saved to {}'.format(numberOfSavedRows, outputFileName))


    inputData = pd.read_csv( inputFileName, nrows = int(numberOfSavedRows) )

    print( inputData.to_csv( outputFileName ) )

    print('Done! You\'re all set!')
