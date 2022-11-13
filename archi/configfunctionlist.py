from enum import Enum

'''
concepts to creat if necessary prior to other things :
- Plateau
- asIsLandscape
- oldNewProcessAssessment
- collaborationAssessment
- suitabilityAssessment
- futureAssessment


column : map to /  work to do
B : processus "N1" /
C : function "N2" / "N1" aggregates "N2" + ArchiProperties.LINKTON1 = "N1" cleanName 
D : property ArchiProperties.KEYWORD for "N2" / 
E : Documentation for "N2" /
F : function "N3 / "N2" aggregates "N3" + ArchiProperties.LINKTON2 = "N2" cleanName
G : Documentation for "N3"
H : Documentation for "N3" / concatenate with G separated via \n
I : Link to Assessment FunctionListToolkit.oldNewProcessAssessment + ArchiProperties.OldOrNewProcess
J : propertie ArchiProperties.SUBFUNCTIONFUTURE / link value to FunctionListToolKit.futureAssessment ==> previously create the assessments
K : propertie ArchiProperties.SUITABILITY / link value to FunctionListToolKit.suitabilityAssessment ==> previously create the assessments
L : propertie ArchiProperties.COLLAB / link value to FunctionListToolKit.collaborationAssessment ==> previously create the assessments
M-AC : use FunctionListToolKit.asIsLandscape to link to the right app. + property ArchiProperties.AppAssigned + link to plateau PlateauToCreate.PRODASIS
AD : Documentation for "N3" / concatenate with G and H separated via \n and prefixed by "link to these tools : "
AE : cleanname (do not remove special characters), split on / then split on +
AF :  / create a child assessment of the assessment 'N' created for K + ArchiProperties.AFAssessment + link to N3
AG :  / if I = "NP" and not empty, create an outcome child of the outcome "Pain Solved by new process"
AH : link "N3" to FunctionListToolKit.targetAssessment + ArchiProperties.targetAssessment
AI : link "N3" to FunctionListToolKit.productionReferencerAssessment + ArchiProperties.productionReferencer
AJ-AV : link "N3" to APP in AY and AZ + link app (AY and AZ) to resource FunctionListToolkit.toBeResources in AJ-AV + ArchiProperties.resource + ArchiProperties.apptobe
        --> creat APP directly in Archi
AW : can be ignored, link AY & AZ directly to N3
AX : to ignore
AY : cleanname (do not remove special character), split on ?.  create if do not exist, link to "not sure" if len(list) > 1
AZ : cleanname (do not remove special character), split on &, create all app in the lsit if necessary
BA-BF : create an assessment S/4 Analysis a child assessment for each column and a child for each value

'''

class ArchiProperties(Enum):
    IMPORTEDFROMFUNCTIONLIST = 'ImportedFromFunctionList'
    KEYWORD = 'Keyword'
    LINKTON1 = 'LinkedToThatN1'
    LINKTON2 = 'LinkedToThatN2'
    LINKTOPLATEAU = 'LinkedToThatPlateau' # from column I
    SUBFUNCTIONFUTURE = 'SubFunctionFuture' # from column J
    PRODASIS = 'PlateauAsIs' # Plateau to create to link column J. It's a property to use only for the Plateaux that are created
    PRODTOBE = 'PlateauToBe' # like above
    SUITABILITY = 'Suitability'
    COLLAB = 'Collaboration'
    APPASSIGNED = 'AppAssigned'
    AFASSESSMENT = 'AFAssessment'
    OLDNEWPROCESS = 'OldOrNewProcess'
    TARGETASSEMENT = 'targetAssessment'
    PRODUCTIONREFERENCER = 'Production Referencer'
    RESOURCE = 'Resource'
    APPTOBE = 'AppToBe'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ArchiProperties))

class ArchiConcepts(Enum):
    COMPOSITIONRELATION = 'CompositionRelationship'
    BUSINESSPROCESS = 'BusinessProcess'
    BUSINESSFUNCTION = 'BusinessFunction'
    ASSOCIATIONRELATION = 'AssociationRelationship'
    ASSIGNEMENTRELATION = 'AssignmentRelationship'
    ASSESSMENT = 'Assessment'
    AGGREGATIONRELATION = 'AggregationRelationship'
    OUTCOME = 'Outcome'
    REALIZATIONRELATION = 'RealizationRelationship'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ArchiConcepts))

class YedProperties(Enum):
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

    @staticmethod
    def list():
        return list(map(lambda c: c.value, YedProperties))

