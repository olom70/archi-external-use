import pylightxl as xl
import archi.lib.csvutil as csvutil
import archi.lib.stringutil as stringutil
import os
import time
import pyyed
import logging
import archi.configfunctionlist as cfl
from archi.common import log_function_call
import archi.lib.configleanix as clix
import archi.lib.fileutil as fileutil

mlogger = logging.getLogger('test-import-LeanIX.leaniximport')

def createLeanIXFile(MAIN_FOLDER: str, OUTPUT: str, OUTPUT_FILE:str) -> list:
    try:
        os.mkdir(MAIN_FOLDER)
        os.mkdir(MAIN_FOLDER + os.path.sep + OUTPUT)
    except FileExistsError as fe:
        pass
    except FileNotFoundError as fnf:
        mlogger.critical(
            f'wrong path, please fix MAIN_FOLDER : {MAIN_FOLDER} and/or OUTPUT {OUTPUT}')
        return []
    except Exception as e:
        mlogger.critical(f'unexpected error : {type(e)}{e.args}')
        return []

    OUTPUT_FOLDER = MAIN_FOLDER + os.path.sep + OUTPUT
    try:
        creationtime = str(time.time())
        csvelementsfile = OUTPUT_FOLDER + os.path.sep + creationtime + OUTPUT_FILE+ '.csv'
        return csvutil.createfiles([csvelementsfile])
    except Exception as e:
        mlogger.critical(
            f'The initialisation of the csv files ({csvelementsfile}) failed')
        return []


