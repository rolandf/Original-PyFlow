"""@package SubGraphs

Class based subgraph.
"""
import os

_subgraphClasses = {}
import json

def _getClasses():
    from ..Nodes.subgraphNode import subgraphNode
    # append from Nodes
    for n in os.listdir(os.path.dirname(__file__)):
        if n.endswith(".pySubgraph"):
            nodeName = n.split(".")[0]
            try:
                with open(os.path.join(os.path.dirname(__file__),n), 'r') as f:
                    data = json.load(f)
                    tryloadFromData("graph",data)   

                node_class = subgraphNode
                if nodeName not in _subgraphClasses:
                    _subgraphClasses[nodeName] = [node_class,data]
            except Exception as e:
                # do not load node if errors or unknown modules
                print(e, nodeName)
                pass


def getNode(name):
    if name in _subgraphClasses:
        return _subgraphClasses[name]
    return None


def getNodeNames():
    return _subgraphClasses.keys()

def tryloadFromData(name,data,path=""):
    data["Type"]
    data["category"]
    data["keywords"]
    data["description"]   
    data[name]['variables']
    data[name]['nodes']
    data[name]['edges']
                 
 
_getClasses()
