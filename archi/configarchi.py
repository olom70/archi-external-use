from enum import IntEnum, Enum

class ElAttr(IntEnum):
    '''
    List if all the known atributes for the Nodes of type 'element'
    '''
    ID = 0
    TYPE = 1
    NAME = 2
    DOCUMENTATION = 3
    PROPERTIES = 4

class RelAttr(IntEnum):
    '''
    List if all the known atributes for the Nodes of type 'relationship'
    '''
    ID = 0
    TYPE = 1
    NAME = 2
    DOCUMENTATION = 3
    PROPERTIES = 4
    SOURCE = 5
    TARGET = 7

class NodeType(Enum):
    '''
    list the nodes type to parse in the Archi file
    '''
    ELEMENT = 'element'
    RELATIONSSHIP = 'relationship'

class ToGet(Enum):
    '''
    ATTR to get the attributes of the node
    DATA to get the value
    '''
    ATTR = 'attr'
    DATA = 'firstChild.data'

class ToStore(Enum):
    '''
    list the names of the attributtes or the name of the tag we want to collect for each node
    '''
    ID = 'identifier'
    TYPE = 'xsi:type'
    VALUE = 'value'
    SOURCE = 'source'
    TARGET = 'target'
    PROPERTY = 'propertyDefinitionRef'

class XMLContent(object):
    def __init__(self, modelName: str) -> None:
        self.NODES = {NodeType.ELEMENT.value:
            ('element', #1
                'name', #2
                'documentation', #3
                'propertie', #4
                'name'),
            NodeType.RELATIONSSHIP.value:
            ('relationship', #1
                'name', #2
                'documentation', #3
                'propertie', #4
                'name')
        }
        self.GETFROMTHESENODES = {NodeType.ELEMENT.value:
                            (ToGet.ATTR.value, #1
                            ToGet.DATA.value, #2
                            ToGet.DATA.value, #3
                            ToGet.ATTR.value, #4
                            ToGet.DATA.value),
                            NodeType.RELATIONSSHIP.value:
                            (ToGet.ATTR.value, #1
                            ToGet.DATA.value, #3
                            ToGet.ATTR.value, #4
                            ToGet.DATA.value)

        }

        self.PARENTSOFTHESENODES = {NodeType.ELEMENT.value:
                                ('elements', #1
                                'element', #2
                                'element', #3
                                'properties', #4
                                'property'),
                                NodeType.RELATIONSSHIP.value:
                                ('relationships', #1
                                'relationship',
                                'relationship'
                                'properties',
                                'property'
                                )
        }

        self.ATTRIBUTESOFTHESENODES = {NodeType.ELEMENT.value:
                                    ([ToStore.ID, ToStore.TYPE], #1
                                    [ToStore.VALUE], #2
                                    [ToStore.VALUE], #3
                                    [ToStore.PROPERTY], #4
                                    [ToStore.VALUE]),
                                    NodeType.RELATIONSSHIP.value:
                                    ([ToStore.ID, ToStore.TYPE,ToStore.SOURCE, ToStore.TARGET], #1
                                    [ToStore.VALUE], #2
                                    [ToStore.VALUE], #3
                                    [ToStore.PROPERTY], #4
                                    [ToStore.VALUE])
        }
  

        # allObjects holds everything. See documentation below
        self.allObjects = {NodeType.ELEMENT.value: [
                                [ToStore.ID],
                                [ToStore.TYPE],
                                ['element-name.value'],
                                ['element-documentation.value'],
                                [{ToStore.PROPERTY: 'propertie.name.value'}]
                            ],
                            NodeType.RELATIONSSHIP.value: [
                                [ToStore.ID],
                                [ToStore.TYPE],
                                ['relationship-name.value'],
                                ['relationship-documentation.value'],
                                [{ToStore.PROPERTY: 'propertie.name.value'}],
                                [ToStore.SOURCE],
                                [ToStore.TARGET]

                            ]
        }
        
        # holds value of the NodeTpe currently processed
        self.currentNodeType = None
        
        # to stop to process the model if any error occurs
        self.somethingWentWrong = False

        # to store the name of the Archi model 
        self.modelName = modelName
    
    def getNodes(self, key: str) -> list:
        '''
        get all the nodes from one the type listed in the enum NodeType
        '''
        try:
            return self.allObjects[str]
        except KeyError as e:
            return None

    def getAll(self) -> dict:
        '''
        get all the nodes all all the types listed in the enum NodeType
        '''

        if len(self.allObjects) > 0:
            return self.allObjects
        else:
            return None

    def documentation() -> str:
        d = ''' 
            Bellow are presented the structures that holds the archi model.

            properties = [
                {'propertyDefinitionRef1.value': 'propertyDefinitionRef_name.value1',
                ''propertyDefinitionRef1.value': 'propertyDefinitionRef_name.value1''
                }
            ]

            elements = [
                ['element.ToStore.ID', 'element.ToStore.ID2', 'element.ToStore.ID3'],
                ['element.ToStore.TYPE', 'element.xsi:type2', 'element.xsi:type'],
                ['elementName.value', 'elementName.value', 'elementName.value'],
                ['documentation_name.value', 'documentation_name.value', 'documentation_name.value'],
                ['[properties1]', '[properties2]', '[properties3]']
            ]

            relationsships = [
                ['element.ToStore.ID', 'element.ToStore.ID2', 'element.ToStore.ID3'],
                ['element.ToStore.TYPE', 'element.xsi:type2', 'element.xsi:type'],
                ['elementName.value', 'elementName.value', 'elementName.value'],
                ['documentation_name.value', 'documentation_name.value', 'documentation_name.value'],
                ['[properties1]', '[properties2]', '[properties3]'],
                ['source1', 'source2', 'source3'],
                ['target1', 'target2', 'target3']
            ]

            allObjects = {
                NodeType.ELEMENT : [],
                NodeType.RELATIONSSHIPS : []
            }

            End of the documentation on the structures
            '''
        return d