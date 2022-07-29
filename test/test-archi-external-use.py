# https://docs.python.org/3/library/xml.dom.html
# https://arun1729.github.io/cog/
import os
import sys
import logging


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)

import archi.tools as tools

logger = logging.getLogger('test-archi-external-use')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('test-archi-external-use.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)



def main():
    logger.info('Start. Application is initializing')


    elements = []
    elementsNames = []
    elementsDocumentation = []
    elementsProperties = []
    fileToRead = "..\tinker.xml"

    elements, elementsNames, elementsDocumentation, elementsProperties = tools.read_model(fileToRead)
    assert elements is not None



if __name__ == '__main__':

    main()