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

# column I.
COLI_OLDNEWPROCESSASSMENT = {'OP': 'id-bc7e380a92844733bc25589ee80a0b3c', # 'Old Process',
                                'NP': 'id-8416d5b25dce4717aff279fa55c0b97b', # 'New Process'
}

# link accordingly apps from as is / to be landscape 
PLATEAUX = {'AsIs' : 'id-6579a4f9a64349cdaa0118ae7471803f',
                    'ToBe': 'id-12de8bea5eb34d2188298a69f918262e' 
}
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

# columns AY & AZ
AYAZ_FUTUREASSESSMENT = { '?': 'id-d51ad52b3ae4497ba67abece2fbf536e'}, # 'Not sure of the tool to use in the future',

# columns M to AE.
# key : the column
# value : the id in Archi of the app
MAE_ASISLANDSCAPE = {'M': 'id-9b38f547-e31e-4bc8-b65b-0e52cf759fc9', #prod.com
                        'N': 'e3399ac2-4e43-4c33-987e-fb3009ae1dcc', #LINK
                        'O': 'id-45864c5fd431470498a528db100857ba', # SAP APO
                        'P': 'id-0bff31b62eaa43918c23c5b0a21369cb', #FMS
                        'Q': 'id-006f61c9520a4fe99f149d794ca87c20', # SAP ECC CORP
                        'R': 'id-6a611baeddcd4f0e886168a038179b3f', # CAPE ou CAPETM ? : 'id-0285b0c626e44cb6b41805b293e94235'
                        'S': 'd9d24b08-3dfa-416c-a167-ec1ef66c22e2', # Order Max
                        'T': 'id-228ec315252e4465a03ec94c3facb035', # Rank2
                        'U': 'id-705bd79c-9a3e-49d7-81c0-ff51c8e2b1bf', # Assess GO --> doublet with column Z.
                        'V': 'id-127c49ca-0a73-4d21-8863-424dadc0620b', #CPP
                        'W': 'id-89ab3ca484e2459c865b4989e6815d1d', #PSV
                        'X': 'ec64ef8e-e763-4b82-9e61-1e568bb0e907', #SAPSNC
                        'Y': 'id-639a99c0-7499-4366-ba87-ae236d99489d', #Mold
                        'Z': 'id-705bd79c-9a3e-49d7-81c0-ff51c8e2b1bf', #AssessGo --> doublet with column U
                        'AA': 'id-6b2c94a449a84e5fac4e17d01a291c86', #Pace
                        'AB': 'a7efee8a-a0ec-4475-b531-d77f93c49978', # Tactical S&OP
                        'AC': 'id-1fd605bd-76cb-44c0-914c-f8d4e32947db', #ETCO
}

# columns AY & AZ  (values in the cells)
AYAZ_TOBELANDSCAPE = {
                        'accessid': 'id-c9e7afb6b4a24ab1b21fb860580b1d72', # identity access
                        '?': 'id-48b86642f7f84d298677fbf61efca7fb', # app to define
                        'alerting': 'id-fa6d9789ef4c4446a144819e0aca1821', # my alert
                        'apo': 'id-45864c5fd431470498a528db100857ba', # SAP APO
                        'aps?': 'id-2e999e92a37844c087e39b11f76eadef', # smart Planning for components + link to assessment "not sure of the tool to use in the future" 
                        'aps': 'id-2e999e92a37844c087e39b11f76eadef', # smart Planning for components
                        'assessgo': 'id-705bd79c-9a3e-49d7-81c0-ff51c8e2b1bf', # assessGO
                        'bommgr': 'id-fd4fe2e2dcad48a7ac80658add009443', # BOM Manager
                        'com': 'id-b905fc58b87244b3addfb56552331fbc', # communication
                        'dpcpdashboard': 'id-7af32f96-b3d5-4f0c-8973-7ccda679dddd', #DPCP Dashboard
                        'dpcpportal': 'id-4964247a-745b-42f1-a1be-b23945745038', #DPCP Portal
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
                        'sac': 'id-1d5dd6cea6784be48dc7537b665ac088', # SAP SAC
                        'shu': 'e154fd41-ece4-4d01-8818-007839fdeb4f', # SHU SSCC (e) 
                        'stockcollab': 'id-5eefed56469b49bdb7fc3b2b81663bbf', # Stock Collab
                        'wms': 'id-ed63d508610f420592774b87760ae98a' # WMS App
                        
}

# column AI
AI_PRODUCTIONREFERENCERASSESSMENT = {'x': 'Tecnically needed for S/4 but can also be the MD main tool (not compulsory if the DB is the same)'
}

# columns AJ to AV
AJAV_TOBERESOURCES = {'AJ': 'id-53efadb0186246fc84af42b9d57a7790', #'Order Manager',
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