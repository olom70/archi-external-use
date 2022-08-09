#%%
from tkinter import Variable
from xml.dom import minidom, Node
from xml.dom.expatbuilder import TEXT_NODE
with open('tinker.xml', encoding='utf-8') as xmltoanalyse:
    dom = minidom.parse(xmltoanalyse)
model = dom.childNodes[0]
topnodes = model.childNodes
for a in topnodes:
    if a.nodeType == Node.TEXT_NODE:
        print("(textnode)" + a.nodeName)
        print(a.data)
    if a.nodeType == Node.ELEMENT_NODE:
        print('nodeName : ', a.nodeName)
        print('nodeValue : ', a.nodeValue)
        print('localName : ', a.localName)
        print('nodeType : ', a.nodeType)
        print('attributes : ', a.attributes)
        print(a.attributes.length)
        if a.attributes.length > 0:
            print("attribute :"+a.attributes.item(0).localName)

        for s in a.childNodes:
            if s.nodeType == Node.ELEMENT_NODE:
                print('s-nodeName : ', s.nodeName)
                if s.attributes.length > 0:
                    print(s.attributes.item(0).nodeName)
                    print(s.getAttribute('xsi:type'))
#%%
from xml.dom import minidom, Node
from enum import Enum
import  archi.configarchi as configarchi


NODES = (
            ('element', #1
                'name', #2
                'documentation', #3
                'propertyDefinitionRef', #4
                'name'),
            ('relationship', #1
                'name'),
)


GETFROMTHESENODES = (
                        ('attr', #1
                        'firstChild.data', #2
                        'firstChild.data', #3
                        'attr', #4
                        'firstChild.data'),
                        ('attr', #1
                        'firstChild.data')
)

PARENTSOFTHESENODES = (
                        ('elements', #1
                        'element', #2
                        'element', #3
                        'properties', #4
                        'property'),
                        ('relationships', #1
                        'relationship')
)

ATTRIBUTESOFTHESENODES = (
                            (['identifier', 'xsi:type'], #1
                            [], #2
                            [], #3
                            ['value'], #4
                            []),
                            (['identifier', 'source', 'target'], #1
                            [])
)


def printNode(node: Node):
    if node.hasChildNodes():
        print(f'parent : {node.parentNode.localName}, node name : {node.localName}, value : {node.firstChild.data}')

def printAttribute(node: Node):
    '''
    https://linux.die.net/diveintopython/html/xml_processing/attributes.html
    '''
    if node.hasAttributes():
        map = node.attributes
        for key in map.keys():
            print(f'node name : {node.localName}, attr name :  {map[key].localName}, value : {map[key].value}')


def processNode(node: Node, knownNodes: list):
    pass
    


with open('tinker.xml', encoding='utf-8') as xmltoanalyse:
    doc = minidom.parse(xmltoanalyse)

name = doc.getElementsByTagName("name")[0]
print(name.firstChild.data)


def walk(listOfNodes, knownNodes: list) -> None:
    '''
        get a list of Nodes and walk the tree of each element of that list

    '''
    for child in listOfNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            printNode(child)
            printAttribute(child)
        if child.hasChildNodes():
            walk(child.childNodes, knownNodes)
        


for e, i in zip(configarchi.NodeType, range(0, len(configarchi.NodeType))):
    walk(doc.getElementsByTagName(e.value), NODES[i])
    
    


#%%
from anytree import Node, RenderTree
import uuid
for n in range(10):
    print(uuid.uuid1())

ids = ['1-8fb02a8f-0d8f-11ed-b9ee-ac74b12a0cdc',
'2-8fb051a2-0d8f-11ed-81ae-ac74b12a0cdc',
'3-8fb051a3-0d8f-11ed-b075-ac74b12a0cdc',
'4-8fb051a4-0d8f-11ed-bb89-ac74b12a0cdc',
'5-8fb051a5-0d8f-11ed-aad7-ac74b12a0cdc',
'6-8fb051a6-0d8f-11ed-9185-ac74b12a0cdc',
'7-8fb051a7-0d8f-11ed-be2c-ac74b12a0cdc',
'8-8fb051a8-0d8f-11ed-910f-ac74b12a0cdc',
'9-8fb051a9-0d8f-11ed-960b-ac74b12a0cdc',
'0-8fb051aa-0d8f-11ed-811a-ac74b12a0cdc']
my_data = {}
my_data[ids[0]] = Node(ids[0])
my_data[ids[1]] = Node(ids[1], parent=my_data[ids[0]])
for pre, fill, node in RenderTree(my_data[ids[0]]):
    print("%s%s" % (pre, node.name))

#%%
from cog.torque import Graph
from cog import config

