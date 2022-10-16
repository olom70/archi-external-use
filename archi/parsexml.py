import logging
import functools
from xml.dom import minidom, Node
import archi.configarchi as conf
import numpy as np

mlogger = logging.getLogger('archi-external-use.parsexml')

def log_function_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        mlogger.info(f'Start of the function {func.__name__}')
        response = func(*args, **kwargs)
        mlogger.info(f'End of the function {func.__name__}')
        return response
    return wrapper

@log_function_call
def alignIndices(content: conf.XMLContent) -> None:
    '''
        The lists of allObjects needs to grow the same pace.
        As some nodes (like Documentation) are optional,
        at the end of the walk() of each NodeType, one need
        to insert None where needed

        TODO : instead of iterating explicitly twice, I could use cycle() : https://realpython.com/iterate-through-dictionary-python/#using-itertools
    '''
    for e in conf.NodeType:
        max = -1 # First step is to get the maximum length pf the lists
        for k, v in content.allObjects[e.value].items():
            if len(v) > max:
                max = len(v)
        #Second step is to add one value to the lists for those thier length is lower than the max
        # as this function is called for each NodeTYpe, I know that at most one value is missing
        mlogger.debug(f'function alignIndices() : max value found : {max}')
        for k, v in content.allObjects[e.value].items():
            if len(v) < max:
                v.append(None)
                content.allObjects[e.value][k] = v
                mlogger.debug(f'function alignIndices() : adding None to : {e.value}/{k}')

@log_function_call
def readModel(fileToRead: str) -> conf.XMLContent:
    '''
        Read an archimate model (in "open exchange" format)
        feed the object XMLContent with what's read
    '''

    def processNodeAttributes(node: Node, content: conf.XMLContent) -> None:
        mlogger.debug(f'function processNodeAttributes() : node received {node.localName}')
        if node.hasAttributes():
            map = node.attributes
            for key in map.keys():
                tofind = node.parentNode.localName+"-"+map[key].localName
                if content.currentNodeType != conf.NodeType.VIEW.value :
                    try:
                        content.allObjects[content.currentNodeType][tofind].append(map[key].value)
                    except KeyError as k:
                        mlogger.warning(f"'{tofind}' not found in TOSTORE, check the configuration")    
                else:
                    try:
                        match tofind:
                            case conf.ToStore.VI.value: #diagrams-identifier
                                # each time I find this value I know that it's a new view to add
                                content.allObjects[content.currentNodeType][map[key].value] = [None, [], []]
                                                                                            # [name, [Nodes], [Relationships]]
                                content.currentView = map[key].value
                            case conf.ToStore.VT.value: #diagrams-type
                                if map[key].value != 'Diagram':
                                    del content.allObjects[content.currentNodeType][content.currentView]
                                    content.currentView = None
                                    # As the view is not a diagram I delete what I initiated when
                                    # I encountered ToStore.VI.value
                            case conf.ToStore.NE.value | conf.ToStore.OE.value: # view-elementRef, node-elementRef
                                if content.currentView is not None:
                                    content.allObjects[content.currentNodeType][content.currentView][1].append(map[key].value)
                            case conf.ToStore.VR.value: # view-relationshipRef
                                if content.currentView is not None:
                                    content.allObjects[content.currentNodeType][content.currentView][2].append(map[key].value)
                    except Exception as e:
                        mlogger.warning(f"'A problem occured during the process of {content.currentNodeType}/{tofind}', check the configuration. ({type(e)}{e.args})")
        else:
            content.somethingWentWrong == True
            mlogger.warning(f'node : {node.localName} has no attributes even though the configuration says otherwise. check GETFROMTHODES')


    @log_function_call
    def processNodeValue(node: Node, content: conf.XMLContent) -> None:
        mlogger.debug(f'function processNodeValue() : node received {node.localName}. parent : {node.parentNode.localName}')
        if node.hasChildNodes():
            tofind = node.parentNode.localName+"-"+node.localName
            if content.currentNodeType != conf.NodeType.VIEW.value :
                try:
                    content.allObjects[content.currentNodeType][tofind].append(node.firstChild.data)
                except KeyError as k:
                    mlogger.warning(f"'{tofind}' not found in TOSTORE, check the configuration")
            else:
                match tofind:
                    case conf.ToStore.VN.value: #view-name
                        content.allObjects[content.currentNodeType][content.currentView][0] = node.firstChild.data
        else:
            content.somethingWentWrong == True
            mlogger.warning(f'node : {node.localName} has no value even tough the configuration says otherwise. check GETFROMTHODES')

    @log_function_call
    def processNode(node: Node, content: conf.XMLContent) -> None:
        mlogger.debug(f'function processNode() : node received {node.localName}')
        try:
            tofind = node.parentNode.localName+"-"+node.localName
            if node.localName in conf.NodeType.list():
                alignIndices(content)
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
            mlogger.warning(f"'{tofind}' not found in NODES, check the configuration.")
        except Exception as e:
            mlogger.warning(f"'{tofind}' not found in NODES, check the configuration. ({type(e)}{e.args})")
    
    @log_function_call
    def addAggregations(content: conf.XMLContent) -> None:
        '''
            In a view, when a concept is embeded in another one, the relationship does not appear in the XML file.
            I do need to add it manually, assuming it's a relation that can be nested
        '''

        @log_function_call
        def RelationCanBeAdded(content: conf.XMLContent, viewid: str, node: str, toStoreOne: conf.ToStore, toStoreTwo: conf.ToStore) -> None:
            found = False
            #first : single out all the relations with a source or target equal to the node
            mlogger.debug(f'searching relation for node {node}')
            try:
                search = content.allObjects[conf.NodeType.RELATIONSSHIP.value][toStoreOne]
                npsearch = np.asarray(search)
                indices = np.asarray(npsearch==node).nonzero()
                if len(indices[0]) > 0:
                    for i in indices[0]:
                        otherSideOfTheCurrentRelationship = content.allObjects[conf.NodeType.RELATIONSSHIP.value][toStoreTwo][i]
                        for nodeToCompareTo in nodes:
                            if nodeToCompareTo == otherSideOfTheCurrentRelationship:
                                if content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RT.value][i] in conf.SuitableRelationship.list():
                                    content.allObjects[conf.NodeType.VIEW.value][viewid][2].append(content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RI.value][i])
                                    mlogger.debug(f'adding relation {content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RI.value][i]}')
                                    found = True
                if not found:
                    mlogger.info(f"The node {node} has either no connection at all or has an explicit connection in the view")
            except Exception as e:
                mlogger.warning(f"'unexpected error in the function relationCanBeAdded(). ({type(e)}{e.args})")


        try:
            if len(content.allObjects[conf.NodeType.VIEW.value]):
                for viewid in content.allObjects[conf.NodeType.VIEW.value].keys():
                    name = ''
                    nodes = []
                    relationships = []
                    name, nodes, relationships = content.allObjects[conf.NodeType.VIEW.value][viewid]
                    for node in nodes:
                        RelationCanBeAdded(content, viewid, node, conf.ToStore.RS.value, conf.ToStore.RG.value)
        except Exception as e:
            mlogger.warning(f"'unexpected error in the function addAggregations. ({type(e)}{e.args})")


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
        alignIndices(content)
        addAggregations(content)
        return content
    except BaseException as be:
        mlogger.critical(f'Unexpected error in function read_model() : {type(be)}{be.args}')
        return None