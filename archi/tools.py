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
        map = node.attributes
        for key in map.keys():
            try:
                tofind = node.parentNode.localName+"-"+map[key].localName
                content.allObjects[content.currentNodeType][tofind].append(map[key].value)
            except KeyError as k:
                mlogger.warning(f"'{tofind}' not found in TOSTORE, check the configuration")    
    else:
        content.somethingWentWrong == True
        mlogger.warning(f'node : {node.localName} has no attributes even though the configuration says otherwise. check GETFROMTHODES')


@log_function_call
def readModel(fileToRead: str) -> conf.XMLContent:
    '''
        Read an archimate model (in "open exchange" format)
        feed the object XMLContent with what's read
    '''

    def processNodeValue(node: Node, content: conf.XMLContent) -> None:
        mlogger.debug(f'function processNodeValue() : node received {node.localName}. parent : {node.parentNode.localName}')
        if node.hasChildNodes():
            try:
                tofind = node.parentNode.localName+"-"+node.localName
                content.allObjects[content.currentNodeType][tofind].append(node.firstChild.data)
            except KeyError as k:
                mlogger.warning(f"'{tofind}' not found in TOSTORE, check the configuration")
        else:
            content.somethingWentWrong == True
            mlogger.warning(f'node : {node.localName} has no value even tough the configuration says otherwise. check GETFROMTHODES')

    def processNode(node: Node, content: conf.XMLContent) -> None:
        mlogger.debug(f'function processNode() : node received {node.localName}')
        try:
            tofind = node.parentNode.localName+"-"+node.localName
            i = content.NODES[content.currentNodeType].index(tofind)
            mlogger.debug(f'function processNode() : indice to seek into NODES : {i}')
            match content.GETFROMTHESENODES[content.currentNodeType][i]:
                case conf.ToGet.ATTR:
                    processNodeAttributes(node, content)
                case conf.ToGet.DATA:
                    processNodeValue(node, content)
                case conf.ToGet.NONE:
                    pass
        except KeyError as k:
            mlogger.critical(f"'{tofind}' not found in NODES, check the configuration.")
            content.somethingWentWrong = True        

    @log_function_call
    def walk(listOfNodes, content: conf.XMLContent) -> None:
        '''
            get a list of Nodes and walk the tree of each element of that list

        '''
        for child in listOfNodes:
            mlogger.debug(f'function walk() : current Node :  {child.localName}')
            if child.nodeType == Node.ELEMENT_NODE:
                processNode(child, content)
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
            content.currentNodeType = e.value
            walk(doc.getElementsByTagName(e.value), content)
            if content.somethingWentWrong:
                mlogger.critical(f'Something went wrong in function read_model() check the logs')
                return None
        return content
    except BaseException as be:
        mlogger.critical(f'Unexpected error in function read_model() : {type(be)}{be.args}')
        return None

