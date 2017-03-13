import time
import webcrawler as WebCrawler
from threading import Thread
import os
import Queue
import pygame
import glob
import random

class Canvas:
	def __init__(self, natural, crawled, nat_folder, webcrawled_folder, _screen, size, num_webcrawled_images_to_simultaneously_display):
		self.rate_natural = natural # How often to update in seconds
		self.rate_crawled = crawled # How often to update in seconds
		self.last_time = time.time()
		self.time_since_natural_image_update = 0
		self.time_since_crawled_image_update = 0
		
		self.cur_nat_image_index = 0
		self.nat_folder = nat_folder
		self.nat_image_names = os.listdir(nat_folder)
		self.num_nat_images = len(self.nat_image_names)
		
		self.num_webcrawled_images_to_simultaneously_display = num_webcrawled_images_to_simultaneously_display
		self.cur_webcrawled_images = Queue.Queue()
		self.webcrawled_image_pool = Queue.Queue()
		self.pool_max_size = 10
		self.webcrawled_image_dir = webcrawled_folder
		self.last_links = ['http://www.caltech.edu/']

		# Used to make sure that we web crawler images that are too big are discarded
		self.screen_size = size
		self.screen = _screen
	
		# Launch webcrawl in background		
		worker = Thread(target=self.launch_image_crawler_daemon, args=(self.webcrawled_image_pool, self.last_links))
		worker.setDaemon(True)
		worker.start()
		
	def refresh(self):
		print('Refreshing.... Crawled Image Pool Size:', self.webcrawled_image_pool.qsize())
		cur_time = time.time()
		time_since_last_refresh = cur_time - self.last_time
		self.last_time = cur_time
		self.time_since_natural_image_update += time_since_last_refresh
		self.time_since_crawled_image_update += time_since_last_refresh
		if self.time_since_natural_image_update > self.rate_natural:
			#print('natural updated. Time since last')
			self.time_since_nat_image_update = 0
			self.update_natural_image()
		if self.time_since_crawled_image_update > self.rate_crawled:
			#print('webcrawled updated')
			self.time_since_crawled_image_update = 0
			self.update_crawled_images()
			
		# Convert cur_nat_image_index to a pygame image and display
		nat_im_path = './' + self.nat_folder +  self.nat_image_names[self.cur_nat_image_index]
		nat_im = self.create_pygame_image(nat_im_path)
		
		# Redraw
		black = 0, 0, 0
		self.screen.fill(black)
		self.screen.blit(nat_im[0], nat_im[1])
		for im in list(self.cur_webcrawled_images.queue):
			self.screen.blit(im[0], im[1])
		cur_time = time.time()
		time_since_last_refresh = cur_time - self.last_time
		self.last_time = cur_time
		self.time_since_natural_image_update += time_since_last_refresh
		self.time_since_crawled_image_update += time_since_last_refresh
		if self.time_since_natural_image_update > self.rate_natural:
			#print('natural updated. Time since last')
			self.time_since_nat_image_update = 0
			self.update_natural_image()
		if self.time_since_crawled_image_update > self.rate_crawled:
			#print('webcrawled updated')
			self.time_since_crawled_image_update = 0
			self.update_crawled_images()
			
		# Convert cur_nat_image_index to a pygame image and display
		nat_im_path = './' + self.nat_folder +  self.nat_image_names[self.cur_nat_image_index]
		nat_im = self.create_pygame_image(nat_im_path)
		
		# Redraw
		black = 0, 0, 0
		self.screen.fill(black)
		self.screen.blit(nat_im[0], nat_im[1])
		for im in list(self.cur_webcrawled_images.queue):
			self.screen.blit(im[0], im[1])
		
	def create_pygame_image(self, img_loc):
		image = pygame.image.load(img_loc)
		rect1 = image.get_rect()
		return (image, rect1)
			
	def update_natural_image(self):
		self.cur_nat_image_index = (self.cur_nat_image_index + 1) % self.num_nat_images
			
	# TODO eventually: Fade out one image, fade in one image
	def update_crawled_images(self):
		if self.webcrawled_image_pool.qsize() == 0:
			self.refill_pool()
		newest_image = self.webcrawled_image_pool.get()
		# Evict image
		if self.cur_webcrawled_images.qsize() == self.num_webcrawled_images_to_simultaneously_display:
			path_to_evicted = self.cur_webcrawled_images.get()[2]
			os.remove(path_to_evicted)
		self.cur_webcrawled_images.put(newest_image)
		
	# Images in pool are stored in tupes of format (pygame image, image dims, local image path)
	def refill_pool(self):
		while(self.webcrawled_image_pool.qsize < self.pool_max_size):
			print('current size of pool:', self.webcrawled_image_pool.qsize)
			time.sleep(1)
		
	def launch_image_crawler_daemon(self, pool, last_links):
		# Constantly Refill virtual images
		# Make sure len of pool stays under self.pool_max_size
		scale = .5
		while True:
			pool_size = pool.qsize()
			print('Daemon operational. Queue size:', pool.qsize())
			if self.webcrawled_image_pool.qsize() >= self.pool_max_size:
				time.sleep(self.rate_crawled)
				continue
				
				
			add_to_pool, last_links = WebCrawler.download_images(last_links, self.webcrawled_image_dir, scale, self.screen_size, batch_size=self.pool_max_size)
			no_links = min(10, len(last_links))
			if no_links == 1:
				last_links = [last_links[0]] # First 10 links
			else:
				last_links = last_links[0:no_links] # First link
				
				
			add_to_pool = list(add_to_pool.queue)
			for im in add_to_pool:
				pool.put(im)
			
  
  