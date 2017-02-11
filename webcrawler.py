import sys
import networkx as nx
import numpy as np
import fetcher as Fetcher
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import Queue

# Returns list containing all hyperlinks
def run_crawler(current_page, G):
    q = Queue.Queue()
    q.put(current_page)
    visited = set(current_page)

    while len(visited) <= 2000:
        page = q.get()
        visited.add(page)
        links = Fetcher.fetch_links(page)
        if links is None:
            continue

        for l in links:
            if 'caltech.edu' in l:
                G.add_edge(page, l)
                if l not in visited:
                    q.put(l)


def main():
    G = nx.DiGraph()
    current_page = "http://www.caltech.edu/"
    run_crawler(current_page, G)


main()
