from enum import IntEnum, Enum

class NodeType(Enum):
    '''
    list the nodes type to parse in the Archi file
    '''
    ELEMENT = 'element'
    RELATIONSSHIP = 'relationship'
    VIEW = 'view'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, NodeType))

class ToGet(Enum):
    '''
    ATTR to get the attributes of the node
    DATA to get the value of the node
    NONE to ignore the node
    '''
    ATTR = 'attr'
    DATA = 'firstChild.data'
    NONE = None

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ToGet))

class ToStore(Enum):
    '''
    list the information I want to keep from XML File.
    The value has either the form parentNode-node or parentNode-NodeAttribute
    '''
    EI='elements-identifier'
    ET='elements-type'
    EN='element-name'
    ED='element-documentation'
    PP='properties-propertyDefinitionRef'
    PV='property-value'
    RI='relationships-identifier'
    RT='relationships-type'
    RN='relationship-name'
    RD='relationship-documentation'
    RS='relationships-source'
    RG='relationships-target'
    RA='relationships-accessType'
    VI='diagrams-identifier'
    VT='diagrams-type'
    VN='view-name'
    NI='view-identifier'
    NE='view-elementRef'
    NT='node-element'
    NL='node-label'


    @staticmethod
    def list():
        return list(map(lambda c: c.value, ToStore))


class XMLContent(object):
    def __init__(self, modelName: str) -> None:
        self.NODES = {NodeType.ELEMENT.value:  
            ('elements-element', #0 parenNode-node
                'element-name', #1
                'element-documentation', #2
                'element-properties', #3
                'properties-property', #4
                'property-value'),
            NodeType.RELATIONSSHIP.value:
            ('relationships-relationship', #0
                'relationship-name', #1
                'relationship-documentation', #2
                'relationship-properties' #3
                'properties-property', #4
                'property-value'),
            NodeType.VIEW.value:
            ('diagrams-view', #0
                'view-name', #1
                'view-node', #2
                'node-style', #3
                'style-fillColor', #4
                'style-lineColor', #5
                'style-font', #6
                'font-color', #7
                'node-label')
        }
        self.GETFROMTHESENODES = {NodeType.ELEMENT.value:
                                (ToGet.ATTR, #0
                            ToGet.DATA, #1
                            ToGet.DATA, #2
                            ToGet.NONE, #3  
                            ToGet.NONE, #4  # BEWARE that as an archimate's artefact can have several properties, the program is not able to handle that at the moment. I should add a beacon "is multiple" in the config.
                            ToGet.NONE),
                            NodeType.RELATIONSSHIP.value:
                            (ToGet.ATTR, #0
                            ToGet.DATA, # 1
                            ToGet.DATA, # 2
                            ToGet.NONE, #3
                            ToGet.NONE, #4
                            ToGet.NONE),
                            NodeType.VIEW.value:
                            (ToGet.ATTR,#0
                            ToGet.DATA, #1
                            ToGet.ATTR, #2
                            ToGet.NONE, #3
                            ToGet.NONE, #4
                            ToGet.NONE, #5
                            ToGet.NONE, #6
                            ToGet.NONE, #7
                            ToGet.DATA)
        }

        self.allObjects = {NodeType.ELEMENT.value: {
                                ToStore.EI.value: [],
                                ToStore.ET.value: [],
                                ToStore.EN.value: [],
                                ToStore.ED.value: [],
                                ToStore.PP.value: [],
                                ToStore.PV.value: []},
                            NodeType.RELATIONSSHIP.value: {
                                ToStore.RI.value: [],
                                ToStore.RT.value: [],
                                ToStore.RN.value: [],
                                ToStore.RD.value: [],
                                ToStore.PP.value: [],
                                ToStore.PV.value: [],
                                ToStore.RS.value: [],
                                ToStore.RG.value: [],
                                ToStore.RA.value: []},
                            NodeType.VIEW.value: {
                                ToStore.VI.value: [],
                                ToStore.VT.value: [],
                                ToStore.VN.value: [],
                                ToStore.NE.value: [],
                                ToStore.NI.value: [],
                                ToStore.NT.value: [],
                                ToStore.NL.value: []}
        }

        # holds value of the NodeType currently processed
        self.currentNodeType = None
        
        # to stop to process the model if any error occurs
        self.somethingWentWrong = False

        # to store the name of the Archi model 
        self.modelName = modelName
    
    def getNodes(self, key: NodeType) -> list:
        '''
        get all the nodes from one type listed in the enum NodeType
        '''
        try:
            return self.allObjects[key.value]
        except KeyError as e:
            return None

    def getAll(self) -> dict:
        '''
        get all the nodes all all the types listed in the enum NodeType
        '''

        return self.allObjects