PREFIXTOID = 'ICMO-' # that prefix will be complemented by the cleaned name up to 39 characters includinf the prefix
DOCSEPARATOR = "|||\n"
YEDFILEPREFIX = 'FunctionListYED'
YEDFILESUFFIX = '.graphml'
ARCHIPREFIX = 'impflcmo'
TAB='Clean List'
YES='Y'
NO='N'
SPLITAPPON='&'
MTOACEXPECTEDVALUE = 'Y'
AJTOAVEXPRECTEDVALUE = 'X'
SUITABILITYEXPECTEDVALUE = ('Y', 'N')

# column I.
I_OLDNEWPROCESSASSMENT = {'OP': 'id-bc7e380a92844733bc25589ee80a0b3c', # 'Old Process',
                                'NP': 'id-8416d5b25dce4717aff279fa55c0b97b', # 'New Process'
}

# link accordingly apps from as is / to be landscape 
class Plateaux(Enum):
    ASIS = 'id-6579a4f9a64349cdaa0118ae7471803f'
    TOBE = 'id-12de8bea5eb34d2188298a69f918262e' 

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Plateaux))


# column J.
J_FUTUREASSESSMENT = {'?': 'id-0d5e3f1dfd234798941af9efe25e8bbd', #'Do not know', 
                            'T': 'id-25390d4dbe8c4a9bbac414c42d23f8ee', # 'Keep function, Transpose it in another tool',
                            'T?': 'id-794382a1a4724d6989fb6c758c879e51', # '(not sure) Keep function, Transpose it in another tool',
                            'Y/T': 'id-6d4b3d4ce40d41cd921c646248925121', # 'Keep but uncertainty on tool',
                            'N': 'id-f7f1b422e0c74c6cab2fd703072ec700', # 'excluded from the future sub-function due to no value for the users',
                            'N?': 'id-79d8a1ce4fff48bea458321e144bbed8', # '(not sure) excluded from the future sub-function due to no value for the users',
                            'D': 'id-dc64608609bb4d21b314d78ed166d0f8', # 'deleted because it as a doublet',
                            'Y': 'id-edc51050f9c244798afd195b98ade1a2', # 'Keep for future',
                            'Y?': 'id-d319cb40623e4c408d2faec3b430fd5f', # '(not sure) Keep for future'
}
# column K.
K_SUITABILITYASSESSMENT = {'N': 'id-2743503fad7e444b834200ecb839e6d2', # 'Do not fullfill the business need',
                                'Y': 'id-51ef9790aabc4c1586310013717c0f4d', # 'Fullfill the business need'
}
# column L.
L_COLLABORATIONREQUIREMENT = {'Y': 'id-ebbd2ea860064784bee3818b20e2b0fd', # 'We want to collaborate with the Supplier',
                                'N': 'id-15a6a454eb0e42c4959915feb0d86324', # 'We do not want to collaborate with the supplier'
}

# column AH.
AH_TARGETASSESSMENT = {'Y': 'id-870462cc1c2d4995aeb0c247c79003d0', # 'This is a target process',
                            'N': 'id-7c8a58af73e44f3ca85556e43e66ed64', # 'This is not a target process'
}

# columns M to AC.
# key : the column
# value : the id in Archi of the app
MAC_ASISLANDSCAPE = {'M': 'id-192b1d1207224c47bedae9878bfd9ad6', #prod.com
                        'N': 'e3399ac2-4e43-4c33-987e-fb3009ae1dcc', #LINK
                        'O': 'id-45864c5fd431470498a528db100857ba', # SAP APO
                        'P': 'id-0bff31b62eaa43918c23c5b0a21369cb', #FMS
                        'Q': 'id-006f61c9520a4fe99f149d794ca87c20', # SAP ECC CORP
                        'R': 'id-6a611baeddcd4f0e886168a038179b3f', # CAPE ou CAPETM ? : 'id-0285b0c626e44cb6b41805b293e94235'
                        'S': 'd9d24b08-3dfa-416c-a167-ec1ef66c22e2', # Order Max
                        'T': 'id-228ec315252e4465a03ec94c3facb035', # Rank2
                        'U': '705bd79c-9a3e-49d7-81c0-ff51c8e2b1bf', # Assess GO --> doublet with column Z.
                        'V': '127c49ca-0a73-4d21-8863-424dadc0620b', #CPP
                        'W': 'id-89ab3ca484e2459c865b4989e6815d1d', #PSV
                        'X': 'ec64ef8e-e763-4b82-9e61-1e568bb0e907', #SAPSNC
                        'Y': '639a99c0-7499-4366-ba87-ae236d99489d', #Mold
                        'Z': '705bd79c-9a3e-49d7-81c0-ff51c8e2b1bf', #AssessGo --> doublet with column U
                        'AA': 'id-6b2c94a449a84e5fac4e17d01a291c86', #Pace
                        'AB': 'a7efee8a-a0ec-4475-b531-d77f93c49978', # Tactical S&OP
                        'AC': '1fd605bd-76cb-44c0-914c-f8d4e32947db', #ETCO
}