conf.COG_HOME="archi_external-use"
conf.COG_PATH_PREFIX="."

g = Graph("cool")


g.put("alice","composed of","bob")
g.put("bob","composed of","fred")
g.put("bob","status","cool_person")
g.put("charlie","serves","bob")
g.put("charlie","composed of","dani")
g.put("dani","follows","bob")
g.put("dani","follows","greg")
g.put("dani","status","cool_person")
g.put("emily","composed of","fred")
g.put("fred","follows","greg")
g.put("greg","status","cool_person")
g.put("bob","score","5")
g.put("greg","score","10")
g.put("alice","score","7")
g.put("dani","score","100")


g.v("bob").tag("from").out(["status", "composed of"]).tag("to").view(["status", "composed of"]).render()
# g.v().has("status", 'cool_person').all()
# g.v().has("follows", "fred").inc().all('e')
#g.v("alice").out().count()
g.v("bob").tag("from").out(["status", "composed of"]).tag("to").view(["status", "composed of"])
g.v("bob").tag("from").out(["status", "composed of"]).tag("to").all('e')


#%%
NODES = (
            ('element', #1
                'name', #2
                'documentation', #3
                'propertyDefinitionRef', #4
                'name'),
            ('relationship', #1
                'name'),
)

t = NODES[0]
print(t)
#%%
import archi.configarchi as conf
from archi.configarchi import KnownContent

for i in conf.NodeType:
    print(i.value)

print(len(conf.NodeType))
print(len(NODES))

a = KnownContent()

print(a.NODES)
#%%

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

allObjects = {NodeType.ELEMENT: [
                                [ToStore.ID],
                                [ToStore.TYPE],
                                ['element-name.value'],
                                ['element-documentation.value'],
                                [{ToStore.PROPERTY: 'propertie.name.value'}]
                            ],
                            NodeType.RELATIONSSHIP: [
                                [ToStore.ID],
                                [ToStore.TYPE],
                                ['relationship-name.value'],
                                ['relationship-documentation.value'],
                                [{ToStore.PROPERTY: 'propertie.name.value'}],
                                [ToStore.SOURCE],
                                [ToStore.TARGET]

                            ]
        }

print(allObjects)
allObjects[NodeType.ELEMENT.ELEMENT][0].append('****+++****')
print(allObjects)
#%%
node = 'name'
parent = 'property'
match (node, parent):
    case ('element', 'elements'):
        print('element')
    case ['name', ('property', 'element')]:
        print('property')
#%%
class ToStore(Enum):
    '''
    list the names of the attributtes or the name of the tag we want to collect for each node
    '''
    ID = 'identifier'
    TYPE = 'xsi:type'
    NAME = 'name'
    DOCUMENTATION = 'documentation'
    # VALUE = 'value'
    SOURCE = 'source'
    TARGET = 'target'
    PROPERTY = 'propertyDefinitionRef'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ToStore))

key = 'identifier'
if key in list(ToStore.list()):
    print('Found')
print(list(ToStore))


def getNodes(key: ToStore) -> list:
    '''
    get all the nodes from one type listed in the enum NodeType
    '''
    print(key.value)

getNodes(ToStore.ID)
#%%
from enum import IntEnum, Enum
class ToStore(Enum):
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

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ToStore))


class NodeType(Enum):
    '''
    list the nodes type to parse in the Archi file
    '''
    ELEMENT = 'element'
    RELATIONSSHIP = 'relationship'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, NodeType))


allObjects1 = {NodeType.ELEMENT.value: {
                        ToStore.EI.value: [ToStore.EI.value],
                        ToStore.ET.value: [ToStore.ET.value],
                        ToStore.EN.value: [ToStore.EN.value],
                        ToStore.ED.value: [ToStore.ED.value],
                        ToStore.PP.value: [ToStore.PP.value],
                        ToStore.PV.value: [ToStore.PV.value]
},
                    NodeType.RELATIONSSHIP.value: {
                        ToStore.RI.value: [ToStore.RI.value],
                        ToStore.RT.value: [ToStore.RT.value],
                        ToStore.RN.value: [ToStore.RN.value],
                        ToStore.RD.value: [ToStore.RD.value],
                        ToStore.PP.value: [ToStore.PP.value],
                        ToStore.PV.value: [ToStore.PV.value],
                        ToStore.RS.value: [ToStore.RS.value],
                        ToStore.RG.value: [ToStore.RG.value],
                        ToStore.RA.value: [ToStore.RA.value]
                    }
}

v = 'elements-identifier'
print(allObjects1[NodeType.ELEMENT.value][v]) 
allObjects1[NodeType.ELEMENT.value][v].append('x')
print(allObjects1[NodeType.ELEMENT.value][v]) 