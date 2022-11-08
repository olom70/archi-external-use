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
import archi.importfunctionlist  as importfunctionlist


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

if __name__ == '__main__':

    logger = logging.getLogger('test-vc-import-function-list')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(filename='test-vc-import-function-list.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('Start. Application is initializing')


    
    MAIN_FOLDER = '/Users/CLAUDE/Documents/dev/archi-external-use'
    FUNCTIONLIST_NAME = 'Functions List.xlsx'
    OUTPUT_FOLDER = 'output'
    YEDFILEPREFIX = 'FunctionListYED'
    ARCHIPREFIX = 'impflcmo'
    TAB='Clean List'

    try:
            os.mkdir(MAIN_FOLDER)
    except FileExistsError as fe:
        pass
    except FileNotFoundError as fnf:
        logger.critical(f'wrong path, please fix MAIN_FOLDER : {MAIN_FOLDER}')
        print('wrong path, please fix MAIN_FOLDER') 
        exit()
    except Exception as e:
        logger.critical(f'unexpected error : {type(e)}{e.args}')
        print(f'unexpected error : {type(e)}{e.args}')
        exit()

    INPUT = MAIN_FOLDER + os.path.sep + FUNCTIONLIST_NAME
    if not os.path.isfile(INPUT):
        logger.critical(f'this file does not exists {input}. put it in the folder {MAIN_FOLDER}')
        print(f'this file does not exists {input}. put it in the folder {MAIN_FOLDER}')


importfunctionlist.importFL(MAIN_FOLDER=MAIN_FOLDER, OUTPUT=OUTPUT_FOLDER,
                                FUNCTIONLIST_NAME=FUNCTIONLIST_NAME, TAB=TAB, YEDFILEPREFIX=YEDFILEPREFIX, ARCHIPREFIX=ARCHIPREFIX)