#column AG
AG_PAINSOLVED = {'AG': 'id-a27ed20cd5a24e84b8e6ce219087a123'}

# columns AY & AZ  (values in the cells)
AYAZ_TOBELANDSCAPE = {
                        'accessid': 'id-c9e7afb6b4a24ab1b21fb860580b1d72', # identity access
                        '?': 'id-48b86642f7f84d298677fbf61efca7fb', # app to define
                        'alerting': 'id-fa6d9789ef4c4446a144819e0aca1821', # my alert
                        'apo': 'id-45864c5fd431470498a528db100857ba', # SAP APO
                        'aps?': 'id-2e999e92a37844c087e39b11f76eadef', # smart Planning for components + link to assessment "not sure of the tool to use in the future" 
                        'aps': 'id-2e999e92a37844c087e39b11f76eadef', # smart Planning for components
                        'assessgo': '705bd79c-9a3e-49d7-81c0-ff51c8e2b1bf', # assessGO
                        'assesgo': '705bd79c-9a3e-49d7-81c0-ff51c8e2b1bf', # assessGO
                        'bommgr': 'id-fd4fe2e2dcad48a7ac80658add009443', # BOM Manager
                        'bom': 'id-fd4fe2e2dcad48a7ac80658add009443', # BOM Manager
                        'com': 'id-b905fc58b87244b3addfb56552331fbc', # communication
                        'dpcpdashboard': '7af32f96-b3d5-4f0c-8973-7ccda679dddd', #DPCP Dashboard
                        'dpcpportal': '4964247a-745b-42f1-a1be-b23945745038', #DPCP Portal
                        'forecastcollab': 'c5ba2e10-96a7-4267-9df0-3a1379d6f497', # DPCP Forecast (e)
                        'integrator': 'id-b566b7c2685242f8a167487115cf6b23', # Integrator
                        'linkeo': 'id-ee73b67f112f4595893d498bbdda059f', #linkeo
                        'ordercollab': 'id-a95f7fe378b542a9bc6dcb245fe3799d', # Order Collaboration
                        'othermodules': 'id-b900bbddcbae49258d5b1ad8bb2ad219', # Other Modules ?
                        'plm': 'id-a976bb6a4ea14dcf996797476177e6eb', # PLM (Spark)
                        'psv': 'id-89ab3ca484e2459c865b4989e6815d1d', # PSV (Production Stock Visibility)
                        'rank2': 'id-228ec315252e4465a03ec94c3facb035', # Rank2 platform
                        'rfid': 'id-45dd37a7e2614d17b8b840e9317c3c35', # RFID Order
                        'rfidorder': 'id-45dd37a7e2614d17b8b840e9317c3c35', #RFID Order
                        'rfq': 'id-45864c5fd431470498a528db100857ba', # SAP APO
                        's/4': 'id-f78c58175d774305a90a69becd71a3b7', # S/4 
                        's/4?': 'id-f78c58175d774305a90a69becd71a3b7', # S/4 
                        'sac': 'id-1d5dd6cea6784be48dc7537b665ac088', # SAP SAC
                        'shu': 'e154fd41-ece4-4d01-8818-007839fdeb4f', # SHU SSCC (e) 
                        'stockcollab': 'id-5eefed56469b49bdb7fc3b2b81663bbf', # Stock Collab
                        'wms': 'id-ed63d508610f420592774b87760ae98a', # WMS App
                        'pi4t': 'id-363075155640440892b2119036575b72', #PI4T
                        'mold': '639a99c0-7499-4366-ba87-ae236d99489d', #Mold
                        'mould': '639a99c0-7499-4366-ba87-ae236d99489d', #Mold
                        'perimeter': 'id-88f4536d78ba45c281767fc8a85c0d91', #PERIMETER
                        'wm': 'id-ed63d508610f420592774b87760ae98a', # WMS app
                        'tms': 'id-0285b0c626e44cb6b41805b293e94235', # CAPETM
                        'md': '631e94a7-58f1-44d1-848b-687dc34f6a66', # Master data ?
                        'alertingtool': 'id-8db799a93b9444d5853f8cb13d9fd381', # alerting tool
                        'alerting?' : 'id-8db799a93b9444d5853f8cb13d9fd381', # alerting tool
                        'it': 'id-435e1c5f710547c6ad7fef5fbb2aeed1', # IT tool
                        'selfbilling': 'id-109863eac0184976b84f6c532f3011a1', # Self Billing
                        'ecc': 'id-006f61c9520a4fe99f149d794ca87c20', # SAP ECC CORP
                        'gex': 'id-f5f6bc68e50b4621918960815ed394cd' # GEX IVALUA
                        
}

