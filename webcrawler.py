import sys
import networkx as nx
import numpy as np
import fetcher as Fetcher
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import Queue
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html)

def get_images(url):
    soup = make_soup(url)
    images = [img for img in soup.findAll('img')]

    #compile our unicode list of image links
    image_links = [each.get('src') for each in images]

    return image_links

# Returns list containing all hyperlinks
def run_crawler(current_page, path_length):
    q = Queue.Queue()
    q.put(current_page)
    visited = {current_page}
    links = []
    while len(visited) <= path_length:
        page = q.get()
        visited.add(page)
        links = Fetcher.fetch_links(page)
        if links is None:
            continue

        for l in links:
            if 'caltech.edu' in l:
                if l not in visited:
                    q.put(l)

                    image = get_images(l)
                    print image

def main():
    path_length = 10
    current_page = "http://www.caltech.edu/"
    run_crawler(current_page, path_length)


main()
