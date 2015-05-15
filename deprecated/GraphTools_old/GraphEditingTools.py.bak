"""
Tools for editing and reshaping graphs
"""

import networkx as nx


def prune_below_degree(graph, minimum_degree=1):
    """
    Trim nodes from graph below threshold
    
    Args:
        graph: NetworkX graph object to prune
        minimum_degree: Integer of the minimum connections a node must have
    
    Returns:
        Filtered graph object
    """
    g2 = graph.copy()
    d = nx.degree(g2)
    for n in g2.nodes():
        if d[n] <= minimum_degree: g2.remove_node(n)
    return g2


def remove_irrelevant_terms(graph, irrelevant_terms):
    """
    This will prune out irrelevant terms and return a copy of the graph without those nodes
    
    Args:
        graph: Networkx object
        irrelevant_terms: Iterable giving irrelevant terms. Usually ConstantsAndUtilities.Ignore.iterable
    
    Returns:
        Pruned graph
    """
    graph.remove_nodes_from(irrelevant_terms)
    return graph


def merge_nodes(graph, nodes, new_node, attr_dict=None, **attr):
    """
    This is a function to merge several nodes into one in a Networkx graph 
    Merges the selected `nodes` of the graph G into one `new_node`,
    meaning that all the edges that pointed to or from one of these
    `nodes` will point to or from the `new_node`.
    attr_dict and **attr are defined as in `G.add_node`.
    """
    G = graph.copy()
    G.add_node(new_node, attr_dict, **attr) # Add the 'merged' node
    for n1,n2,data in G.edges(data=True):
        # For all edges related to one of the nodes to merge,
        # make an edge going to or coming from the `new gene`.
        if n1 in nodes:
            G.add_edge(new_node,n2,data)
        elif n2 in nodes:
            G.add_edge(n1,new_node,data)
    for n in nodes: # remove the merged nodes
        G.remove_node(n)
    return G


def merge_from_list(graph, merge_dict):
    """
    This merges nodes in a graph based on a dictionary giving mappings
    
    Args:
        graph: Networkx graph object to modify
        merge_dict: A dictionary with the mappings. Usually this is ConstantsAndUtilities.Merge.toMerge
    
    Returns:
        Updated graph object
    """
    for k in merge_dict.keys():
        graph = merge_nodes(graph, merge_dict[k], k)
    return graph

if __name__ == '__main__':
    pass
