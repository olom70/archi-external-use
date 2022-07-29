#%%
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

Nodes = ['element', 'name', 'documentation' 'relationship']
Attributes = [['identifier', 'xsi:type'], [], [], ['identifier', 'source', 'target']]
Value = [False, True, True, False]

with open('tinker.xml', encoding='utf-8') as xmltoanalyse:
    doc = minidom.parse(xmltoanalyse)

name = doc.getElementsByTagName("name")[0]
print(name.firstChild.data)

def printNode(node: Node):
    print(f'name : {node.tagName}, value : {node.firstChild.data}')

def printAttribute(node):
    print(f'name : {node.localName}, value : {node.value}')


def walk(listOfNodes):
    for child in listOfNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            printNode(child)
            if child.hasAttributes():
                if child.nodeName == 'element':
                    print(child.getAttribute('identifier'))

        if child.hasChildNodes():
            walk(child.childNodes)
        


walk(doc.getElementsByTagName("element"))

# elements = doc.getElementsByTagName("element")
# for element in elements:
#     print(f"id : {element.getAttribute('identifier')}, type {element.getAttribute('xsi:type')}")
#     name = element.getElementsByTagName("name")[0]
#     print(name.firstChild.data)
#     childs = element.childNodes
#     for child in childs:
#         if child.nodeType == Node.ELEMENT_NODE:
#             print(f'type : {child.nodeType}, {child.tagName}, {child.firstChild.data}')
    


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



