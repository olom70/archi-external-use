import os
import logging
import functools
from xml.dom import minidom, Node
import archi.configarchi as conf
from interactive import ToStore

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
        map = node.attributes
        for key in map.keys():
            if map[key].localName in content.ToStore.list():
                mlogger.debug(f'parent of the node : {node.parentNode.localName}, attr name :  {map[key].localName}, value : {map[key].value}')
                match key:
                    case conf.ToStore.ID.value:
                        content.allObjects[content.currentNodeType][conf.Position.ID.value].append(map[key].value)
                    case conf.ToStore.TYPE.value:
                        content.allObjects[content.currentNodeType][conf.Position.TYPE.value].append(map[key].value)
                    case conf.ToStore.PROPERTY.value:
                        content.allObjects[content.currentNodeType][conf.Position.PROPNAME.value].append(map[key].value)
                    case conf.ToStore.SOURCE.value:
                        content.allObjects[content.currentNodeType][conf.Position.SOURCE.value].append(map[key].value)
                    case conf.ToStore.TARGET.value:
                        content.allObjects[content.currentNodeType][conf.Position.TARGET.value].append(map[key].value)
            else:
                mlogger.warning(f'this attribute is unknown : {map[key].localName}, add it in ATTRIBUTESOFTHENODES in order to process it.')
    else:
        content.somethingWentWrong == True
        mlogger.warning(f'node : {node.localName} has no attributes even though the configuration says otherwise. check GETFROMTHODES')


def processNodeValue(node: Node, content: conf.XMLContent) -> None:
    mlogger.debug(f'function processNodeValue() : node received {node.localName}. parent : {node.parentNode.localName}')
    if node.hasChildNodes():
        i = content.NODES[content.currentNodeType].index(node.localName)
        match (node.localName):
            case (conf.ToStore.DOCUMENTATION.value):
                content.allObjects[content.currentNodeType][conf.Position.DOCUMENTATION.value].append(node.firstChild.data)
            case (conf.ToStore.NAME.value):
                if (content.PARENTSOFTHESENODES[content.currentNodeType][i] == conf.QualifyName.PROPERTYNAME.value):
                    content.allObjects[content.currentNodeType][conf.Position.PROPVALUE.value].append(node.firstChild.data)
                else:
                    content.allObjects[content.currentNodeType][conf.Position.NAME.value].append(node.firstChild.data)
            case _:
                mlogger.warning(f'This node is not parametized, set it up. Node name : {node.localName}. Parent : {node.parentNode.localName}')
                
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
            match content.GETFROMTHESENODES[content.currentNodeType][i]:
                case conf.ToGet.ATTR:
                    processNodeAttributes(node, content)
                case conf.ToGet.DATA:
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

