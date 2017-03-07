import sys
import networkx as nx
import numpy as np
import fetcher as Fetcher
import matplotlib.mlab as mlab
import matplotlib
import random
import os
import string
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import Queue
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib

def download_images(url_list, batch_size=50, screen_size=None):
    """ Returns queue of URLs"""
    q, images = run_crawler(url_list, 1)
    if len(images) > batch_size:
        images = images[:batch_size]
    for url in images:
        cwd = os.getcwd()
        print(cwd)
        image = urllib.URLopener()
        image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        image.retrieve(url, './image/virtual_images/' + image_name + '.jpg')
    return q

def get_images(url):
    soup = make_soup(url)
    images = [img for img in soup.findAll('img')]

    #compile our unicode list of image links
    image_links = [each.get('src') for each in images if 'http' in each.get('src')]

    return image_links

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

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
    q, images = run_crawler(current_pages, 1)
    print(images)
# Helpful links:
# https://www.daniweb.com/programming/software-development/code/440946/display-an-image-from-a-url-tkinter-python
# https://www.daniweb.com/programming/software-development/code/467528/show-internet-image-with-tkinter
