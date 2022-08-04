import os
import logging
import functools
from xml.dom import minidom, Node
import archi.configarchi as conf

mlogger = logging.getLogger('archi-external-use.tools')

def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        mlogger.info(f'Start of the function {func.__name__}')
        response = func(*args, **kwargs)
        mlogger.info(f'End of the function {func.__name__}')
        return response
    return wrapper

def processNodeAttributes(node: Node, content: conf.XMLContent) -> None:
    mlogger.debug(f'function processNodeAttributes() : node received {node.localName}')
    if node.hasAttributes():
        i = content.NODES[content.currentNodeType].index(node.localName)
        map = node.attributes
        for key in map.keys():
            if map[key].localName in content.ToStore:
                mlogger.debug(f'parent of the node : {node.parentNode.localName}, attr name :  {map[key].localName}, value : {map[key].value}')
                match key:
                    case conf.ToStore.ID:
                        content.allObjects[content.currentNodeType][0].append(map[key].value)
                    case conf.ToStore.TYPE:
                        content.allObjects[content.currentNodeType][1].append(map[key].value)
                    case conf.ToStore.SOURCE:
                        content.allObjects[content.currentNodeType][5].append(map[key].value)
                    case conf.ToStore.TARGET:
                        content.allObjects[content.currentNodeType][6].append(map[key].value)
                    case conf.ToStore.PROPERTY:
                        content.allObjects[content.currentNodeType][4][map[key].value] == ''

            else:
                mlogger.warning(f'this attribute is unknown : {map[key].localName}, add it in ATTRIBUTESOFTHENODES in order to process it.')
    else:
        content.somethingWentWrong == True
        mlogger.warning(f'node : {node.localName} has no attributes even tough the configuration says otherwise. check GETFROMTHODES')


def processNodeValue(node: Node, content: conf.XMLContent) -> None:
    mlogger.debug(f'function processNodeValue() : node received {node.localName}')
    if node.hasChildNodes():
        print(f'parent : {node.parentNode.localName}, node name : {node.localName}, value : {node.firstChild.data}')
    else:
        content.somethingWentWrong == True
        mlogger.warning(f'node : {node.localName} has no value even tough the configuration says otherwise. check GETFROMTHODES')


def processNode(node: Node, content: conf.XMLContent) -> None:
    mlogger.debug(f'function processNode() : node received {node.localName}')
    try:
        i = 0
        i == content.NODES[content.currentNodeType].index(node.localName)
        mlogger.debug(f'function processNode() : indice to seek into NODES : {i}')
        if (node.parentNode.localName == content.PARENTSOFTHESENODES[content.currentNodeType][i]):
            # test juste pour vérifier que je suis bien au bon endroit de la hiérarchie
            # et pas dans homonyme ailleurs
            match content.GETFROMTHESENODES[content.currentNodeType][i]:
                case conf.ToGet.ATTR:
                    processNodeAttributes(node, content)
                case conf.ToGet.DATA.value:
                    processNodeValue(node, content)
        else:
            mlogger.warning(f'unexpected parent : {node.parentNode.localName}, for node name : {node.localName}')
    except BaseException as be:
        mlogger.critical(f'Unexpected error in function processNode() : {type(be)}{be.args}')
        content.somethingWentWrong = True        




@log_function_call
def readModel(fileToRead: str) -> conf.XMLContent:
    '''
        Read an archimate model (in "open exchange" format)
        feed the object XMLContent with what's read
    '''

    @log_function_call
    def walk(listOfNodes, content: conf.XMLContent) -> None:
        '''
            get a list of Nodes and walk the tree of each element of that list

        '''
        for child in listOfNodes:
            mlogger.debug(f'function walk() : current Node :  {child.localName}')
            if child.nodeType == Node.ELEMENT_NODE:
                processNode(child)
            if not content.somethingWentWrong: # I stop walking if a node raise a problem
                if child.hasChildNodes():
                    walk(child.childNodes, content)
            else:
                mlogger.critical(f'Something went wrong in function walk() check the logs')



    try:
        with open(fileToRead, encoding='utf-8') as xmltoanalyse:
            doc = minidom.parse(xmltoanalyse)
            mlogger.info(f'function read_model() : opening the file {fileToRead}')
        modelName = doc.getElementsByTagName("name")[0].firstChild.data
        content = conf.XMLContent(modelName=modelName)


        for e in conf.NodeType:
            mlogger.debug(f'function read_model() : processing the node type {conf.NodeType}')
            mlogger.debug(f'function read_model() : known nodes given to walk() {content.NODES[e.value]}')
            content.currentNodeType == e.value
            walk(doc.getElementsByTagName(e.value), content)
            if content.somethingWentWrong:
                mlogger.critical(f'Something went wrong in function read_model() check the logs')
                return None


        return content
    except BaseException as be:
        mlogger.critical(f'Unexpected error in function read_model() : {type(be)}{be.args}')
        return None