AYAZ_EXCEPTIONLIST = ['aps/apo', 'eccaps', 's/4?', 's/4/bom?', 'sac?aps?', 's/4/rank2', 'psvs/4', 'assesgo/gex']

# column AI
AI_PRODUCTIONREFERENCERASSESSMENT = {'x': 'Tecnically needed for S/4 but can also be the MD main tool (not compulsory if the DB is the same)'
}

# columns AJ to AV
AIAV_TOBERESOURCES = {'AI': 'id-ef7fead320de457d9700fd14aa4b9f84', # Production Referencer
                        'AJ': 'id-53efadb0186246fc84af42b9d57a7790', #'Order Manager',
                        'AK': 'id-1ce1072e0e614b63a30748fabce61004', #'Stock Manager',
                        'AL': 'id-9299e5238ff8442e92fe39338db288cd', #'CPT Quotation Manager',
                        'AM': 'id-2d61455566a041f2ad0b4ed50e7fbeb0', #'CPT Planner (MRP)',
                        'AN': 'id-544df78e57e745fdbd7e98526be87304', #'Alert Manager',
                        'AO': 'id-5d263f778cd7486da47c83a7e8a4db1d', #'Pre Invoice Manager',
                        'AP': 'id-b167f327ceea459796c7331ad62a17e2', #'Componnent Manager(Mold)',
                        'AQ': 'id-c4d639e83afb4c2290337852cabb1b2f', #'Sales / Purchase Forecast (APO)',
                        'AR': 'id-d4e1eff616954b84a51740c220dfa073', #'Supplier Manager (Assess GO)',
                        'AS': 'id-f2df5bfce1394b818e63b4853039c124', #'Expedition / Preparation',
                        'AT': 'id-cc7a56aa79e7435781e0c48e70bbcbf5', #'BI',
                        'AU': 'id-b2a6811f33ab4134b9f1b7408b42c3b6', #'Athorization Manager',
                        'AV': 'id-762a65c23b164d2b934114d313291b89', #'ADMIN Parameters'
}

# columns BA - BF
# the key is the concatenation of the column's name and the value that can be encountered in the cell
BABF_S4ANALYSIS = {
                    'BAP': 'id-ea56ed63074644a5bcf3a4a7e96a7e39', # Partially managed in S/4
                    'BAY': 'id-38d13a26ba8f45dba76dcc7ccf1e6cd5', # Fully managed in S/4
                    'BAN': 'id-800a2846b8ce44e2b4fd46ae5f74c91d', # Not managed in S/4
                    'BCS': 'id-859f4c368bd441828f74a8a1876ba6e9', # S : Standard
                    'BCP': 'id-28c86b37b4e54065a7515e15a3f33576', # P : With Process adjustment
                    'BCE': 'id-869a86cd77a14844af056c6bf14446f9', # E : To manage in External module
                    'BCD': 'id-4777426700d0471cac777355f17f9365', # D : Dev required
                    'BCA': 'id-2a82b4d5dc3441dc9e819dda25b97c83', # A : Impossible => Abort
                    'BC?': 'id-bb1c86180aee4765b0db0294cda27caa', # ? : to study ni detail
                    'BD*': 'id-7970a56ecdc94ea5b489467f4642a388', #* nice to have
                    'BD**': 'id-dcb8a6ec110c48ffbac8d3f4d1345782', #** usefull
                    'BD***': 'id-cfdede8577b24639ae15f6b983ee57af', #*** important
                    'BD****': 'id-b5a58e51d2f749a6989407065028d4da', #**** very important
                    'BD*****': 'id-e69fcd29fd5445b9aa96a8cf16f1f77e', #***** impossible to work w/o it 
                    'BE-': 'id-bd2606ec530846348bc386a8ed44afcc', #
                    'BE*': 'id-5a5b2c140c7a4ce39feba1cdc00de578', #
                    'BE**': 'id-4864fdff3b6247029ace9835d19e9a7c', #
                    'BE***': 'id-6f84441cc7d24e03a2c82f2bf381f919', #
                    'BEincl': 'id-e83f588f94f4424e8a0697ab424c22d3', #
                    'BENA': 'id-084f66a25d2d4abbb0fa1882ca95abd0', #
                    'BFp': 'id-172db897c8e14f9899c45eb49cf875b8', # develop in prod.com
                    'BF2.0': 'id-261bdb455064420cacd97a3ccd257737', # develop in S/4 and prod.com
                    'BFS/4': 'id-14fff60b514442949135e863fbbd9916', # develop in S/4
}
