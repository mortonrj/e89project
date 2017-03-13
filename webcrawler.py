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
    print("Get_images about to make soup")
    print(url)
    soup = make_soup(url)

    if soup.findAll('img') <= 0:
        return []
    images = [img for img in soup.findAll('img')]
    #compile our unicode list of image links
    print("Made it to images")
    print(images)
    if len(images) > 0:
        image_links = set()
        print(images[0].get('src'))
        for elem in images:
            try:
                if 'http' in elem.get('src'):
                    image_links.add(elem.get('src'))
            except:
                pass

        return list(image_links)
    return []

def make_soup(url):
    try:
        html = urlopen(url).read()
        return BeautifulSoup(html, "lxml")
    except:
        pass

# Returns list containing all hyperlinks
def run_crawler(current_pages, min_images):
    global all_time_visited
    q = Queue.Queue()
    visited = set()
    for page in current_pages:
        q.put(page)
        visited.add(page)
    images = []
    while len(images) < min_images:
        page = q.get()
        visited.add(page)
        all_time_visited.add(page)
        links = Fetcher.fetch_links(page)
        if links is None:
            continue

        for l in links[:10]:
            print(l)
            signal.alarm(10)
            try:
                if l not in visited and l not in all_time_visited:
                    q.put(l)
                    images.extend(get_images(l))
                    print("\n \n Current number of images")
                    print(len(images))
                    print("I have been extended")
            except TimeoutException:
                continue # continue the for loop if function A takes more than 5 second
            else:
                # Reset the alarm
                signal.alarm(0)
    print('$$$$$$$$$$$$$ret val', q.queue, '\n\n', images)
    return list(q.queue), images

def main():
    path_length = 10
    current_pages = ["http://www.amazon.com/"]
    q, images = run_crawler(current_pages, 1)
    print(len(images))

main()
