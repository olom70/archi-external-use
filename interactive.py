#%%
from re import L
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

config.COG_HOME="archi_external-use"
config.COG_PATH_PREFIX="."

g = Graph("cool")


g.put("alice","composedof","bob")
g.put("bob","composedof","fred")
g.put("bob","status","cool_person")
g.put("charlie","serves","bob")
g.put("bob","composedof","dani")
g.put("dani","follows","bob")
g.put("dani","follows","greg")
g.put("dani","status","cool_person")
g.put("emily","composedof","fred")
g.put("fred","composedof","greg")
g.put("greg","status","cool_person")
g.put("bob","score","5")
g.put("greg","score","10")
g.put("alice","score","7")
g.put("dani","score","100")


#g.v().has("composed of", "fred").all()
#g.getv("follows").render()
#g.v().inc(["composedof"]).view(['composedof']).render()
g.v("bob").tag("part of").out(["composedof"]).all()
# g.v().has("status", 'cool_person').all()
# g.v().has("follows", "fred").inc().all('e')
#g.v("alice").out().count()
#g.v("bob").tag("from").out(["status", "composed of"]).tag("to").view(["status", "composed of"]).all()
#g.v("bob").tag("from").out(["status", "composed of"]).tag("to").all('e')
#g.v("bob").tag("from").out(["composed of"]).tag("to").all('e')

#g.v("bob").out().all()
#g.v("bob").tag("from").out("composed of").tag("to").all()
#g.v("bob").out().all()
#g.v("bob").out().count()
#g.scan(scan_type='v')
#g.v("bob").out("composed of").tag("from").out("composed of").tag("to").all()
#g.v().tag("from").out("composed of").tag("to").view("composed of").render()
#g.v("bob").out().tag("from").out().tag("to").all()
#g.v().has("composed of", "fred").inc().all('e')


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
#%%
import networkx as nx
MDG = nx.MultiDiGraph()
nodes = ['id5', 'id2', 'id3', 'id4', 'id1', 'id0']
MDG.add_nodes_from(nodes)
edges = [('id1', 'id2', {"composed of": "name12"}),
         ("id1", "id6", {"composed of": "name23"}),
         ("id2", "id3", {"composed of": "name23"}),
         ("id3", "id4", {"composed of": "name34"}),
         ("id3", "id4", {"aggregates": "name34a"}),
         ("id4", "id5", {"aggregates": "name45"}),
         ("id0", "id2", {"aggregates": "name45"})
        ]
MDG.add_edges_from(edges)


def walkgraph(MDG: nx.MultiDiGraph,  current_node: list, already_met: list) -> None:

    def continue_walk(e: dict) -> bool:
        print("inside continue")
        for v, k in e.items():
            print(f' dictionary : {k}')
            if ("composed of" in k):
                print('return true')
                return True

    print(f'current_node : {current_node}')
    print(f'all edges {nx.edges(MDG, current_node)}')
    nextNodes = []
    if len(nx.edges(MDG, current_node)) > 0:
        for e in nx.edges(MDG, current_node):
            print(f"edges : {e}")
            print(f"list of edges {MDG.adj[e[0]][e[1]]}")
            continue_walk(MDG.adj[e[0]][e[1]])
            try:
                i = nextNodes.index(e[1])
            except ValueError:
                nextNodes.append(e[1])
            print(f'nextnodes : {nextNodes}')
            continue_walk(MDG.adj[e[0]][e[1]])
        walkgraph(MDG, nextNodes, already_met)           



start = "id1"

walkgraph(MDG, start, [])

print(list(MDG.nodes))

print(list(nx.topological_sort(MDG)))

top = [n for n,d in MDG.in_degree() if d==0]
print(top)
print(MDG.out_degree(top))
# %%

#%%

import logging

import archi.parsexml as parsexml
import archi.creategraphs as creategraphs
import archi.configarchi as conf
import networkx as nx
logger = logging.getLogger('archi-external-use')
logger.setLevel(logging.WARNING)
fh = logging.FileHandler(filename='test-archi-external-use.log')
fh.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.info('Start. Application is initializing')

fileToRead = 'VC.xml'
content = parsexml.readModel(fileToRead)
modelAsGraph = creategraphs.createGraph(content)
listOfIsolatedNodes = [n for n,d in modelAsGraph.degree() if d==0]
name = nx.get_node_attributes(modelAsGraph, conf.ToStore.EN.value)
type = nx.get_node_attributes(modelAsGraph, conf.ToStore.ET.value)
for isolatedNode in listOfIsolatedNodes:
    print(f'id : {isolatedNode}, name : {name[isolatedNode]}, type : {type[isolatedNode]} ')

# %%
