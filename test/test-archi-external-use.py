# https://docs.python.org/3/library/xml.dom.html
# https://arun1729.github.io/cog/
from typing import List
import unittest
import os
import sys
import logging
import networkx as nx


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

import archi.parsexml as parsexml
import archi.creategraphs as creategraphs
import archi.configarchi as conf
import archi.exploitgrpah as exploitgraph

if __name__ == '__main__':

    logger = logging.getLogger('test-archi-external-use')
    logger.setLevel(logging.WARNING)
    fh = logging.FileHandler(filename='test-archi-external-use.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info('Start. Application is initializing')

    fileToRead = 'tinker.xml'
    
    content = parsexml.readModel(fileToRead)
    assert content.getAll()  is not None
    assert content.getNodes(conf.NodeType.ELEMENT)  is not None
    assert content.getNodes(conf.NodeType.RELATIONSSHIP)  is not None
    
    allContent = content.getAll()
    assert 'id-bc7db218fc4c42b88409118617393819' in allContent[conf.NodeType.ELEMENT.value][conf.ToStore.EI.value]
    assert allContent[conf.NodeType.VIEW.value]['id-2683cb1d748a40148dba0ca693063c60'][0] == 'application layer'
    assert allContent[conf.NodeType.VIEW.value]['id-2683cb1d748a40148dba0ca693063c60'][1][0] == 'id-e7ba459f108a4c62804e8e2ac83d25bd'
    assert allContent[conf.NodeType.VIEW.value]['id-2683cb1d748a40148dba0ca693063c60'][2][0] == 'id-23a7d1fa38a94c698f5295ebaee087c7'
    assert allContent[conf.NodeType.VIEW.value]['id-14c9a667d06949e49b10686750cf5cac'][2][0] == 'id-afea383831d546909ccd4235087de2af'
    
    modelAsGraph = creategraphs.createGraph(content)
    assert nx.is_directed(modelAsGraph)
    name = nx.get_node_attributes(modelAsGraph, conf.ToStore.EN.value)
    assert name["id-e7ba459f108a4c62804e8e2ac83d25bd"] == 'A function'

    viewIdentifier = 'id-14c9a667d06949e49b10686750cf5cac'
    viewAsGraph = creategraphs.createGraphView(viewIdentifier, content)
    name = nx.get_node_attributes(viewAsGraph, conf.ToStore.EN.value)
    assert name['id-2652f6a8ea82422f914026fd17b39331'] == 'Support'
    assert len(viewAsGraph.get_edge_data('id-2652f6a8ea82422f914026fd17b39331', 'id-5c93f97b4b684599add997942e49fb7f')) > 0
    assert len(viewAsGraph.get_edge_data('id-3842a16dac924661b4ef18fbb0231be9', 'id-0760dabecdff4cf092beeb6a009ba38b')) > 0
    
    viewIdentifier = 'id-2683cb1d748a40148dba0ca693063c60'
    viewAsGraph = creategraphs.createGraphView(viewIdentifier, content)
    assert len(viewAsGraph.get_edge_data('id-e7ba459f108a4c62804e8e2ac83d25bd', 'id-bc7db218fc4c42b88409118617393819')) > 0
    
    viewIdentifier = 'id-14c9a667d06949e49b10686750cf5cac'
    viewAsGraph = creategraphs.createGraphView(viewIdentifier, content)
    lists = exploitgraph.prepareBusinessCapabilitiesTreemap(viewAsGraph,)
    assert len(lists.parents) > 0
    assert len(lists.names) > 0
    assert len (lists.levels) > 0
    assert len(lists.textsinfo) > 0



    fh.close()
