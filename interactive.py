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

from archi.lib import stringutil
v = [
'Access ID',
'ALERTING',
'APO',
'APS',
'APS ?',
'ASSESS GO',
'BOM mgr',
'BOM Mgr',
'COM',
'DPCP Dashboard',
'DPCP Portal',
'Forecast Collab',
'Integrator',
'INTEGRATOR',
'Order Collab',
'PLM',
'RFID',
'RFID order',
'RFQ',
'S/4',
'SAC',
'SHU',
'Stock collab',
'Stock Collab',
'WMS',
'?',
'?',
'APS',
'Linkeo',
'Order Collab',
'Order Collab & S/4',
'other modules',
'PLM',
'PLM &  Order Collab',
'PSV',
'RANK2',
'RFQ',
'S/4',
'S/4 & APS',
'S/4 & APS & SAC',
'S/4 & DPCP Dashboard',
'SAC',
'SHU',

]
r = []
for n in v:
    r.append(stringutil.cleanName(
                                                    n,
                                                    True,
                                                    True,
                                                    'lowercase',
                                                    True,
                                                    False,
                                                    True)
    )
splitted = []
for s in r:
    for a in s.split('&'):
        splitted.append(a)
    print 
print(splitted)
# %%
v = 'SAP ?'
from archi.lib import stringutil
vclean = stringutil.cleanName(
                                                    v,
                                                    True,
                                                    True,
                                                    'lowercase',
                                                    True,
                                                    False,
                                                    True)

l = vclean.split('?')
print(l)
# %%
from archi.lib import stringutil
v = '''
Id	Macro process	Function Future	Key word	Market ID	Sub Function List	Future Sub-function General Description	User story / Information	OP: Old  NP: New	Sub-funct Future Y/N/T/D/?	Suitability of the SI today	Collabor	Prod.com	LINK	APO	FMS	ECC	CAPE	Order Max	Rank 2	Assess GO	CPP	PSV	SNC	MOLDGO	Asset GO	PACE	Tactical S&OP	ETCO	link with tool	Others	Function Gap ( Based on the actual local projects, feedback and expectation from the users)	Pain solved	Target	Production Referencer	Order Manager	Stock Manager	CPT Quotation Manager	CPT Planner (MRP)	Alert Manager	Pre-invoice Manager	Mold	APO	ASSES GO	Expedition Preparation	BI	Authorisation manager	ADMIN Parameters	Other	CTR only one target tool	Tool proposal	Tool  proposal 2	IF S/4, manage in it ?	If not S/4 where ?	S/4 std level (S/P/E/D/A?)	Weigh	Cost if dev in prod.com	Needed S4/p/2	Comment	Open questions	Forcasted year	Target reached
'''
l = v.split()
for n in l:
    print(stringutil.cleanName(
                                                        v,
                                                        True,
                                                        True,
                                                        'lowercase',
                                                        True,
                                                        True,
                                                        True)
    )
# %%
v = 'R'
a = int(v)
print(isinstance(a, int))
# %%
import pyyed
l_alreadyAdded = []
g.write_graph(MAIN_FOLDER + os.path.sep + OUTPUT + os.path.sep + l_alreadyAdded[len(l_alreadyAdded)-1], pretty_print=True)
g = pyyed.Graph()
g.define_custom_property("node", "UseCase", "string", "")

# %%
l_alreadyAdded = [1, 2]
print(l_alreadyAdded[len(l_alreadyAdded)-1])
# %%
v = 'clode'
print(v[0:2])
# %%
l = ['a', 'b', 'c']
a, b, c = [l[i] for i in range(0, len(l))]
print(f'a={a}, b={b}, c={c}')
# %%
import archi.configfunctionlist as cfl
fltk = cfl.FunctionListToolkit()
def writelink(Level3ID: str, columnToLink: str, valueOfTheCell: str ) -> None:
    found = True
    try:
        match columnToLink.upper():
            case 'I':
                source = fltk.oldNewProcessAssessment[valueOfTheCell]
                destination = Level3ID
                linkType = cfl.ArchiConcepts.ASSOCIATIONRELATION.value
            case _:
                found = False
                print('this value is not configured')
    except KeyError:
        print('this value is not handled')
        found = False
    if found:
        print(f'source={source}, destination={destination}, linkType={linkType}')

column = 'i'
value = 'OP'
myprocess = 'level3process'
writelink(myprocess, column, value)
# %%
