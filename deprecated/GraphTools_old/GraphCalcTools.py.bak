#calc closeness centrality
import shelve
import networkx

def sorted_degree_map(degree_map):
    """
    Function which sorts hashtags by their degrees
    
    Args:
        degree_map:
    
    Returns:
        Sorted mapping
    """
    ms = sorted(degree_map.iteritems(), key=lambda (k,v):(-v,k))
    return ms

def calc_and_save_closeness_centrality(graph, term):
    c = nx.closeness_centrality(graph)
    cs = sorted_degree_map(c)
    s = shelve.open('charts_and_graphs/%s_closenesscentrality' % date.today())
    s[term] = cs
    s.close()

def load_closeness_centrality(term, date):
    """
    Loads a list of tuples containing closeness centrality for the term
    """
    s = shelve.open('charts_and_graphs/%s_closenesscentrality' % date)
    graph = s[term]
    s.close()
    return graph

#Betweenness centrality
def calc_and_save_betweeneness_centrality(graph, term):
    c = nx.betweenness_centrality(graph)
    cs = sorted_degree_map(c)
    s = shelve.open('charts_and_graphs/%s_betweennesscentrality' % date.today())
    s[term] = cs
    s.close()

def load_betweenness_centrality(term, date):
    """
    Loads a list of tuples containing betweenness centrality for the term
    """
    s = shelve.open('charts_and_graphs/%s_betweennesscentrality' % date)
    graph = s[term]
    s.close()
    return graph

#Average clustering coefficient
def calc_and_save_clustering_coefficient(graph, term):
    c = nx.average_clustering(graph)
    s = shelve.open('charts_and_graphs/%s_avgclusteringcoefficient' % date.today())
    s[term] = cs
    s.close()

def load_clustering_coeff(term, date):
    """
    Loads a list of tuples containing betweenness centrality for the term
    """
    s = shelve.open('charts_and_graphs/%s_avgclusteringcoefficient' % date)

if __name__ == '__main__':
    pass
