#%%
import xml.etree.ElementTree as ET
with open('tinker.xml', encoding='utf-8') as xmltoanalyse:
    data = xmltoanalyse.read()
    # is it an xml file ?
    if data[0:5] == '<?xml':
        root = ET.fromstring(data)
        # for myelement in root:
        #     print(myelement.tag)
        for e in root.iter("{http://www.opengroup.org/xsd/archimate/3.0/}element"):
            print(e.items())
            myname = e.findall("{http://www.opengroup.org/xsd/archimate/3.0/}name")
            print(myname)
#%%
from xml.dom import minidom
with open('tinker.xml', encoding='utf-8') as xmltoanalyse:
    dom = minidom.parse(xmltoanalyse)
model = dom.childNodes[0]
topnodes = model.childNodes
for a in topnodes:
    if a.nodeType == 1:
        print('nodeName : ', a.nodeName)
        print('nodeValue : ', a.nodeValue)
        print('localName : ', a.localName)
        print('nodeType : ', a.nodeType)
        print('attributes : ', a.attributes)
        print(a.attributes.length)
        if a.attributes.length > 0:
            print(a.attributes.item(0).nodeName)

        for s in a.childNodes:
            if s.nodeType == 1:
                print('s-nodeName : ', s.nodeName)
                if s.attributes.length > 0:
                    print(s.attributes.item(0).nodeName)
                    print(s.getAttribute('xsi:type'))
