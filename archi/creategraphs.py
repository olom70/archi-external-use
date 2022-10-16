import logging
import archi.configarchi as conf
import networkx as nx

from archi.parsexml import log_function_call

mlogger = logging.getLogger('archi-external-use.creategraphs')

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
                for n in v[1]: # v[1] holds the identifiers of the nodes
                    i = content.allObjects[conf.NodeType.ELEMENT.value][conf.ToStore.EI.value].index(n)
                    name = content.allObjects[conf.NodeType.ELEMENT.value][conf.ToStore.EN.value][i]
                    viewAsGraph.add_nodes_from([(n, {conf.ToStore.EN.value: name})])
                for e in v[2]: # v[2] holds the identifiers of the edges
                    i = content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RI.value].index(e)
                    name = content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RN.value][i]
                    source = content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RS.value][i]
                    target = content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RG.value][i]
                    rtype = content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RT.value][i]
                    accessType = content.allObjects[conf.NodeType.RELATIONSSHIP.value][conf.ToStore.RA.value][i]
                    viewAsGraph.add_edges_from([(source, target, {conf.ToStore.RN.value: name,
                                                                conf.ToStore.RI.value: e,
                                                                conf.ToStore.RT.value: rtype,
                                                                conf.ToStore.RA.value: accessType
                                                                })]
                                                )
        return viewAsGraph
    except Exception as e:
        mlogger.critical(f'Unexpected error in function createGraphView() : {type(e)}{e.args}')
        return None