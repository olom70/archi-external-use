import logging
import functools
from xml.dom import minidom, Node
import archi.configarchi as conf
import networkx as nx
import numpy as np
import uuid
import itertools

mlogger = logging.getLogger('test-archi-external-use.tools')

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

        TODO : instead as iterating explicitly twice, I could use cycle() : https://realpython.com/iterate-through-dictionary-python/#using-itertools
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
    @log_function_call
    def addImplicitRelationship(content: conf.XMLContent) -> None:
        '''
        Add a relationship between two nodes that are embeded in a view
        '''
        try:
            #first : single out all the relations with a source equal to the parent node
            search = content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RS.value]
            npsearch = np.asarray(search)
            indices = np.asarray(npsearch==content.isPotentialParent).nonzero()

            found = True
            if len(indices[0]) > 0:
                #second : in the result, search a target that is the current node
                relationExists = [ i for i in range(len(indices[0])) if indices[0][i] == content.isChild ]
                if len(relationExists) > 0:
                    # third : I found a least a relationship between the parent and the child
                    # now let's examine if there is a suitable relation type to add
                    relationOK = [ i for i in range(len(relationExists)) if relationExists[i] == conf.SuitableRelationship.COMPOSITION.value ]
                    if len(relationOK) > 0:
                        content.allObjects[content.currentNodeType][content.currentView][2].append(conf.NodeType.RELATIONSSHIP.value[conf.ToStore.RI.value][relationOK[0]])
                        content.allObjects[content.currentNodeType][content.currentView][2].append(relationOK[0])
                    else:
                        relationOK = [ i for i in range(len(relationExists)) if relationExists[i] == conf.SuitableRelationship.AGGREGATION.value ]
                        if len(relationOK) > 0:
                            content.allObjects[content.currentNodeType][content.currentView][2].append(conf.NodeType.RELATIONSSHIP.value[conf.ToStore.RI.value][relationOK[0]])
                            content.allObjects[content.currentNodeType][content.currentView][2].append(relationOK[0])
                        else:
                            found = False
                else:
                    found = False
            else:
                found = False
            
            if not found:
                uid = uuid.uuid4()
                content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RI.value].append(uid)
                content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RT.value].append(conf.SuitableRelationship.COMPOSITION.value)
                content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RN.value].append(None)
                content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RD.value].append(None)
                content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RS.value].append(content.isPotentialParent)
                content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RG.value].append(content.isChild)
                content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RA.value].append(None)
                content.allObjects[content.currentNodeType][content.currentView][2].append(uid)
        except Exception as e:
            mlogger.warning(f"'A problem occured during the process of isPotentialParent : {content.isPotentialParent}, isChild {content.isChild}', {type(e)}{e.args})")

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
                                    content.isPotentialParent = map[key].value if tofind in conf.IsPotentialParentType.list() else ''
                                    if tofind in conf.IsChildType.list():
                                        content.isChild = map[key].value
                                        addImplicitRelationship(content)
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
            mlogger.warning(f"'{tofind}' not found in NODES, check the configuration. ({type(be)}{be.args})")

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
        return content
    except BaseException as be:
        mlogger.critical(f'Unexpected error in function read_model() : {type(be)}{be.args}')
        return None

@log_function_call
def createGraph(content: conf.XMLContent) -> nx.MultiDiGraph:
    '''
        process conf.XMLContent.allobjects to create a graph
    '''
    modelAsGraph = nx.MultiDiGraph()

    def processElement(elements: dict) -> None:
        for ei, et, en, ed, pv in zip(elements[conf.ToStore.EI.value],
                                                elements[conf.ToStore.ET.value],
                                                elements[conf.ToStore.EN.value],
                                                elements[conf.ToStore.ED.value],
                                                elements[conf.ToStore.PV.value]):
            modelAsGraph.add_nodes_from(
                [
                    (ei, {conf.ToStore.ET.value: et,
                            conf.ToStore.EN.value: en,
                            conf.ToStore.ED.value: ed,
                            conf.ToStore.PV.value: pv})
                ]
            )

    def processRelationShip(relationships: dict) -> None:
        for ri, rt, rn, rs, rg, ra in zip(relationships[conf.ToStore.RI.value],
                                                relationships[conf.ToStore.RT.value],
                                                relationships[conf.ToStore.RN.value],
                                                relationships[conf.ToStore.RS.value],
                                                relationships[conf.ToStore.RG.value],
                                                relationships[conf.ToStore.RA.value]):
            modelAsGraph.add_edges_from(
                [
                    (rs, rg, {conf.ToStore.RI.value: ri,
                                conf.ToStore.RT.value: rt,
                                conf.ToStore.RN.value: rn,
                                conf.ToStore.RA.value: ra})
                ]
            )
        
    def processViews(views: dict) -> None:
        mlogger.info(f"nodeType Views is known, but is not handled here")

    try:
        for e in conf.NodeType:
            match e:
                case conf.NodeType.ELEMENT:
                    processElement(content.getNodes(e))
                case conf.NodeType.RELATIONSSHIP:
                    processRelationShip(content.getNodes(e))
                case conf.NodeType.VIEW:
                    processViews(content.getNodes(e))
                case _:
                    mlogger.warning(f'this NodeType seems new, as it has no means to process it. When will you get your hands dirty ?. NodeType : {e.value}')
        return modelAsGraph
    except Exception as be:
        mlogger.critical(f'Unexpected error in function create_graph() : {type(be)}{be.args}')
        return None

@log_function_call
def createGraphView(viewIdentifier: str, content: conf.XMLContent) -> nx.MultiDiGraph:
    '''
    Create the graph for the view identified by viewIdentifier
    '''
    viewAsGraph = nx.MultiDiGraph()
    try:
        for k,v in content.allObjects[conf.NodeType.VIEW.value].items():
            mlogger.debug(f'key / value processed : {k} / {v}')
            if k == viewIdentifier:
                viewAsGraph.add_nodes_from([(viewIdentifier, {conf.ToStore.NI.value: v[0]})]) # v[0] holds the identifiers of the view
                for n in v[1]: # v[1] holds the identifiers of the nodes
                    i = content.allObjects[conf.NodeType.ELEMENT.value][conf.ToStore.EI.value].index(n)
                    name = content.allObjects[conf.NodeType.ELEMENT.value][conf.ToStore.EN.value][i]
                    viewAsGraph.add_nodes_from([(n, {conf.ToStore.EN.value: name})])
                for e in v[2]: # v[2] holds the identifiers of the edges
                    i = content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RI.value].index(e)
                    name = content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RN.value][i]
                    source = content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RS.value][i]
                    target = content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RG.value][i]
                    viewAsGraph.add_edges_from([(source, target, {conf.ToStore.RN.value: name,
                                                                conf.ToStore.RI.value: e
                                                                })]
                                                )
        return viewAsGraph
    except Exception as e:
        mlogger.critical(f'Unexpected error in function createGraphView() : {type(e)}{e.args}')
        return None