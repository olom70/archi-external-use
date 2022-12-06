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
def getcleanedID(rawname: str, level: int) -> str:
    cleaned = cfl.PREFIXTOID + stringutil.cleanName(
        rawname,
        True,
        True,
        'lowercase',
        True,
        True,
        True) \
        + '_Level' + str(level)[0:39]
    mlogger.debug(f"level {level}, raw : {rawname}, cleaned : {cleaned} ")
    return cleaned

@log_function_call
def getCleanedName(rawname: str, level: int) -> str:
    cleaned = stringutil.cleanName(
        rawname,
        False,
        False,
        'nochange',
        True,
        False,
        False)
    mlogger.debug(f"level {level}, raw : {rawname}, cleaned : {cleaned} ")
    return cleaned

@log_function_call
def getCleanedString(rawname: str) -> str:
    cleaned = stringutil.cleanName(
        rawname,
        False,
        False,
        'nochange',
        True,
        False,
        False)
    mlogger.debug(f"raw : {rawname}, cleaned : {cleaned} ")
    return cleaned

@log_function_call
def getCleanedApp(rawname: str) -> str:
    cleaned = stringutil.cleanName(
        rawname,
        True,
        True,
        'lowercase',
        True,
        False,
        True)
    mlogger.debug(f"raw : {rawname}, cleaned : {cleaned} ")
    return cleaned

