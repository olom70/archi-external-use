# Import of the function list in Archi.
# MVP : import and create, do not sync.
# How to control :
#  - create a Yed File for each Macro Process with the N2, N3 hierarchy
# Steps : 
# - Create à CSV in memory at the end dump ?
# Steps of the creation of the program :
# 1) begin with N1, N2,N3 and columns contateneted in the Documentation (full spreadsheet)
# 1b) add assertions
# 2) add others columns steps by step (on a spreadsheet where only one macro-process remains)
# 2b) add assertions for each steps
# 3) full import

import os
import sys
import logging
import argparse


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

import archi.importfunctionlist  as importfunctionlist

if __name__ == '__main__':

    logger = logging.getLogger('vc-import-function-list')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename='vc-import-function-list.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('Start. Application is initializing')

    my_parser = argparse.ArgumentParser(description='Create csv files to import into Archi')

    # Add the arguments
    my_parser.add_argument('file',
                        metavar='file',
                        type=str,
                        help='the excel file to import')
    my_parser.add_argument('path',
                        metavar='path',
                        type=str,
                        help='the path where resides the excel file')
    my_parser.add_argument('output',
                        metavar='output',
                        type=str,
                        help='the folder where to create the csv files')

    # Execute the parse_args() method
    args = my_parser.parse_args()

    # Initialize program variables after the parameters
    FUNCTIONLIST_NAME = args.file
    MAIN_FOLDER = args.path
    OUTPUT = args.output


assert importfunctionlist.importFL(MAIN_FOLDER=MAIN_FOLDER, OUTPUT=OUTPUT,
                                FUNCTIONLIST_NAME=FUNCTIONLIST_NAME)

