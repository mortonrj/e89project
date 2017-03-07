import sys
import networkx as nx
import numpy as np
import fetcher as Fetcher
import matplotlib.mlab as mlab
import matplotlib
matplotlib.use('TkAgg')
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
def run_crawler(current_pages, path_length):
    q = Queue.Queue()
    visited = set()
    for page in current_pages:
        q.put(page)
        visited.add(page)
    images = []
    while len(visited) <= path_length:
        page = q.get()
        visited.add(page)
        links = Fetcher.fetch_links(page)
        if links is None:
            continue

        for l in links[:10]:
            if 'caltech.edu' in l and l != 'http://hr.caltech.edu/work/job_openings':
                if l not in visited:
                    q.put(l)
                    images.extend(get_images(l))
        return q, images

def main():
    path_length = 10
    current_pages = ["http://www.caltech.edu/"]
    run_crawler(current_pages, 1)

# Helpful links:
# https://www.daniweb.com/programming/software-development/code/440946/display-an-image-from-a-url-tkinter-python
# https://www.daniweb.com/programming/software-development/code/467528/show-internet-image-with-tkinter


main()
