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
node = 'name'
parent = 'property'
match (node, parent):
    case ('element', 'elements'):
        print('element')
    case ['name', ('property', 'element')]:
        print('property')

#%%

#%%
import networkx as nx
MDG = nx.MultiDiGraph()
nodes = [('id5', {"name":"yes"}), 'id2', 'id3', 'id4', 'id1', 'id0']
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

nx.write_graphml(MDG, 'modelasgraph.graphml', edge_id_from_attribute="name")

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
nx.write_graphml(modelAsGraph, 'modelasgraph.graphml')
# %%
