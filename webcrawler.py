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
		
all_time_visited = set()

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
			if 'caltech.edu' in l and l != 'http://hr.caltech.edu/work/job_openings' and len(l) > 4:
				if l not in visited and l not in all_time_visited:
					print('new item added to queue:', l)
					q.put(l)
					images.extend(get_images(l))
	print('$$$$$$$$$$$$$ret val', q.queue, '\n\n', images)
	return list(q.queue), images

def main():
    path_length = 10
    current_pages = ["http://www.caltech.edu/"]
    q, images = run_crawler(current_pages, 1)
    print(images)
