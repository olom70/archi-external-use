import pylightxl as xl
import lib.csvutil as csvutil
import lib.stringutil as stringutil
import os
import time
import pyyed
import archi.configfunctionlist as configfunctionlist

def importFL(MAIN_FOLDER: str, OUTPUT: str, FUNCTIONLIST_NAME: str, TAB: str, YEDFILEPREFIX: str, ARCHIPREFIX: str) -> None: 


    INPUT = MAIN_FOLDER + os.path.sep + FUNCTIONLIST_NAME
    ELEMENTTYPE = 'Grouping'
    RELATIONTYPE = 'CompositionRelationship'
    KEY = 'import'
    VALUE = 'VIP'
    L1FONTSTYLE = "bold"
    L1FONTSIZE = "14"
    L2FONTSTYLE = "plain"
    L2FONTSIZE = "13"
    L3FONTSTYLE = "plain"
    L3FONTSIZE = "12"
    WIDTH='200'
    L1COLOR="#DE1FF2"
    L2COLOR="#07F2B8"
    L3COLOR="#F2BE1F"

    if not os.path.isfile(INPUT):
        print(f'this file does not exists {input}. put it in the folder {MAIN_FOLDER}')

    db = xl.readxl(fn=INPUT)

    creationtime = str(time.time())
    csvelementsfile = MAIN_FOLDER + os.path.sep + ARCHIPREFIX + creationtime + '-elements.csv'
    csvpropertiesfile = MAIN_FOLDER + os.path.sep + ARCHIPREFIX + creationtime + '-properties.csv'
    csvrelationsfile = MAIN_FOLDER + os.path.sep + ARCHIPREFIX + creationtime + '-relations.csv'
    outputfiles = csvutil.createfiles([csvelementsfile, csvpropertiesfile, csvrelationsfile])
    outputfiles[1].writerow(csvutil.initElementsHeader())
    outputfiles[3].writerow(csvutil.initPropertiesHeader())
    outputfiles[5].writerow(csvutil.initRelationsHeader())

    colAcolId=db.ws(ws=TAB).col(col=1) #A
    colBmacroprocess=db.ws(ws=TAB).col(col=2) #B
    colCfunctionfuture=db.ws(ws=TAB).col(col=3) #C
    colDkeyword=db.ws(ws=TAB).col(col=4) #D
    colEmarketid=db.ws(ws=TAB).col(col=5) #E
    colFsubfunctionlist=db.ws(ws=TAB).col(col=6) #F
    colGfuturesubfunctiongeneraldescription=db.ws(ws=TAB).col(col=7) #G
    colHuserstoryinformation=db.ws(ws=TAB).col(col=8) #H
    colIopoldnpnew=db.ws(ws=TAB).col(col=9) #I
    colJsubfunctfutureyntd=db.ws(ws=TAB).col(col=10) #J
    colKsuitabilityofthesitoday=db.ws(ws=TAB).col(col=11) #K
    colLcollabor=db.ws(ws=TAB).col(col=12) #L
    colMprodcom=db.ws(ws=TAB).col(col=13) #M
    colNlink=db.ws(ws=TAB).col(col=14) #N
    colOapo=db.ws(ws=TAB).col(col=15) #O
    colPfms=db.ws(ws=TAB).col(col=16) #P
    colQecc=db.ws(ws=TAB).col(col=17) #Q
    colRcape=db.ws(ws=TAB).col(col=18) #R
    colSordermax=db.ws(ws=TAB).col(col=19) #S
    colTrank2=db.ws(ws=TAB).col(col=20) #T
    colUassessgo=db.ws(ws=TAB).col(col=21) #U
    colVcpp=db.ws(ws=TAB).col(col=22) #V
    colWpsv=db.ws(ws=TAB).col(col=23) #W
    colXsnc=db.ws(ws=TAB).col(col=24) #X
    colYmoldgo=db.ws(ws=TAB).col(col=25) #Y
    colZassetgo=db.ws(ws=TAB).col(col=26) #Z
    colA_Apace=db.ws(ws=TAB).col(col=27) #AA
    colA_Btacticalsop=db.ws(ws=TAB).col(col=28) #AB
    colA_Cetco=db.ws(ws=TAB).col(col=29) #AC
    colA_Dlinkwithtool=db.ws(ws=TAB).col(col=30) #AD
    colA_Eothers=db.ws(ws=TAB).col(col=31) #AE
    colA_Ffunctiongap=db.ws(ws=TAB).col(col=32) #AF
    colA_Gpainsolved=db.ws(ws=TAB).col(col=33) #AG
    colA_Htarget=db.ws(ws=TAB).col(col=34) #AH
    colA_Iproductionreferencer=db.ws(ws=TAB).col(col=35) #AI
    colA_Jordermanager=db.ws(ws=TAB).col(col=36) #AJ
    colA_Kstockmanager=db.ws(ws=TAB).col(col=37) #AK
    colA_Lcptquotationmanager=db.ws(ws=TAB).col(col=38) #AL
    colA_Mcptplanner=db.ws(ws=TAB).col(col=39) #AM
    colA_Nalertmanager=db.ws(ws=TAB).col(col=40) #AN
    colA_Opreinvoicemanager=db.ws(ws=TAB).col(col=41) #AO
    colA_Pmold=db.ws(ws=TAB).col(col=42) #AP
    colA_Qapo=db.ws(ws=TAB).col(col=43) #AQ
    colA_Rassesgo=db.ws(ws=TAB).col(col=44) #AR
    colA_Sexpeditionpreparation=db.ws(ws=TAB).col(col=45) #AS
    colA_Tbi=db.ws(ws=TAB).col(col=46) #AT
    colA_Uauthorisationmanager=db.ws(ws=TAB).col(col=47) #AU
    colA_Vadminparameters=db.ws(ws=TAB).col(col=48) #AV
    colA_Wother=db.ws(ws=TAB).col(col=49) #AW
    colA_Xctronlyonetargettool=db.ws(ws=TAB).col(col=50) #AX
    colA_Ytoolproposal=db.ws(ws=TAB).col(col=51) #AY
    colA_Ztoolproposal2=db.ws(ws=TAB).col(col=52) #AZ
    colB_Aifs4=db.ws(ws=TAB).col(col=53) #BA
    colB_Bifnots4where=db.ws(ws=TAB).col(col=54) #BB
    colB_Cs4stdlevel=db.ws(ws=TAB).col(col=55) #BC
    colB_Dweigh=db.ws(ws=TAB).col(col=56) #BD
    colB_Ecostifdevinprod=db.ws(ws=TAB).col(col=57) #BE
    colB_Fneededs4p2=db.ws(ws=TAB).col(col=58) #BF
    colB_Gcomment=db.ws(ws=TAB).col(col=59) #BG
    colB_Hopenquestions=db.ws(ws=TAB).col(col=60) #BH
    colB_Iforcastedyear=db.ws(ws=TAB).col(col=61) #BI
    colB_Jtargetreached=db.ws(ws=TAB).col(col=63) #BJ

    l_alreadyAdded = []
    g = pyyed.Graph()
    g.define_custom_property("node", "UseCase", "string", "")

    for items in zip(colAcolId, colBmacroprocess, colCfunctionfuture, colDkeyword, colEmarketid, colFsubfunctionlist, colGfuturesubfunctiongeneraldescription, colHuserstoryinformation, colIopoldnpnew, colJsubfunctfutureyntd, colKsuitabilityofthesitoday, colLcollabor, colMprodcom, colNlink, colOapo, colPfms, colQecc, colRcape, colSordermax, colTrank2, colUassessgo, colVcpp, colWpsv, colXsnc, colYmoldgo, colZassetgo,
                     colA_Apace, colA_Btacticalsop, colA_Cetco, colA_Dlinkwithtool, colA_Eothers, colA_Ffunctiongap, colA_Gpainsolved, colA_Htarget, colA_Iproductionreferencer, colA_Jordermanager, colA_Kstockmanager, colA_Lcptquotationmanager, colA_Mcptplanner, colA_Nalertmanager, colA_Opreinvoicemanager, colA_Pmold, colA_Qapo, colA_Rassesgo, colA_Sexpeditionpreparation, colA_Tbi, colA_Uauthorisationmanager, colA_Vadminparameters, colA_Wother, colA_Xctronlyonetargettool, colA_Ytoolproposal, colA_Ztoolproposal2,
                     colB_Aifs4, colB_Bifnots4where, colB_Cs4stdlevel, colB_Dweigh, colB_Ecostifdevinprod, colB_Fneededs4p2, colB_Gcomment, colB_Hopenquestions, colB_Iforcastedyear, colB_Jtargetreached
                    ):

        processLine = True
        try:
            id = int(items[0])
        except ValueError:
            processLine = False

        if processLine:
            # IDgeneration ####################################################
            Level1ID = stringutil.cleanName(
                                                items[2],
                                                True,
                                                True,
                                                'lowercase',
                                                True,
                                                True,
                                                True) \
                            + '_Level1'
            Level2ID = Level1ID+stringutil.cleanName(
                                                items[3],
                                                True,
                                                True,
                                                'lowercase',
                                                True,
                                                True,
                                                True) \
                            + '_Level2'
            Level3ID = Level2ID+stringutil.cleanName(
                                                items[4],
                                                True,
                                                True,
                                                'lowercase',
                                                True,
                                                True,
                                                True) \
                            + '_Level3'
            
            #Level1 ###############################################################1
            if Level1ID not in l_alreadyAdded:
                l_alreadyAdded.append(Level1ID)

                Name = stringutil.cleanName(
                                                    items[2],
                                                    False,
                                                    False,
                                                    'nochange',
                                                    True,
                                                    False,
                                                    False) \
                        + ' (L1)'
                Documentation = ''
                toWrite= csvutil.initElements(ID=Level1ID, Type=ELEMENTTYPE, Name=Name, Documentation=Documentation)
                outputfiles[1].writerow(toWrite)

                toWrite = csvutil.initProperties(ID=Level1ID, Key=KEY, Value=VALUE)
                outputfiles[3].writerow(toWrite)

                g.add_node(Level1ID, label=Name, font_size=L1FONTSIZE, font_style=L1FONTSTYLE, width=WIDTH, shape_fill=L1COLOR)

            
            #Level2 ###############################################################
            if Level2ID not in l_alreadyAdded:
                l_alreadyAdded.append(Level2ID)
                Name = stringutil.cleanName(
                                                    items[3],
                                                    False,
                                                    False,
                                                    'nochange',
                                                    True,
                                                    False,
                                                    False) \
                        + ' (L2)'
                Documentation = ''
                toWrite= csvutil.initElements(ID=Level2ID, Type=ELEMENTTYPE, Name=Name, Documentation=Documentation)
                outputfiles[1].writerow(toWrite)

                toWrite = csvutil.initProperties(ID=Level2ID, Key=KEY, Value=VALUE)
                outputfiles[3].writerow(toWrite)

                toWrite = csvutil.initRelations(ID=Level2ID, Type=RELATIONTYPE, Source=Level1ID, Target=Level2ID)
                outputfiles[5].writerow(toWrite)

                g.add_node(Level2ID, label=Name, font_size=L2FONTSIZE, font_style=L2FONTSTYLE, width=WIDTH, shape_fill=L2COLOR)
                g.add_edge(Level1ID, Level2ID)


            #Level 3 ##############################################################
            if Level3ID not in l_alreadyAdded:
                l_alreadyAdded.append(Level3ID)
                Name = stringutil.cleanName(
                                                    items[4],
                                                    False,
                                                    False,
                                                    'nochange',
                                                    True,
                                                    False,
                                                    False) \
                        + ' (L3)'
                Doc1 = stringutil.cleanName(
                                                    items[5],
                                                    False,
                                                    False,
                                                    'nochange',
                                                    True,
                                                    False,
                                                    False)
                Doc2 = stringutil.cleanName(
                                                    items[6],
                                                    False,
                                                    False,
                                                    'nochange',
                                                    True,
                                                    False,
                                                    False)
            
                toWrite= csvutil.initElements(ID=Level3ID, Type=ELEMENTTYPE, Name=Name, Documentation=Doc1+Doc2)
                outputfiles[1].writerow(toWrite)

                toWrite = csvutil.initProperties(ID=Level3ID, Key=KEY, Value=VALUE)
                outputfiles[3].writerow(toWrite)

                toWrite = csvutil.initRelations(ID=Level3ID, Type=RELATIONTYPE, Source=Level2ID, Target=Level3ID)
                outputfiles[5].writerow(toWrite)

                g.add_node(Level3ID, label=Name, font_size=L3FONTSIZE, font_style=L3FONTSTYLE, width=WIDTH, shape_fill=L3COLOR,
                            custom_properties={"UseCase": Doc1})
                g.add_edge(Level2ID, Level3ID)
                # g.add_node(Level3ID+'B', label=items[5]+items[6], font_size=L3FONTSIZE, font_style=L3FONTSTYLE)
                # g.add_edge(Level3ID, Level3ID+'B', label="use case is")
        
                g.write_graph(MAIN_FOLDER + os.path.sep + YEDFILE, pretty_print=True)