@log_function_call
def getcleanedValue(rawname: str) -> str:
    cleaned = stringutil.cleanName(
        rawname,
        True,
        False,
        'uppercase',
        False,
        False,
        False)
    mlogger.debug(f"raw : {rawname}, cleaned : {cleaned} ")
    return cleaned



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

    def getS4analysis(value: str) -> str:
        match value:
            case 'Y' : return 'FullyManaged'
            case 'P' : return 'PartiallyManaged'
            case 'N' : return 'NotManaged'
            case _   : return ''

    def getApplications(apps: dict) -> str:
        to_return = []
        for key, value in apps.items():
            match key:
                case   'm': to_return.append('prod.com') if value == 'Y' else ''
                case   'n': to_return.append('link') if value == 'Y' else ''
                case   'o': to_return.append('SAP APO') if value == 'Y' else ''
                case   'p': to_return.append('SAP FMS') if value == 'Y' else ''
                case   'q': to_return.append('SAP ECC CORP 6.0') if value == 'Y' else ''
                case   'r': to_return.append('cape') if value == 'Y' else ''
                case   's': to_return.append('ORDER MAX') if value == 'Y' else ''
                case   't': to_return.append('rank2platform') if value == 'Y' else ''
                case   'u': to_return.append('AssessGo') if value == 'Y' else ''
                case   'v': to_return.append('CPP') if value == 'Y' else ''
                case   'w': to_return.append('PSV (Production stock Visibility)') if value == 'Y' else ''
                case   'x': to_return.append('SAP SNC') if value == 'Y' else ''
                case   'y': to_return.append('MOLD') if value == 'Y' else ''
                case   'z': to_return.append('AssessGo') if value == 'Y' else ''
                case   'aa':  to_return.append('PACE') if value == 'Y' else ''
                case   'ab':  to_return.append('S&OP Tactic') if value == 'Y' else ''
                case   'ac':  to_return.append('eTCO') if value == 'Y' else ''
            if value == 'Y': to_return.append(clix.LIST_SEPARATOR)
            
        
        str_toreturn = ''.join(map(str,to_return))
        return str_toreturn[0:len(str_toreturn)-1] if str_toreturn[len(str_toreturn)-1:len(str_toreturn)] == ';' else str_toreturn


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

        db = xl.readxl(fn=INPUT)
        colAcolId = db.ws(ws=cfl.TAB).col(col=1)  # A
        colBmacroprocess = db.ws(ws=cfl.TAB).col(col=2)  # B
        colCfunctionfuture = db.ws(ws=cfl.TAB).col(col=3)  # C
        colDkeyword = db.ws(ws=cfl.TAB).col(col=4)  # D
        colEmarketid = db.ws(ws=cfl.TAB).col(col=5)  # E
        colFsubfunctionlist = db.ws(ws=cfl.TAB).col(col=6)  # F
        colGfuturesubfunctiongeneraldescription = db.ws(ws=cfl.TAB).col(col=7)  # G
        colHuserstoryinformation = db.ws(ws=cfl.TAB).col(col=8)  # H
        colIopoldnpnew = db.ws(ws=cfl.TAB).col(col=9)  # I
        colJsubfunctfutureyntd = db.ws(ws=cfl.TAB).col(col=10)  # J
        colKsuitabilityofthesitoday = db.ws(ws=cfl.TAB).col(col=11)  # K
        colLcollabor = db.ws(ws=cfl.TAB).col(col=12)  # L
        colMprodcom = db.ws(ws=cfl.TAB).col(col=13)  # M
        colNlink = db.ws(ws=cfl.TAB).col(col=14)  # N
        colOapo = db.ws(ws=cfl.TAB).col(col=15)  # O
        colPfms = db.ws(ws=cfl.TAB).col(col=16)  # P
        colQecc = db.ws(ws=cfl.TAB).col(col=17)  # Q
        colRcape = db.ws(ws=cfl.TAB).col(col=18)  # R
        colSordermax = db.ws(ws=cfl.TAB).col(col=19)  # S
        colTrank2 = db.ws(ws=cfl.TAB).col(col=20)  # T
        colUassessgo = db.ws(ws=cfl.TAB).col(col=21)  # U
        colVcpp = db.ws(ws=cfl.TAB).col(col=22)  # V
        colWpsv = db.ws(ws=cfl.TAB).col(col=23)  # W
        colXsnc = db.ws(ws=cfl.TAB).col(col=24)  # X
        colYmoldgo = db.ws(ws=cfl.TAB).col(col=25)  # Y
        colZassetgo = db.ws(ws=cfl.TAB).col(col=26)  # Z
        colA_Apace = db.ws(ws=cfl.TAB).col(col=27)  # AA
        colA_Btacticalsop = db.ws(ws=cfl.TAB).col(col=28)  # AB
        colA_Cetco = db.ws(ws=cfl.TAB).col(col=29)  # AC
        colA_Dlinkwithtool = db.ws(ws=cfl.TAB).col(col=30)  # AD
        colA_Eothers = db.ws(ws=cfl.TAB).col(col=31)  # AE
        colA_Ffunctiongap = db.ws(ws=cfl.TAB).col(col=32)  # AF
        colA_Gpainsolved = db.ws(ws=cfl.TAB).col(col=33)  # AG
        colA_Htarget = db.ws(ws=cfl.TAB).col(col=34)  # AH
        colA_Iproductionreferencer = db.ws(ws=cfl.TAB).col(col=35)  # AI
        colA_Jordermanager = db.ws(ws=cfl.TAB).col(col=36)  # AJ
        colA_Kstockmanager = db.ws(ws=cfl.TAB).col(col=37)  # AK
        colA_Lcptquotationmanager = db.ws(ws=cfl.TAB).col(col=38)  # AL
        colA_Mcptplanner = db.ws(ws=cfl.TAB).col(col=39)  # AM
        colA_Nalertmanager = db.ws(ws=cfl.TAB).col(col=40)  # AN
        colA_Opreinvoicemanager = db.ws(ws=cfl.TAB).col(col=41)  # AO
        colA_Pmold = db.ws(ws=cfl.TAB).col(col=42)  # AP
        colA_Qapo = db.ws(ws=cfl.TAB).col(col=43)  # AQ
        colA_Rassesgo = db.ws(ws=cfl.TAB).col(col=44)  # AR
        colA_Sexpeditionpreparation = db.ws(ws=cfl.TAB).col(col=45)  # AS
        colA_Tbi = db.ws(ws=cfl.TAB).col(col=46)  # AT
        colA_Uauthorisationmanager = db.ws(ws=cfl.TAB).col(col=47)  # AU
        colA_Vadminparameters = db.ws(ws=cfl.TAB).col(col=48)  # AV
        colA_Wother = db.ws(ws=cfl.TAB).col(col=49)  # AW
        colA_Xctronlyonetargettool = db.ws(ws=cfl.TAB).col(col=50)  # AX
        colA_Ytoolproposal = db.ws(ws=cfl.TAB).col(col=51)  # AY
        colA_Ztoolproposal2 = db.ws(ws=cfl.TAB).col(col=52)  # AZ
        colB_Aifs4 = db.ws(ws=cfl.TAB).col(col=53)  # BA
        colB_Bifnots4where = db.ws(ws=cfl.TAB).col(col=54)  # BB
        colB_Cs4stdlevel = db.ws(ws=cfl.TAB).col(col=55)  # BC
        colB_Dweigh = db.ws(ws=cfl.TAB).col(col=56)  # BD
        colB_Ecostifdevinprod = db.ws(ws=cfl.TAB).col(col=57)  # BE
        colB_Fneededs4p2 = db.ws(ws=cfl.TAB).col(col=58)  # BF
        colB_Gcomment = db.ws(ws=cfl.TAB).col(col=59)  # BG
        colB_Hopenquestions = db.ws(ws=cfl.TAB).col(col=60)  # BH
        colB_Iforcastedyear = db.ws(ws=cfl.TAB).col(col=61)  # BI
        colB_Jtargetreached = db.ws(ws=cfl.TAB).col(col=63)  # BJ

        l_alreadyAdded = []
        l1_alreadyAdded = []

        for items in zip(colAcolId, colBmacroprocess, colCfunctionfuture, colDkeyword, colEmarketid, colFsubfunctionlist, colGfuturesubfunctiongeneraldescription, colHuserstoryinformation, colIopoldnpnew, colJsubfunctfutureyntd, colKsuitabilityofthesitoday, colLcollabor, colMprodcom, colNlink, colOapo, colPfms, colQecc, colRcape, colSordermax, colTrank2, colUassessgo, colVcpp, colWpsv, colXsnc, colYmoldgo, colZassetgo,
                        colA_Apace, colA_Btacticalsop, colA_Cetco, colA_Dlinkwithtool, colA_Eothers, colA_Ffunctiongap, colA_Gpainsolved, colA_Htarget, colA_Iproductionreferencer, colA_Jordermanager, colA_Kstockmanager, colA_Lcptquotationmanager, colA_Mcptplanner, colA_Nalertmanager, colA_Opreinvoicemanager, colA_Pmold, colA_Qapo, colA_Rassesgo, colA_Sexpeditionpreparation, colA_Tbi, colA_Uauthorisationmanager, colA_Vadminparameters, colA_Wother, colA_Xctronlyonetargettool, colA_Ytoolproposal, colA_Ztoolproposal2,
                        colB_Aifs4, colB_Bifnots4where, colB_Cs4stdlevel, colB_Dweigh, colB_Ecostifdevinprod, colB_Fneededs4p2, colB_Gcomment, colB_Hopenquestions, colB_Iforcastedyear, colB_Jtargetreached
                        ):
            a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, \
                aa, ab, ac, ad, ae, af, ag, ah, ai, aj, ak, al, am, an, ao, ap, aq, ar, as_, at, au, av, aw, ax, ay, az, \
                ba, bb, bc, bd, be, bf, bg, bh, bi, bj = [
                    items[col] for col in range(0, len(items))]

            processLine = True
            try:
                id = int(a)
            except ValueError:
                processLine = False

            if processLine:
                # IDgeneration ####################################################
                Level1ID = getcleanedID(b, 1)
                Level2ID = Level1ID + clix.HIERARCHY_SEPARATOR + getcleanedID(c, 2)
                idInName = '(' + str(a) + ') '
                Level3ID = Level1ID + clix.HIERARCHY_SEPARATOR +  Level2ID + clix.HIERARCHY_SEPARATOR + getcleanedID(idInName + f, 3)

                # Process Level1 ###############################################################
                if Level1ID not in l1_alreadyAdded:
                    l1_alreadyAdded.append(Level1ID)
                    name = getCleanedName(b, 1)
                    displayName = name
                    description = ''
                    relToParent = ''
                    S4Analysis = ''
                    relProcessToApplication = ''
                    toWrite = csvutil.initLeanIXProcess(type=clix.TYPE_PROCESS,
                            name=Level1ID,
                            displayName=displayName,
                            relToParent=relToParent,
                            S4Analysis=S4Analysis,
                            relProcessToApplication=relProcessToApplication,
                            description=description
                            )
                    #outputfiles[3].writerow(toWrite)


                # Level2 ###############################################################
                if Level2ID not in l_alreadyAdded:
                    l_alreadyAdded.append(Level2ID)
                    name = getCleanedName(c, 2).title()
                    displayName = getCleanedName(b, 1) + clix.HIERARCHY_SEPARATOR + name
                    description = ''
                    relToParent = getCleanedName(b, 1)
                    S4Analysis = ''
                    relProcessToApplication = ''
                    toWrite = csvutil.initLeanIXProcess(type=clix.TYPE_PROCESS,
                            name=name,
                            displayName=displayName,
                            relToParent=relToParent,
                            S4Analysis=S4Analysis,
                            relProcessToApplication=relProcessToApplication,
                            description=description
                            )
                    outputfiles[3].writerow(toWrite)

                # Level 3 ##############################################################
                name = idInName + getCleanedName(f, 3).title()
                displayName = getCleanedName(b, 1) + clix.HIERARCHY_SEPARATOR + getCleanedName(c, 2).title() + clix.HIERARCHY_SEPARATOR + name
                description = getCleanedString(g) \
                    + cfl.DOCSEPARATOR + getCleanedString(h) \
                    + cfl.DOCSEPARATOR + 'asis, link with these tools :' + getCleanedString(ad) + ' ' + getCleanedString(ae) \
                    + cfl.DOCSEPARATOR + 'tobe, if future not in S/4, where : ' + getCleanedString(bb) \
                    + cfl.DOCSEPARATOR + 'comment : ' + getCleanedString(bg) \
                    + cfl.DOCSEPARATOR + 'open questions : ' + getCleanedString(bh)
                relToParent = getCleanedName(b, 1).title() + clix.HIERARCHY_SEPARATOR + getCleanedName(c, 2).title()
                S4Analysis = getS4analysis(ba)
                relProcessToApplication = getApplications({'m': m,
                                                           'n': n,
                                                           'o': o,
                                                           'p': p,
                                                           'q': q,
                                                           'r': r,
                                                           's': s,
                                                           't': t,
                                                           'u': u,
                                                           'v': v,
                                                           'w': w,
                                                           'x': x,
                                                           'y': y,
                                                           'z': z,
                                                           'aa': aa,
                                                           'ab': ab,
                                                           'ac': ac}
                                                        )
                toWrite = csvutil.initLeanIXProcess(type=clix.TYPE_PROCESS,
                        name=name,
                        displayName=displayName,
                        relToParent=relToParent,
                        S4Analysis=S4Analysis,
                        relProcessToApplication=relProcessToApplication,
                        description=description
                        )
                outputfiles[3].writerow(toWrite)
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
                            description='description', relToParent='relToParent', 
                            relProcessToApplication='relProcessToApplication', S4Analysis='S4Analysis')
                            )
    outputfiles[3].writerow(
        csvutil.initLeanIXProcess(id='ID', type='Type', name='Name', displayName='Display Name',
                            description='Description', relToParent='Parents', 
                            relProcessToApplication='Applications', S4Analysis='S4Analysis')
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


    # Business Capabilities
    # INPUT = MAIN_FOLDER + os.path.sep + BUSINESS_CAPABILITIE_NAME
    # if not os.path.isfile(INPUT):
    #     mlogger.critical(
    #         f'this file does not exists {INPUT}. put it in the folder {MAIN_FOLDER}')
    #     return False
    # ok = importBC()
    # if not ok:
    #     mlogger.critical(f'ImportBC() returned False')
    #     outputfiles[0].close()
    #     outputfiles[2].close()
    #     outputfiles[4].close()
    #     return False

    #Function List
    ok = True
    INPUT = MAIN_FOLDER + os.path.sep + FUNCTIONLIST_NAME
    if not os.path.isfile(INPUT):
        mlogger.critical(
            f'this file does not exists {INPUT}. put it in the folder {MAIN_FOLDER}')
        return False
    if ok:
        ok = importFL()
        if not ok:
            mlogger.critical(f'ImportFL() returned False')
            outputfiles[0].close()
            outputfiles[2].close()
            outputfiles[4].close()
            return False
        if ok: return True
    