import sys
import networkx as nx
import numpy as np
import fetcher as Fetcher
import matplotlib.mlab as mlab
import matplotlib
import random
import os
import string
import Queue
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib
import pygame
import signal

all_time_visited = set()


class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

def download_images(url_list, webcrawled_image_dir, scale, screen_size, batch_size=50):
    """ Returns queue of URLs"""
    print('@@@@@@@@@@@@@ url list:', url_list)
    cwd = os.getcwd()
    print('\n\n\n')
    leftover_links, images = run_crawler(url_list, batch_size)
    if len(images) > batch_size:
        images = images[:batch_size]
    # Images in pool are stored in tupes of format (pygame image, image dims, local image path)
    image_pool = Queue.Queue()
    for url in images:
        cwd = os.getcwd()
        image = urllib.URLopener()
        image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        im_path = webcrawled_image_dir + image_name + '.jpg'
        image.retrieve(url, im_path)
        pygame_image = pygame.image.load(im_path)
        rect1 = pygame_image.get_rect()
        w,h = pygame_image.get_size()
        pygame_image = pygame.transform.scale(pygame_image, (int(scale*w), int(scale*h)))
        width, height = screen_size
        rect1.center =(random.randint(0, width), random.randint(0, height))
        image_pool.put((pygame_image, rect1, im_path))

    return image_pool, leftover_links


def get_images(url):
    soup = make_soup(url)
    images = [img for img in soup.findAll('img')]
    print("Made it to get_images")
    print(images)
    #compile our unicode list of image links
    image_links = [each.get('src') for each in images if 'http' in each.get('src')]

    return image_links

def make_soup(url):
    html = urlopen(url).read()
    return BeautifulSoup(html, "lxml")

# Returns list containing all hyperlinks
def run_crawler(current_pages, min_images):
    global all_time_visited
    q = Queue.Queue()
    visited = set()
    print("\n\n")
    print(current_pages)
    print("\n\n")
    for page in current_pages:
        print(page)
        q.put(page)
        print("Queue added page")
        visited.add(page)
        print("Visited added page")
    images = []
    while len(images) < min_images:
        page = q.get()
        print("in while loop")
        print(page)
        visited.add(page)
        print("hi1")
        all_time_visited.add(page)
        print("hi1")
        links = Fetcher.fetch_links(page)
        print("hi1")
        if links is None:
            continue

        print(links)

        for l in links[:10]:
            print(l)
            #if 'caltech.edu' in l and l != 'http://hr.caltech.edu/work/job_openings' and len(l) > 4:
            signal.alarm(5)
            try:
                if l not in visited and l not in all_time_visited:
                    print('new item added to queue:')
                    print(l)
                    q.put(l)
                    images.extend(get_images(l))
            except TimeoutException:
                continue # continue the for loop if function A takes more than 5 second
            else:
                # Reset the alarm
                signal.alarm(0)
    print('$$$$$$$$$$$$$ret val', q.queue, '\n\n', images)
    return list(q.queue), images

def main():
    path_length = 10
    current_pages = ["http://www.bing.com/"]
    q, images = run_crawler(current_pages, 1)
    print(len(images))

main()
