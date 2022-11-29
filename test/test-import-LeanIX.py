import os
import sys
import logging
import argparse

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

import archi.leaniximport as leaniximport

if __name__ == '__main__':

    logger = logging.getLogger('test-import-LeanIX')
    logger.setLevel(logging.WARNING)
    fh = logging.FileHandler(filename='test-import-LeanIX.log')
    fh.setLevel(logging.WARNING)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('Start. Application is initializing')


    my_parser = argparse.ArgumentParser(description='Create csv files to import into Archi')

    # Add the arguments
    my_parser.add_argument('bcfile',
                        metavar='bcfile',
                        type=str,
                        help='the business capabilities excel file to import')
    my_parser.add_argument('flfile',
                        metavar='flfile',
                        type=str,
                        help='the function list excel file to import')
    my_parser.add_argument('path',
                        metavar='path',
                        type=str,
                        help='the path where resides the excel file')
    my_parser.add_argument('output',
                        metavar='output',
                        type=str,
                        help='the folder where to create the csv files')
    my_parser.add_argument('outputfileprefix',
                        metavar='outputfileprefix',
                        type=str,
                        help='the prefix of the file to create in the outputfolder')
    my_parser.add_argument('allinonefile',
                        metavar='allinonefile',
                        type=str,
                        help='true to generate one output file only, false to create a file for each input file')

    # Execute the parse_args() method
    args = my_parser.parse_args()

    # Initialize program variables after the parameters
    FUNCTIONLIST_NAME = args.flfile
    BUSINESS_CAPABILITIE_NAME = args.bcfile
    MAIN_FOLDER = args.path
    OUTPUT = args.output
    OUTPUT_FILE_PREFIX = args.outputfileprefix
    ALL_IN_ONE_FILE = True if args.allinonefile == 'True' else False

    assert leaniximport.importALL(MAIN_FOLDER=MAIN_FOLDER, OUTPUT=OUTPUT,
                                FUNCTIONLIST_NAME=FUNCTIONLIST_NAME,
                                BUSINESS_CAPABILITIE_NAME=BUSINESS_CAPABILITIE_NAME,
                                OUTPUT_FILE_PREFIX=OUTPUT_FILE_PREFIX,
                                ALL_IN_ONE_FILE=ALL_IN_ONE_FILE)

    fh.close()