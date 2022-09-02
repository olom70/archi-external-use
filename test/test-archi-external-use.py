# https://docs.python.org/3/library/xml.dom.html
# https://arun1729.github.io/cog/
import unittest
import os
import sys
import logging
import networkx as nx

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

import archi.tools as tools
import  archi.configarchi as conf

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
    content = tools.readModel(fileToRead)
    assert content.getAll()  is not None
    assert content.getNodes(conf.NodeType.ELEMENT)  is not None
    assert content.getNodes(conf.NodeType.RELATIONSSHIP)  is not None
    allContent = content.getAll()
    assert 'id-bc7db218fc4c42b88409118617393819' in allContent[conf.NodeType.ELEMENT.value][conf.ToStore.EI.value]

    modelAsGraph = tools.createGraph(content)
    assert nx.is_directed(modelAsGraph)
    name = nx.get_node_attributes(modelAsGraph, conf.ToStore.EN.value)
    assert name["id-e7ba459f108a4c62804e8e2ac83d25bd"] == 'A function'

    fh.close()
