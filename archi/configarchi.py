from enum import IntEnum, Enum

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
    NONE = None

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ToGet))


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
                'property-value')
        }
        self.GETFROMTHESENODES = {NodeType.ELEMENT.value:
                                (ToGet.ATTR, #0
                            ToGet.DATA, #1
                            ToGet.DATA, #2
                            ToGet.NONE, #3
                            ToGet.ATTR, #4
                            ToGet.DATA),
                            NodeType.RELATIONSSHIP.value:
                            (ToGet.ATTR, #0
                            ToGet.DATA, # 1
                            ToGet.DATA, # 2
                            ToGet.NONE, #3
                            ToGet.ATTR, #4
                            ToGet.DATA)
        }

        self.PARENTSOFTHESENODES = {NodeType.ELEMENT.value:
                                ('elements', #0
                                'element', #1
                                'element', #2
                                'element', #3
                                'properties', #4
                                'property'),
                                NodeType.RELATIONSSHIP.value:
                                ('relationships', #0
                                'relationship', #1
                                'relationship', #2
                                'relationship', #3
                                'properties', #4
                                'property')
        }

        self.TOSTORE = {NodeType.ELEMENT.value:
                                    ('elements-identifier' , #0 parentNode-attributename
                                    'elements-type', #1 parentNode-attributename
                                    'element-name', #2 parentNode-node
                                    'element-documentation', #3 parentNode-node
                                    'properties-propertyDefinitionRef', #4 parentNode-node
                                    'property-value'), #5 parentNode-attributename
                                    NodeType.RELATIONSSHIP.value:
                                    ('relationships-identifier' , #0 parentNode-attributename
                                    'relationships-type', #1 parentNode-attributename
                                    'relationship-name', #2 parentNode-node
                                    'relationship-documentation', #3 parentNode-node
                                    'properties-propertyDefinitionRef', #4 parentNode-attributename
                                    'property-value', #5 parentNode-node
                                    'relationships-source', #6 parentNode-attributename
                                    'relationships-target', #7 parentNode-attributename
                                    'relationships-accessType') #7 parentNode-attributename
        }
  
        # allObjects holds everything. See documentation below
        self.allObjects = {NodeType.ELEMENT.value: [
                                ['elements-identifier'],
                                ['elements-type'],
                                ['element-name'],
                                ['element-documentation'],
                                ['propertie-propertyDefinitionRefs'],
                                ['property-value']
                            ],
                            NodeType.RELATIONSSHIP.value: [
                                ['relationships-identifier'],
                                ['relationships-type'],
                                ['relationship-name'],
                                ['relationships-documentation'],
                                ['propertie-propertyDefinitionRefs'],
                                ['property-value'],
                                ['relationships-source'],
                                ['relationships-target'],
                                ['relationships-accessType']

                            ]
        }
        
        # holds value of the NodeTpe currently processed
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

        if len(self.allObjects) > 0:
            return self.allObjects
        else:
            return None