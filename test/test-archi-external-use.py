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

    xmlContent = tools.readModel(fileToRead)
    assert xmlContent.getAll()  is not None
    assert xmlContent.getNodes(conf.NodeType.ELEMENT.value)  is not None
    assert xmlContent.getNodes(conf.NodeType.RELATIONSSHIPS.value)  is not None
    allContent = xmlContent.getAll()
    assert 'id-1d4cb2202a604caa880e9e2f42df8996' in allContent[conf.NodeType.ELEMENT.value][conf.ElAttr.ID.value]
    indice = allContent[conf.NodeType.ELEMENT.value][conf.ElAttr.ID.value].index('id-1d4cb2202a604caa880e9e2f42df8996')
    assert allContent[conf.NodeType.ELEMENT.value][conf.ElAttr.TYPE.value][indice] == 'ApplicationComponent'



if __name__ == '__main__':

    main()