from enum import Enum

'''
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
AE : Documentation for "N3" / concatenate with G and H and AD separated via \n and prefixed by "other tools : "
AF :  / create a child assessment of the assessment 'N' created for K + ArchiProperties.AFAssessment
AG :  / if I = "NP" and not empty, create an outcome child of the outcome "Pain Solved by new process"

TODO : add an ID to all requirements, assessments and outcome

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



    @staticmethod
    def list():
        return list(map(lambda c: c.value, ArchiProperties))

class PlateauToCreate(Enum):
    # used to create the plateaux and link the subfunctions to the plateaux
    PRODASIS = 'Transformation Prod.com AS-IS'
    PRODTOBE = 'Transformation Prod.com TO-BE'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, PlateauToCreate))

class FunctionListToolkit(object):
    def __init__(self) -> None:
        # futureAssessment : from column J.
        # used to create the assessments and then link them to the sub function.
        #  If the cell is empty :  do not link to an assessment
        # The value from the spreasheet is stored in the property ArchiProperties.SUBFUNCTIONFUTURE
        # create a parent assessement "Future of the function" and the childs below
        self.futureAssessment = {'?': 'Do not know', 
                                 'T': 'Keep function, Transpose it in another tool',
                                 'T?': 'Keep function, Transpose it in another tool, Assessment not 100pct sure',
                                 'Y/T': 'Keep but uncertainty on tool',
                                 'N': 'excluded from the future sub-function due to no value for the users',
                                 'N?': 'excluded from the future sub-function due to no value for the users, Assessment not 100pct sure',
                                 'D': 'deleted because it as a  doublet',
                                 'Y': 'Keep for future',
                                 'Y?': 'Keep for future, Assessment not 100pct sure'
        }
        # suitabilityAssessment : from column K.
        # The value from the spreadsheet is stored in the property ArchiProperties.
        # create a parent assessment "Suitability of the function" and these childs :
        self.suitabilityAssessment = {'N': 'Do not fullfill the business need',
                                        'Y': 'Fullfill the business need'
        }
        # collaborationRequirement : from column L.
        # The value from the spreadsheet is stored in the property ArchiProperties.
        # Create a parent requirement "Collaboration with the supplier" and these childs :
        self.collaborationAssessment = {'N': 'We want to collaborate with the Supplier',
                                        'Y': 'We do not want to collaborate with the supplier'
        }
        # OldNewProcessAssessment : from column I.
        # The value from the spreadsheet is stored in the property ArchiProperties.
        # Create a parent assessment "Old or New Process ?" and these childs
        self.oldNewProcessAssessment = {'OP': 'Old Process',
                                        'NP': 'New Process'
        }

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
                                'U': 'id-705bd79c-9a3e-49d7-81c0-ff51c8e2b1bf', # Assess GO
                                'V': 'id-127c49ca-0a73-4d21-8863-424dadc0620b', #CPP
                                'W': 'id-89ab3ca484e2459c865b4989e6815d1d', #PSV
                                'X': 'ec64ef8e-e763-4b82-9e61-1e568bb0e907', #SAPSNC
                                'Y': 'id-639a99c0-7499-4366-ba87-ae236d99489d', #Mold
                                'Z': 'id-705bd79c-9a3e-49d7-81c0-ff51c8e2b1bf', #AssessGo
                                'AA': 'id-6b2c94a449a84e5fac4e17d01a291c86', #Pace
                                'AB': 'a7efee8a-a0ec-4475-b531-d77f93c49978', # Tactical S&OP
                                'AC': 'id-1fd605bd-76cb-44c0-914c-f8d4e32947db', #ETCO
        }
