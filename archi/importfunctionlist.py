import pylightxl as xl
import archi.lib.csvutil as csvutil
import archi.lib.stringutil as stringutil
import os
import time
import pyyed
import logging
import archi.configfunctionlist as cfl
from archi.common import log_function_call
import uuid

mlogger = logging.getLogger('vc-import-function-list.importfunctionlist')

def openYed() -> pyyed.Graph:
    graph = pyyed.Graph()
    graph.define_custom_property("node", "UseCase", "string", "")
    return graph


@log_function_call
def importFL(MAIN_FOLDER: str, OUTPUT: str, FUNCTIONLIST_NAME: str) -> bool:

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
                                    False) \
        + ' (L' + str(level) + ')'
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
    def writeLine(toWrite: str, where: int) -> None:
        outputfiles[where].writerow(toWrite)
        mlogger.debug(f"line written into file {where} : {toWrite} ")

    @log_function_call
    def writelink(LevelID: str, columnToLink: str, valueOfTheCell: str ) -> None:
        found = True
        if valueOfTheCell == '':
            mlogger.debug(f'no value in the cell for {LevelID} in column {columnToLink}')
            return True
        try:
            match columnToLink.upper():
                case 'I':
                    source = cfl.COLI_OLDNEWPROCESSASSMENT[valueOfTheCell]
                    target = LevelID
                    linkType = cfl.ArchiConcepts.ASSOCIATIONRELATION.value
                case _:
                    found = False
                    mlogger.info(f"This column : '{columnToLink}' is not handled by the function writelink ")
        except KeyError:
            mlogger.info(f"Level : '{LevelID}' can not be link because this value : '{valueOfTheCell}' from column '{columnToLink}' doesn't exists in dictionary COLI_OLDNEWPROCESSASSESSMENT ")
            found = False
        if found:
            writeLine(csvutil.initRelations(ID=uuid.uuid4(), Type=linkType, Source=source, Target=target), 5)
            mlogger.debug(f'relation added. Type : {linkType}, source : {source}, target : {target}')
            return True
        else:
            return False

    #==========================================================================
    try:
        os.mkdir(MAIN_FOLDER)
        os.mkdir(MAIN_FOLDER + os.path.sep + OUTPUT)
    except FileExistsError as fe:
        pass
    except FileNotFoundError as fnf:
        mlogger.critical(f'wrong path, please fix MAIN_FOLDER : {MAIN_FOLDER} and/or OUTPUT {OUTPUT}')
        return False
    except Exception as e:
        mlogger.critical(f'unexpected error : {type(e)}{e.args}')
        return False

    INPUT = MAIN_FOLDER + os.path.sep + FUNCTIONLIST_NAME
    if not os.path.isfile(INPUT):
        mlogger.critical(f'this file does not exists {INPUT}. put it in the folder {MAIN_FOLDER}')
        return False

    OUTPUT_FOLDER = MAIN_FOLDER + os.path.sep + OUTPUT
    try:
        creationtime = str(time.time())
        csvelementsfile = OUTPUT_FOLDER + os.path.sep + cfl.ARCHIPREFIX + creationtime + '-elements.csv'
        csvpropertiesfile = OUTPUT_FOLDER + os.path.sep + cfl.ARCHIPREFIX + creationtime + '-properties.csv'
        csvrelationsfile = OUTPUT_FOLDER + os.path.sep + cfl.ARCHIPREFIX + creationtime + '-relations.csv'
        outputfiles = csvutil.createfiles([csvelementsfile, csvpropertiesfile, csvrelationsfile])
        outputfiles[1].writerow(csvutil.initElementsHeader())
        outputfiles[3].writerow(csvutil.initPropertiesHeader())
        outputfiles[5].writerow(csvutil.initRelationsHeader())
    except Exception as e:
        mlogger.critical(f'The initialisation of the csv files ({csvelementsfile},{csvpropertiesfile},{csvrelationsfile}) failed')
        return False

    mlogger.debug(f'about to read the file {INPUT}')
    everythingwascool = True
    db = xl.readxl(fn=INPUT)

    colAcolId=db.ws(ws=cfl.TAB).col(col=1) #A
    colBmacroprocess=db.ws(ws=cfl.TAB).col(col=2) #B
    colCfunctionfuture=db.ws(ws=cfl.TAB).col(col=3) #C
    colDkeyword=db.ws(ws=cfl.TAB).col(col=4) #D
    colEmarketid=db.ws(ws=cfl.TAB).col(col=5) #E
    colFsubfunctionlist=db.ws(ws=cfl.TAB).col(col=6) #F
    colGfuturesubfunctiongeneraldescription=db.ws(ws=cfl.TAB).col(col=7) #G
    colHuserstoryinformation=db.ws(ws=cfl.TAB).col(col=8) #H
    colIopoldnpnew=db.ws(ws=cfl.TAB).col(col=9) #I
    colJsubfunctfutureyntd=db.ws(ws=cfl.TAB).col(col=10) #J
    colKsuitabilityofthesitoday=db.ws(ws=cfl.TAB).col(col=11) #K
    colLcollabor=db.ws(ws=cfl.TAB).col(col=12) #L
    colMprodcom=db.ws(ws=cfl.TAB).col(col=13) #M
    colNlink=db.ws(ws=cfl.TAB).col(col=14) #N
    colOapo=db.ws(ws=cfl.TAB).col(col=15) #O
    colPfms=db.ws(ws=cfl.TAB).col(col=16) #P
    colQecc=db.ws(ws=cfl.TAB).col(col=17) #Q
    colRcape=db.ws(ws=cfl.TAB).col(col=18) #R
    colSordermax=db.ws(ws=cfl.TAB).col(col=19) #S
    colTrank2=db.ws(ws=cfl.TAB).col(col=20) #T
    colUassessgo=db.ws(ws=cfl.TAB).col(col=21) #U
    colVcpp=db.ws(ws=cfl.TAB).col(col=22) #V
    colWpsv=db.ws(ws=cfl.TAB).col(col=23) #W
    colXsnc=db.ws(ws=cfl.TAB).col(col=24) #X
    colYmoldgo=db.ws(ws=cfl.TAB).col(col=25) #Y
    colZassetgo=db.ws(ws=cfl.TAB).col(col=26) #Z
    colA_Apace=db.ws(ws=cfl.TAB).col(col=27) #AA
    colA_Btacticalsop=db.ws(ws=cfl.TAB).col(col=28) #AB
    colA_Cetco=db.ws(ws=cfl.TAB).col(col=29) #AC
    colA_Dlinkwithtool=db.ws(ws=cfl.TAB).col(col=30) #AD
    colA_Eothers=db.ws(ws=cfl.TAB).col(col=31) #AE
    colA_Ffunctiongap=db.ws(ws=cfl.TAB).col(col=32) #AF
    colA_Gpainsolved=db.ws(ws=cfl.TAB).col(col=33) #AG
    colA_Htarget=db.ws(ws=cfl.TAB).col(col=34) #AH
    colA_Iproductionreferencer=db.ws(ws=cfl.TAB).col(col=35) #AI
    colA_Jordermanager=db.ws(ws=cfl.TAB).col(col=36) #AJ
    colA_Kstockmanager=db.ws(ws=cfl.TAB).col(col=37) #AK
    colA_Lcptquotationmanager=db.ws(ws=cfl.TAB).col(col=38) #AL
    colA_Mcptplanner=db.ws(ws=cfl.TAB).col(col=39) #AM
    colA_Nalertmanager=db.ws(ws=cfl.TAB).col(col=40) #AN
    colA_Opreinvoicemanager=db.ws(ws=cfl.TAB).col(col=41) #AO
    colA_Pmold=db.ws(ws=cfl.TAB).col(col=42) #AP
    colA_Qapo=db.ws(ws=cfl.TAB).col(col=43) #AQ
    colA_Rassesgo=db.ws(ws=cfl.TAB).col(col=44) #AR
    colA_Sexpeditionpreparation=db.ws(ws=cfl.TAB).col(col=45) #AS
    colA_Tbi=db.ws(ws=cfl.TAB).col(col=46) #AT
    colA_Uauthorisationmanager=db.ws(ws=cfl.TAB).col(col=47) #AU
    colA_Vadminparameters=db.ws(ws=cfl.TAB).col(col=48) #AV
    colA_Wother=db.ws(ws=cfl.TAB).col(col=49) #AW
    colA_Xctronlyonetargettool=db.ws(ws=cfl.TAB).col(col=50) #AX
    colA_Ytoolproposal=db.ws(ws=cfl.TAB).col(col=51) #AY
    colA_Ztoolproposal2=db.ws(ws=cfl.TAB).col(col=52) #AZ
    colB_Aifs4=db.ws(ws=cfl.TAB).col(col=53) #BA
    colB_Bifnots4where=db.ws(ws=cfl.TAB).col(col=54) #BB
    colB_Cs4stdlevel=db.ws(ws=cfl.TAB).col(col=55) #BC
    colB_Dweigh=db.ws(ws=cfl.TAB).col(col=56) #BD
    colB_Ecostifdevinprod=db.ws(ws=cfl.TAB).col(col=57) #BE
    colB_Fneededs4p2=db.ws(ws=cfl.TAB).col(col=58) #BF
    colB_Gcomment=db.ws(ws=cfl.TAB).col(col=59) #BG
    colB_Hopenquestions=db.ws(ws=cfl.TAB).col(col=60) #BH
    colB_Iforcastedyear=db.ws(ws=cfl.TAB).col(col=61) #BI
    colB_Jtargetreached=db.ws(ws=cfl.TAB).col(col=63) #BJ

    l_alreadyAdded = []
    l1_alreadyAdded = []

    for items in zip(colAcolId, colBmacroprocess, colCfunctionfuture, colDkeyword, colEmarketid, colFsubfunctionlist, colGfuturesubfunctiongeneraldescription, colHuserstoryinformation, colIopoldnpnew, colJsubfunctfutureyntd, colKsuitabilityofthesitoday, colLcollabor, colMprodcom, colNlink, colOapo, colPfms, colQecc, colRcape, colSordermax, colTrank2, colUassessgo, colVcpp, colWpsv, colXsnc, colYmoldgo, colZassetgo,
                    colA_Apace, colA_Btacticalsop, colA_Cetco, colA_Dlinkwithtool, colA_Eothers, colA_Ffunctiongap, colA_Gpainsolved, colA_Htarget, colA_Iproductionreferencer, colA_Jordermanager, colA_Kstockmanager, colA_Lcptquotationmanager, colA_Mcptplanner, colA_Nalertmanager, colA_Opreinvoicemanager, colA_Pmold, colA_Qapo, colA_Rassesgo, colA_Sexpeditionpreparation, colA_Tbi, colA_Uauthorisationmanager, colA_Vadminparameters, colA_Wother, colA_Xctronlyonetargettool, colA_Ytoolproposal, colA_Ztoolproposal2,
                    colB_Aifs4, colB_Bifnots4where, colB_Cs4stdlevel, colB_Dweigh, colB_Ecostifdevinprod, colB_Fneededs4p2, colB_Gcomment, colB_Hopenquestions, colB_Iforcastedyear, colB_Jtargetreached
                    ):
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, \
        aa, ab, ac, ad, ae, af, ag, ah, ai, aj, ak, al, am, an, ao, ap, aq, ar, as_, at, au, av, aw, ax, ay, az, \
        ba, bb, bc, bd, be, bf, bg, bh, bi, bj = [items[col] for col in range(0, len(items))]
        
        processLine = True
        try:
            id = int(a)
        except ValueError:
            processLine = False

        if processLine:
            # IDgeneration ####################################################
            Level1ID = getcleanedID(b, 1)
            Level2ID = Level1ID + getcleanedID(c, 2)
            Level3ID = Level2ID + getcleanedID(f, 3)
            
            #Process Level1 ###############################################################
            if Level1ID not in l1_alreadyAdded:
                try:
                    graph.write_graph(OUTPUT_FOLDER + os.path.sep + l1_alreadyAdded[len(l1_alreadyAdded)-1]+cfl.YEDFILESUFFIX, pretty_print=True)
                except NameError:
                    pass
                graph = openYed()
                l1_alreadyAdded.append(Level1ID)

                Name = getCleanedName(b, 1)
                Documentation = ''
                writeLine(csvutil.initElements(ID=Level1ID, Type=cfl.ArchiConcepts.BUSINESSPROCESS.value, Name=Name, Documentation=Documentation), 1)
                writeLine(csvutil.initProperties(ID=Level1ID, Key=cfl.ArchiProperties.IMPORTEDFROMFUNCTIONLIST.value, Value=cfl.YES), 3)
                graph.add_node(Level1ID, label=Name, font_size=cfl.YedProperties.L1FONTSIZE.value, font_style=cfl.YedProperties.L1FONTSTYLE.value, width=cfl.YedProperties.WIDTH.value, shape_fill=cfl.YedProperties.L1COLOR.value)
            
            #Level2 ###############################################################
            if Level2ID not in l_alreadyAdded:
                l_alreadyAdded.append(Level2ID)
                Name = getCleanedName(c, 2)
                Documentation = getCleanedString(e)
                writeLine(csvutil.initElements(ID=Level2ID, Type=cfl.ArchiConcepts.BUSINESSFUNCTION.value, Name=Name, Documentation=Documentation), 1)
                writeLine(csvutil.initProperties(ID=Level2ID, Key=cfl.ArchiProperties.IMPORTEDFROMFUNCTIONLIST.value, Value=cfl.YES), 3)
                writeLine(csvutil.initProperties(ID=Level2ID, Key=cfl.ArchiProperties.KEYWORD.value, Value=d), 3)
                writeLine(csvutil.initProperties(ID=Level2ID, Key=cfl.ArchiProperties.LINKTON1.value, Value=Level1ID), 3)
                writeLine(csvutil.initRelations(ID=uuid.uuid4(), Type=cfl.ArchiConcepts.COMPOSITIONRELATION.value, Source=Level1ID, Target=Level2ID), 5)
                graph.add_node(Level2ID, label=Name, font_size=cfl.YedProperties.L2FONTSIZE.value, font_style=cfl.YedProperties.L2FONTSTYLE.value, width=cfl.YedProperties.WIDTH.value, shape_fill=cfl.YedProperties.L2COLOR.value)
                graph.add_edge(Level1ID, Level2ID)

            #Level 3 ##############################################################
            if Level3ID not in l_alreadyAdded:
                l_alreadyAdded.append(Level3ID)
                Name = getCleanedName(f, 3)
                Documentation = getCleanedString(g) + cfl.DOCSEPARATOR + getCleanedString(h)
            
                writeLine(csvutil.initElements(ID=Level3ID, Type=cfl.ArchiConcepts.BUSINESSFUNCTION.value, Name=Name, Documentation=Documentation), 1)
                writeLine(csvutil.initProperties(ID=Level3ID, Key=cfl.ArchiProperties.IMPORTEDFROMFUNCTIONLIST.value, Value=cfl.YES), 3)
                writeLine(csvutil.initProperties(ID=Level3ID, Key=cfl.ArchiProperties.LINKTON2.value, Value=Level2ID), 3)
                writeLine(csvutil.initRelations(ID=uuid.uuid4(), Type=cfl.ArchiConcepts.COMPOSITIONRELATION.value, Source=Level2ID, Target=Level3ID), 5)
                everythingwascool = False if not writelink(LevelID=Level3ID, columnToLink='I', valueOfTheCell=i) else everythingwascool

                graph.add_node(Level3ID, label=Name, font_size=cfl.YedProperties.L3FONTSIZE.value, font_style=cfl.YedProperties.L3FONTSTYLE.value, width=cfl.YedProperties.WIDTH.value, shape_fill=cfl.YedProperties.L3COLOR.value,
                            custom_properties={"UseCase": getCleanedString(h)})
                graph.add_edge(Level2ID, Level3ID)
    
    outputfiles[0].close()
    outputfiles[2].close()
    outputfiles[4].close()
    try:
        graph.write_graph(OUTPUT_FOLDER + os.path.sep + l1_alreadyAdded[len(l1_alreadyAdded)-1]+cfl.YEDFILESUFFIX, pretty_print=True)
    except NameError:
        pass

    return everythingwascool

