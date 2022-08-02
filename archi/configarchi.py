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
    RELATIONSSHIPS = 'relationship'

class ToGet(Enum):
    ATTR = 'attr'
    DATA = 'firstChild.data'

class XMLContent(object):
    def __init__(self, modelName: str) -> None:
        self.NODES = (
            ('element', #1
                'name', #2
                'documentation', #3
                'propertyDefinitionRef', #4
                'name'),
            ('relationship', #1
                'name'),
        )
        self.GETFROMTHESENODES = (
                            (ToGet.ATTR.value, #1
                            ToGet.DATA.value, #2
                            ToGet.DATA.value, #3
                            ToGet.ATTR.value, #4
                            ToGet.DATA.value),
                            (ToGet.ATTR.value, #1
                            ToGet.DATA.value)
        )

        self.PARENTSOFTHESENODES = (
                                ('elements', #1
                                'element', #2
                                'element', #3
                                'properties', #4
                                'property'),
                                ('relationships', #1
                                'relationship')
        )

        self.ATTRIBUTESOFTHESENODES = (
                                    (['identifier', 'xsi:type'], #1
                                    [], #2
                                    [], #3
                                    ['value'], #4
                                    []),
                                    (['identifier', 'source', 'target'], #1
                                    [])
        )

        # allObjects holds everything. See documentation below
        self.allObjects = {}
        # holds the indice to use to access the lists inside the variable self.NODES
        self.indice = None
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
                {'property1': 'value1',
                'property2':'value2'
                }
            ]

            elements = [
                ['id', 'id2', 'id3'],
                ['type', 'type2', 'type'],
                ['name1', 'name2', 'name3'],
                ['documentation1', 'documentation2', 'documentation3'],
                ['[properties1]', '[properties2]', '[properties3]']
            ]

            relationsships = [
                ['id', 'id2', 'id3'],
                ['type', 'type2', 'type'],
                ['name1', 'name2', 'name3'],
                ['documentation1', 'documentation2', 'documentation3'],
                ['[properties1]', '[properties2]', '[properties3]']
                ['source1', 'source2', 'source3']
                ['target1', 'target2', 'target3']
            ]

            allObjects = {
                [NodeType.ELEMENT]
                [NodeType.RELATIONSSHIPS]
            }

            End of the documentation on the structures
            '''
        return d