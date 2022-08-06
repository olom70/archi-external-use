# https://docs.python.org/3/library/xml.dom.html
# https://arun1729.github.io/cog/
import unittest
import os
import sys
import logging


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

import archi.tools as tools
import  archi.configarchi as conf

logger = logging.getLogger('test-archi-external-use')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('test-archi-external-use.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)



def main():
    logger.info('Start. Application is initializing')
    fileToRead = 'tinker.xml'

    content = tools.readModel(fileToRead)
    assert content.getAll()  is not None
    assert content.getNodes(conf.NodeType.ELEMENT)  is not None
    assert content.getNodes(conf.NodeType.RELATIONSSHIP)  is not None
    allContent = content.getAll()
    assert 'id-1d4cb2202a604caa880e9e2f42df8996' in allContent[conf.NodeType.ELEMENT.value][conf.Position.ID.value]
    indice = allContent[conf.NodeType.ELEMENT.value][conf.Position.ID.value].index('id-1d4cb2202a604caa880e9e2f42df8996')
    assert allContent[conf.NodeType.ELEMENT.value][conf.Position.TYPE.value][indice] == 'ApplicationComponent'



if __name__ == '__main__':

    main()