@log_function_call
def importALL(MAIN_FOLDER: str, OUTPUT: str, FUNCTIONLIST_NAME: str,
                BUSINESS_CAPABILITIE_NAME: str,
                OUTPUT_FILE_PREFIX: str,
                ALL_IN_ONE_FILE : bool
            ) -> bool:

    @log_function_call
    def importBC() -> bool:
        '''
        prepare the business capabilities map to an import in Lean IX
        '''

        try:

            toWrite = csvutil.initLeanIX(type=clix.TYPE_CAPABILITY, name=clix.ROOT) #it's the default Business Capability
            outputfiles[1].writerow(toWrite)

            db = xl.readxl(fn=INPUT)
            colA = db.ws(ws='bcmap').col(col=1)
            colB = db.ws(ws='bcmap').col(col=2)
            colC = db.ws(ws='bcmap').col(col=3)
            colD = db.ws(ws='bcmap').col(col=4)
            colE = db.ws(ws='bcmap').col(col=5)
            colF = db.ws(ws='bcmap').col(col=6)
            colG = db.ws(ws='bcmap').col(col=7)
            colH = db.ws(ws='bcmap').col(col=8)
            colI = db.ws(ws='bcmap').col(col=9)
            colJ = db.ws(ws='bcmap').col(col=10)
            colK = db.ws(ws='bcmap').col(col=11)

            l_alreadyAdded = []
            for items in zip(colA, colB, colC, colD, colE, colF, colG, colH, colI, colJ, colK):
        
                colAImport, colBL1ID, colCL2ID, colDLinkToFL, colEL3ID, colFL4ID, \
                    colGFRdesc, colHENdesc, colIDescriptions, colJITSolutions, \
                    colKITSolutions = [
                    items[col] for col in range(0, len(items))]

                if colAImport != 'y':
                    pass
                else:
                    Level1ID = colBL1ID
                    Level2ID = colCL2ID
                    Level3ID = colEL3ID
                    Level4ID = colFL4ID

                    description = stringutil.cleanName(
                                                    colGFRdesc,
                                                    False,
                                                    False,
                                                    'nochange',
                                                    True,
                                                    False,
                                                    False) \
                                    + clix.DESCRIPTION_SEPARATOR \
                                    + stringutil.cleanName(
                                                    colHENdesc,
                                                    False,
                                                    False,
                                                    'nochange',
                                                    True,
                                                    False,
                                                    False) \
                                    + clix.DESCRIPTION_SEPARATOR \
                                    + stringutil.cleanName(
                                                    colIDescriptions,
                                                    False,
                                                    False,
                                                    'nochange',
                                                    True,
                                                    False,
                                                    False)

                    ############################
                    # LEVEL 1 ##################
                    ############################
                    if Level1ID not in l_alreadyAdded:
                        l_alreadyAdded.append(Level1ID)
                        toWrite = csvutil.initLeanIX(type=clix.TYPE_CAPABILITY,
                                                        name=Level1ID,
                                                        displayName=colBL1ID,
                                                        relToParent=clix.ROOT
                                                    )
                        outputfiles[1].writerow(toWrite)
                    ############################
                    # LEVEL 2 ##################
                    ############################
                    if Level2ID not in l_alreadyAdded:
                        l_alreadyAdded.append(Level2ID)
                        if len(colEL3ID) < 4:
                            relToParent=clix.ROOT + clix.HIERARCHY_SEPARATOR + Level1ID
                            toWrite = csvutil.initLeanIX(type=clix.TYPE_CAPABILITY,
                                                        name=Level2ID,
                                                        displayName=colCL2ID,
                                                        relToParent=relToParent,
                                                        description=description
                                                    )
                            outputfiles[1].writerow(toWrite)
                    ############################
                    # LEVEL 3 ##################
                    ############################
                    if Level3ID not in l_alreadyAdded:
                        l_alreadyAdded.append(Level3ID)
                        if len(colFL4ID) < 4:
                            relToParent=clix.ROOT \
                                + clix.HIERARCHY_SEPARATOR \
                                + Level1ID \
                                + clix.HIERARCHY_SEPARATOR \
                                + Level2ID
                            toWrite = csvutil.initLeanIX(type=clix.TYPE_CAPABILITY,
                                                        name=Level3ID,
                                                        displayName=colEL3ID,
                                                        relToParent=relToParent,
                                                        description=description
                                                    )
                            outputfiles[1].writerow(toWrite)
                    ############################
                    # LEVEL 4 ##################
                    ############################
                    if Level4ID not in l_alreadyAdded:
                        l_alreadyAdded.append(Level3ID)
                        if len(colFL4ID) > 4:
                            relToParent=clix.ROOT + clix.HIERARCHY_SEPARATOR + Level1ID + clix.HIERARCHY_SEPARATOR + Level2ID + clix.HIERARCHY_SEPARATOR + Level3ID
                            toWrite = csvutil.initLeanIX(type=clix.TYPE_CAPABILITY,
                                                        name=Level4ID,
                                                        displayName=colFL4ID,
                                                        relToParent=relToParent,
                                                        description=description
                                                    )
                            outputfiles[1].writerow(toWrite)

            return True
        except Exception as e:
            mlogger.critical(f'Unexpected error in function prepareCapabilitiesTreemap() : {type(e)}{e.args}')
            return False



    @log_function_call
    def importFL() -> bool:
        
        return True


    #==================================================================================
    #Start of function
    #==================================================================================
    if not ALL_IN_ONE_FILE:
        outputfiles = createLeanIXFile(MAIN_FOLDER=MAIN_FOLDER, OUTPUT=OUTPUT, OUTPUT_FILE=OUTPUT_FILE_PREFIX+clix.BC_SUFFIX)
    else:
        outputfiles = createLeanIXFile(MAIN_FOLDER=MAIN_FOLDER, OUTPUT=OUTPUT, OUTPUT_FILE=OUTPUT_FILE_PREFIX)
    try:
        outputfiles[1].writerow(csvutil.initLeanIXHeader())
    except Exception as e:
        mlogger.critical(f'Unexpected error in function importALL() : {type(e)}{e.args}')

    INPUT = MAIN_FOLDER + os.path.sep + BUSINESS_CAPABILITIE_NAME
    if not os.path.isfile(INPUT):
        mlogger.critical(
            f'this file does not exists {INPUT}. put it in the folder {MAIN_FOLDER}')
        return False

    ok = importBC()
    if not ok:
        outputfiles[0].close()    
        return False

    if not ALL_IN_ONE_FILE:
        outputfiles[0].close()
        outputfiles = createLeanIXFile(MAIN_FOLDER=MAIN_FOLDER, OUTPUT=OUTPUT, OUTPUT_FILE=OUTPUT_FILE_PREFIX+clix.FL_SUFFIX)
        try:
            outputfiles[1].writerow(csvutil.initLeanIXHeader())
        except Exception as e:
            mlogger.critical(f'Unexpected error in function importALL() : {type(e)}{e.args}')

    INPUT = MAIN_FOLDER + os.path.sep + FUNCTIONLIST_NAME
    if not os.path.isfile(INPUT):
        mlogger.critical(
            f'this file does not exists {INPUT}. put it in the folder {MAIN_FOLDER}')
        return False
    ok = importFL()
    if not ok:
        outputfiles[0].close()
        return False

    outputfiles[0].close()
    return True

