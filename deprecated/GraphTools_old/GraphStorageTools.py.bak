
#Tool for dealing with unicode encoding problems
from django.utils.encoding import smart_str, smart_unicode
import TwitterGEXF as TG #custom gexf saver
from datetime import date
import networkx as nx

class GEXFSaver(object):
    """
    Saves graph in gexf format
    """
    problems = []
    @staticmethod
    def stringit(x):
        """
        Fixes problem with unicode encoding
        """
        try:
            return x.encode('ascii')
        except UnicodeDecodeError:
            saver.problems.append(x)

    @staticmethod
    def save(graph, graphname, path="charts_and_graphs"):
        """
        Saves a graph to a file after fixing unicode problems to work around a bug in nx
        @param graph The graph to save
        @param filename The file to save it to
        """
        tr = nx.relabel_nodes(graph, saver.stringit)
        today = date.today()
        filename = '%s/%s_%s.gexf' % (path, date.today(), graphname)
        TG.write_gexf(tr, filename)
        f = open('path/%s_%s_errors.txt' %(path, date.today(), graphname), 'w')
        for p in saver.problems:
            f.write('%s \n' % p)
        f.close()
        print "%s problems" % len(saver.problems)
        saver.problems = []

def make_and_save_egographs(maingraph, term):
    """
    Make and save Ego graphs with irrelevant terms removed. 
    
    Args:
        maingraph: The main body graph to make ego graphs from
        term: String of term to make the egograph for
    """
    g = nx.ego_graph(maingraph, term)
    g = remove_irrelevant_terms(g)
    print nx.info(g)
    saver.save(g, '%s_egograph' % term)
    
def load(date, graphname, path='charts_and_graphs'):
    """
    Loads saved graphs
    """
    return nx.read_gexf('%s/%s_%s.gexf' % (path, date, graphname))

if __name__ == '__main__':
    pass