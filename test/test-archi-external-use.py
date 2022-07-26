# https://docs.python.org/3/library/xml.dom.html
# https://arun1729.github.io/cog/
import os
import sys
import logging
import networkx as nx


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

import archi.parsexml as parsexml
import archi.creategraphs as creategraphs
import archi.configarchi as conf
import archi.exploitgraph as exploitgraph

if __name__ == '__main__':

    logger = logging.getLogger('archi-external-use')
    logger.setLevel(logging.WARNING)
    fh = logging.FileHandler(filename='test-archi-external-use.log')
    fh.setLevel(logging.WARNING)
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
    assert 'id-e6f02aa2c3cc491285e8cb17fe91493e' in allContent[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RI.value] #relationship beween to groups
    i = allContent[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RI.value].index('id-e6f02aa2c3cc491285e8cb17fe91493e')
    assert allContent[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RS.value][i] == 'id-5c93f97b4b684599add997942e49fb7f' # source and destination exists
    assert allContent[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RG.value][i] == 'id-f180722b19304db18ac623c0e8957d5e'
    
    assert allContent[conf.NodeType.VIEW.value]['id-2683cb1d748a40148dba0ca693063c60'][0] == 'application layer'
    assert allContent[conf.NodeType.VIEW.value]['id-2683cb1d748a40148dba0ca693063c60'][1][0] == 'id-e7ba459f108a4c62804e8e2ac83d25bd'
    assert allContent[conf.NodeType.VIEW.value]['id-2683cb1d748a40148dba0ca693063c60'][2][0] == 'id-23a7d1fa38a94c698f5295ebaee087c7'
    assert allContent[conf.NodeType.VIEW.value]['id-14c9a667d06949e49b10686750cf5cac'][2][0] == 'id-afea383831d546909ccd4235087de2af'

    assert allContent[conf.NodeType.VIEW.value]['id-14c9a667d06949e49b10686750cf5cac'][0] == 'POS complet'
    assert 'id-e6f02aa2c3cc491285e8cb17fe91493e' in allContent[conf.NodeType.VIEW.value]['id-14c9a667d06949e49b10686750cf5cac'][2]
    
    
    
    
    modelAsGraph = creategraphs.createGraph(content)
    assert nx.is_directed(modelAsGraph)
    name = nx.get_node_attributes(modelAsGraph, conf.ToStore.EN.value)
    assert name["id-e7ba459f108a4c62804e8e2ac83d25bd"] == 'A function'
    assert len(modelAsGraph.get_edge_data('id-5c93f97b4b684599add997942e49fb7f', 'id-f180722b19304db18ac623c0e8957d5e')) > 0 #source and destination exists


    viewIdentifier = 'id-14c9a667d06949e49b10686750cf5cac'
    viewAsGraph = creategraphs.createGraphView(viewIdentifier, content)
    name = nx.get_node_attributes(viewAsGraph, conf.ToStore.EN.value)
    assert name['id-2652f6a8ea82422f914026fd17b39331'] == 'Support'
    assert len(viewAsGraph.get_edge_data('id-2652f6a8ea82422f914026fd17b39331', 'id-5c93f97b4b684599add997942e49fb7f')) > 0
    assert len(viewAsGraph.get_edge_data('id-3842a16dac924661b4ef18fbb0231be9', 'id-0760dabecdff4cf092beeb6a009ba38b')) > 0
    assert len(viewAsGraph.get_edge_data('id-2652f6a8ea82422f914026fd17b39331', 'id-5c93f97b4b684599add997942e49fb7f')) > 0
    assert len(viewAsGraph.get_edge_data('id-5c93f97b4b684599add997942e49fb7f', 'id-f180722b19304db18ac623c0e8957d5e')) > 0
    assert len(viewAsGraph.get_edge_data('id-8854ca01fd1146e487af84fe653c5246', 'id-3e37f7b0410d4461980c23e53803d625')) > 0
    assert len(viewAsGraph.get_edge_data('id-14d9c024b6a842a488b33acc328ce2ef', 'id-9e3511f76bb242509f012326bbb40d61')) > 0
    assert len(viewAsGraph.get_edge_data('id-14d9c024b6a842a488b33acc328ce2ef', 'id-d4a3e9b92105486c91587e997ec9dddc')) > 0
    assert len(viewAsGraph.get_edge_data('id-14d9c024b6a842a488b33acc328ce2ef', 'id-a441c73a938048e1aa7f21f0f80bfa55')) > 0
    assert len(viewAsGraph.get_edge_data('id-997ec223b7b04de383f7215d4d5defd0', 'id-9b3830c7fc1541d795e0b52278574211')) > 0
    assert len(viewAsGraph.get_edge_data('id-9b3830c7fc1541d795e0b52278574211', 'id-2df0ee12df0f4251bfea1a01084dc81a')) > 0
    assert len(viewAsGraph.get_edge_data('id-2df0ee12df0f4251bfea1a01084dc81a', 'id-64c316b0b70b4a71944489000741a26c')) > 0
    assert len(viewAsGraph.get_edge_data('id-2df0ee12df0f4251bfea1a01084dc81a', 'id-e3912480a0e046178e216650a29ac8d5')) > 0

    lists: conf.Lists
    lists = exploitgraph.prepareBusinessCapabilitiesTreemap(viewAsGraph)
    assert len(lists.parents) > 0
    assert len(lists.names) > 0
    assert len (lists.levels) > 0
    assert len(lists.textsinfo) > 0

    fh.close()
