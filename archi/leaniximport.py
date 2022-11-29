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

@log_function_call
def importALL(MAIN_FOLDER: str, OUTPUT: str, FUNCTIONLIST_NAME: str,
                BUSINESS_CAPABILITIE_NAME: str
            ) -> bool:


    def getProcessCell(colDLinkToFL: str) -> str:
        if len(colDLinkToFL) > 4:
            relBusinessCapabilityToProcess =  colDLinkToFL.replace(clix.SPLITON, clix.LIST_SEPARATOR)
            relBusinessCapabilityToProcess = stringutil.cleanName(
                                                    relBusinessCapabilityToProcess,
                                                    False,
                                                    False,
                                                    'noChange',
                                                    True,
                                                    False,
                                                    False)
        else:
            relBusinessCapabilityToProcess = ''
        return relBusinessCapabilityToProcess

    def getAppCell(colJITSolutions: str) -> str:
        if len(colJITSolutions) > 2:
            relBusinessCapabilityToApplication =  colJITSolutions.replace(clix.SPLITON, clix.LIST_SEPARATOR)
            relBusinessCapabilityToApplication = stringutil.cleanName(
                                                    relBusinessCapabilityToApplication,
                                                    True,
                                                    True,
                                                    'lowercase',
                                                    True,
                                                    False,
                                                    False)
        else:
            relBusinessCapabilityToApplication = ''
        return relBusinessCapabilityToApplication


    @log_function_call
    def importBC() -> bool:
        '''
        prepare the business capabilities map to an import in Lean IX
        '''

        try:

            # toWrite = csvutil.initLeanIXCapabilities(type=clix.TYPE_CAPABILITY, name=clix.ROOT) #it's the default Business Capability
            # outputfiles[1].writerow(toWrite)

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
                        toWrite = csvutil.initLeanIXCapabilities(type=clix.TYPE_CAPABILITY,
                                                        name=Level1ID,
                                                        displayName=Level1ID,
                                                        relToParent=''
                                                    )
                        outputfiles[1].writerow(toWrite)
                    ############################
                    # LEVEL 2 ##################
                    ############################
                    if Level2ID not in l_alreadyAdded:
                        l_alreadyAdded.append(Level2ID)
                        displayName=Level1ID + clix.HIERARCHY_SEPARATOR + Level2ID
                        relToParent=Level1ID
                        relBusinessCapabilityToProcess =  getProcessCell(colDLinkToFL)
                        relBusinessCapabilityToApplication =  getAppCell(colJITSolutions)
                        toWrite = csvutil.initLeanIXCapabilities(type=clix.TYPE_CAPABILITY,
                                                    name=Level2ID,
                                                    displayName=displayName,
                                                    description=description,
                                                    relBusinessCapabilityToProcess=relBusinessCapabilityToProcess,
                                                    relBusinessCapabilityToApplication=relBusinessCapabilityToApplication,
                                                    relToParent=relToParent
                                                )
                        outputfiles[1].writerow(toWrite)
                    ############################
                    # LEVEL 3 ##################
                    ############################
                    if Level3ID not in l_alreadyAdded:
                        l_alreadyAdded.append(Level3ID)
                        if len(colEL3ID) > 4:
                            displayName=Level1ID \
                                + clix.HIERARCHY_SEPARATOR \
                                + Level2ID \
                                + clix.HIERARCHY_SEPARATOR \
                                + Level3ID
                            relToParent=Level1ID \
                                + clix.HIERARCHY_SEPARATOR \
                                + Level2ID
                            relBusinessCapabilityToProcess =  getProcessCell(colDLinkToFL)
                            relBusinessCapabilityToApplication =  getAppCell(colJITSolutions)

                            toWrite = csvutil.initLeanIXCapabilities(type=clix.TYPE_CAPABILITY,
                                                        name=Level3ID,
                                                        displayName=displayName,
                                                        description=description,
                                                        relBusinessCapabilityToProcess=relBusinessCapabilityToProcess,
                                                        relBusinessCapabilityToApplication=relBusinessCapabilityToApplication,
                                                        relToParent=relToParent
                                                    )
                            outputfiles[1].writerow(toWrite)
                    ############################
                    # LEVEL 4 ##################
                    ############################
                    if Level4ID not in l_alreadyAdded:
                        l_alreadyAdded.append(Level4ID)
                        if len(colFL4ID) > 4:
                            displayName=Level1ID \
                                + clix.HIERARCHY_SEPARATOR \
                                + Level2ID \
                                + clix.HIERARCHY_SEPARATOR \
                                + Level3ID \
                                + clix.HIERARCHY_SEPARATOR \
                                + Level4ID
                            relToParent=Level1ID \
                                + clix.HIERARCHY_SEPARATOR \
                                + Level2ID \
                                + clix.HIERARCHY_SEPARATOR \
                                + Level3ID
                            relBusinessCapabilityToProcess =  getProcessCell(colDLinkToFL)
                            relBusinessCapabilityToApplication =  getAppCell(colJITSolutions)

                            toWrite = csvutil.initLeanIXCapabilities(type=clix.TYPE_CAPABILITY,
                                                        name=Level4ID,
                                                        displayName=displayName,
                                                        description=description,
                                                        relBusinessCapabilityToProcess=relBusinessCapabilityToProcess,
                                                        relBusinessCapabilityToApplication=relBusinessCapabilityToApplication,
                                                        relToParent=relToParent
                                                    )
                            outputfiles[1].writerow(toWrite)
                    ############################
                    # PROCESS ##################
                    ############################
                    if len(colDLinkToFL) > 4:
                        for process in colDLinkToFL.split(clix.SPLITON):
                            process = stringutil.cleanName(
                                                    process,
                                                    False,
                                                    False,
                                                    'noChange',
                                                    True,
                                                    False,
                                                    False)
                            if process not in l_alreadyAdded:
                                l_alreadyAdded.append(process)
                                outputfiles[3].writerow(
                                csvutil.initLeanIXProcess(type=clix.TYPE_PROCESS, name=process)
                                )
                    ############################
                    # APPLICATIONS ##################
                    ############################
                    if len(colJITSolutions) > 2:
                        for app in colJITSolutions.split(clix.SPLITON):
                            app = stringutil.cleanName(
                                                    app,
                                                    True,
                                                    True,
                                                    'lowercase',
                                                    True,
                                                    False,
                                                    False)
                            if app not in l_alreadyAdded:
                                l_alreadyAdded.append(app)
                                outputfiles[5].writerow(
                                csvutil.initLeanIXProcess(type=clix.TYPE_APPLICATION, name=app)
                                )
                    

            return True
        except Exception as e:
            mlogger.critical(f'Unexpected error in function importAll() : {type(e)}{e.args}')
            return False



    @log_function_call
    def importFL() -> bool:
        
        return True


    #==================================================================================
    #Start of function
    #==================================================================================
    
    try:
        os.mkdir(MAIN_FOLDER)
        os.mkdir(MAIN_FOLDER + os.path.sep + OUTPUT)
    except FileExistsError as fe:
        pass
    except FileNotFoundError as fnf:
        mlogger.critical(
            f'wrong path, please fix MAIN_FOLDER : {MAIN_FOLDER} and/or OUTPUT {OUTPUT}')
        return False
    except Exception as e:
        mlogger.critical(f'unexpected error : {type(e)}{e.args}')
        return False

    OUTPUT_FOLDER = MAIN_FOLDER + os.path.sep + OUTPUT
    try:
        creationtime = str(time.time())
        csvBusinessCapability = OUTPUT_FOLDER + os.path.sep + clix.PREFIX + creationtime + clix.BC_SUFFIX + '.csv'
        csvProcess = OUTPUT_FOLDER + os.path.sep + clix.PREFIX + creationtime + clix.PR_SUFFIX + '.csv'
        csvAPP = OUTPUT_FOLDER + os.path.sep + clix.PREFIX + creationtime + clix.AP_SUFFIX + '.csv'
        outputfiles = csvutil.createfiles([csvBusinessCapability, csvProcess, csvAPP])
    except Exception as e:
        mlogger.critical(
            f'The initialisation of the csv files ({csvBusinessCapability}, {csvProcess}, {csvAPP}) failed')
        return False

    # Init first 2 lines of the Business Capabilities
    outputfiles[1].writerow(
        csvutil.initLeanIXCapabilities(id='id', type='type', name='name', displayName='displayName',
                            description='description', relToParent='relToParent', 
                            relBusinessCapabilityToProcess='relBusinessCapabilityToProcess',
                            relBusinessCapabilityToApplication='relBusinessCapabilityToApplication')
                            )
    outputfiles[1].writerow(
        csvutil.initLeanIXCapabilities(id='ID', type='Type', name='Name', displayName='Display Name',
                            description='Description', relToParent='Parents', 
                            relBusinessCapabilityToProcess='Processes',
                            relBusinessCapabilityToApplication='Applications')
                            )
    # Init first 2 lines of the Processes
    outputfiles[3].writerow(
        csvutil.initLeanIXProcess(id='id', type='type', name='name', displayName='displayName',
                            description='description',
                            relProcessToApplication='relProcessToApplication')
                            )
    outputfiles[3].writerow(
        csvutil.initLeanIXProcess(id='ID', type='Type', name='Name', displayName='Display Name',
                            description='Description',
                            relProcessToApplication='Applications')
                            )
    # Init first 2 lines of the Applications
    outputfiles[5].writerow(
        csvutil.initLeanIXApplication(id='id', type='type', name='name', displayName='displayName',
                            description='description', functionalSuitability='functionalSuitability', 
                            relApplicationToProcess='relApplicationToProcess')
                            )
    outputfiles[5].writerow(
        csvutil.initLeanIXApplication(id='ID', type='Type', name='Name', displayName='Display Name',
                            description='Description', functionalSuitability='Functional Fit', 
                            relApplicationToProcess='Processes')
                            )

    INPUT = MAIN_FOLDER + os.path.sep + BUSINESS_CAPABILITIE_NAME
    if not os.path.isfile(INPUT):
        mlogger.critical(
            f'this file does not exists {INPUT}. put it in the folder {MAIN_FOLDER}')
        return False

    ok = importBC()
    if not ok:
        mlogger.critical(f'ImportBC() returned False')
        outputfiles[0].close()
        outputfiles[2].close()
        outputfiles[4].close()
        return False
    
    if ok: return True
    