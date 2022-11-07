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

class FunctionListToolkit(object):
    def __init__(self) -> None:


        self.prefixToID = 'IFFLBCMO-' # that prefix will be complemented by the cleaned name up to 39 characters includinf the prefix

        self.plateaux = {'AsIs' : 'id-6579a4f9a64349cdaa0118ae7471803f',
                            'ToBe': 'id-12de8bea5eb34d2188298a69f918262e' 
        }
        # futureAssessment : from column J.
        # used to create the assessments and then link them to the sub function.
        #  If the cell is empty :  do not link to an assessment
        # The value from the spreasheet is stored in the property ArchiProperties.SUBFUNCTIONFUTURE
        # create a parent assessement "Future of the function" and the childs below
        self.futureAssessment = {'?': 'id-0d5e3f1dfd234798941af9efe25e8bbd', #'Do not know', 
                                 'T': 'id-25390d4dbe8c4a9bbac414c42d23f8ee', # 'Keep function, Transpose it in another tool',
                                 'T?': 'id-794382a1a4724d6989fb6c758c879e51', # '(not sure) Keep function, Transpose it in another tool',
                                 'Y/T': 'id-6d4b3d4ce40d41cd921c646248925121', # 'Keep but uncertainty on tool',
                                 'N': 'id-f7f1b422e0c74c6cab2fd703072ec700', # 'excluded from the future sub-function due to no value for the users',
                                 'N?': 'id-79d8a1ce4fff48bea458321e144bbed8', # '(not sure) excluded from the future sub-function due to no value for the users',
                                 'D': 'id-dc64608609bb4d21b314d78ed166d0f8', # 'deleted because it as a doublet',
                                 'Y': 'id-edc51050f9c244798afd195b98ade1a2', # 'Keep for future',
                                 'Y?': 'id-d319cb40623e4c408d2faec3b430fd5f', # '(not sure) Keep for future'
        }
        # suitabilityAssessment : from column K.
        # The value from the spreadsheet is stored in the property ArchiProperties.
        # create a parent assessment "Suitability of the function" and these childs :
        self.suitabilityAssessment = {'N': 'id-2743503fad7e444b834200ecb839e6d2', # 'Do not fullfill the business need',
                                        'Y': 'id-51ef9790aabc4c1586310013717c0f4d', # 'Fullfill the business need'
        }
        # collaborationRequirement : from column L.
        # The value from the spreadsheet is stored in the property ArchiProperties.
        # Create a parent requirement "Collaboration with the supplier" and these childs :
        self.collaborationRequirement = {'Y': 'id-ebbd2ea860064784bee3818b20e2b0fd', # 'We want to collaborate with the Supplier',
                                        'N': 'id-15a6a454eb0e42c4959915feb0d86324', # 'We do not want to collaborate with the supplier'
        }
        # OldNewProcessAssessment : from column I.
        # The value from the spreadsheet is stored in the property ArchiProperties.
        # Create a parent assessment "Old or New Process ?" and these childs
        self.oldNewProcessAssessment = {'OP': 'id-bc7e380a92844733bc25589ee80a0b3c', # 'Old Process',
                                        'NP': 'id-8416d5b25dce4717aff279fa55c0b97b', # 'New Process'
        }

        # TargetAssessment : from column AH.
        # The value from the spreadsheet is stored in the property ArchiProperties.
        self.TargetAssessment = {'Y': 'id-870462cc1c2d4995aeb0c247c79003d0', # 'This is a target process',
                                 'N': 'id-7c8a58af73e44f3ca85556e43e66ed64', # 'This is not a target process'
        }

        # futureToolAssessment : used when there is a ? in the name in the columns AY & AZ
        # The value from the spreadsheet is stored in the property ArchiProperties.
        self.futureToolAssessment = { '?': 'id-d51ad52b3ae4497ba67abece2fbf536e'}, # 'Not sure of the tool to use in the future',

        #asIsLandscape : from column M to AE.
        # key : the column
        # value : the id in Archi of the app
        self.asIsLandscape = {'M': 'id-9b38f547-e31e-4bc8-b65b-0e52cf759fc9', #prod.com
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

        #toBeLanscape : from column AY & AZ  (values in the cells)
        self.toBeLandscape = {'apo': 'id-45864c5fd431470498a528db100857ba', # SAP APO
                                'aps': 'id-9b695f97aaf3461a9102ed944a26380f', # APS (BlueYonder)
                                'aps?': 'id-9b695f97aaf3461a9102ed944a26380f', # Blue yonder + link to assessment "not sure of the tool to use in the future" 
                                'bommgr': 'id-fd4fe2e2dcad48a7ac80658add009443', # BOM Manager
                                'forecastcollab': 'c5ba2e10-96a7-4267-9df0-3a1379d6f497', # DPCP Forecast (e)
                                'integrator': 'id-b566b7c2685242f8a167487115cf6b23', # Integrator
                                'ordercollab': 'id-a95f7fe378b542a9bc6dcb245fe3799d', # Order Collaboration
                                's4': 'id-f78c58175d774305a90a69becd71a3b7', # S/4 
                                'shu': 'e154fd41-ece4-4d01-8818-007839fdeb4f', # SHU SSCC (e) 
                                'plm': 'id-a976bb6a4ea14dcf996797476177e6eb', # PLM (Spark)
                                'stockcollab': 'id-5eefed56469b49bdb7fc3b2b81663bbf', # 
                                
        }

        self.targetAssessment = {'N': 'id-7c8a58af73e44f3ca85556e43e66ed64', # 'This is not a target process',
                                    'Y': 'id-870462cc1c2d4995aeb0c247c79003d0', # 'This is a target process'
        }
        self.productionReferencerAssessment = {'x': 'Tecnically needed for S/4 but can also be the MD main tool (not compulsory if the DB is the same)'
        }
        self.toBeResources = {'AI': 'id-ef7fead320de457d9700fd14aa4b9f84', #'Production Referencer',
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

