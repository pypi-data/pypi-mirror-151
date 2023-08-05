import json

from tokyo_annotation.lineage import Lineage
from tokyo_annotation.utils import DiGraph
from tokyo_annotation.models.lineage import DataNode, JobNode


def parse_lineage_from_marquez(
    lineage: str
) -> Lineage:
    parsed = json.loads(lineage)

    _graph = parsed['graph']
    graph = DiGraph()

    # Register all nodes in graph
    for node in _graph:
        node_type = DataNode if node['type'] == 'DATASET' else JobNode
        graph.add(
            node_type(node['id'], node['type'])
        )

    # Connect node's edges
    nodes = graph.nodes.map

    def _get_key_from_id(id, nodes: dict):
        for k, node in nodes.items():
            if node.id == id:
                return k

    for node in _graph:
        in_edges = [edge['origin'] for edge in node['inEdges']]
        out_edges = [edge['destination'] for edge in node['outEdges']]

        current_node_key = _get_key_from_id(node['id'], nodes)

        for id in in_edges:
            node_key = _get_key_from_id(id, nodes)
            graph.set_edge(node_key, current_node_key, True)

        for id in out_edges:
            node_key = _get_key_from_id(id, nodes)
            graph.set_edge(current_node_key, node_key, True)

    return Lineage(graph)