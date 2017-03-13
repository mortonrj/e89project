import sys, pygame
import time
import pygame.time
import glob, os
import random
from canvas_mt import Canvas
from threading import Thread
import webcrawler as WebCrawler

def launch_image_crawler_daemon(pool, last_links, webcrawled_image_dir, screen_size, pool_max_size, rate_crawled):
		# Constantly Refill virtual images
		# Make sure len of pool stays under self.pool_max_size
		scale = .5
		while True:
			pool_size = pool.qsize()
			print('Daemon operational. Queue size:', pool_size)
			if pool_size >= pool_max_size:
				time.sleep(rate_crawled)
				continue
				
				
			add_to_pool, last_links = WebCrawler.download_images(last_links, webcrawled_image_dir, scale, screen_size, batch_size=pool_max_size)
			no_links = min(10, len(last_links))
			if no_links == 1:
				last_links = [last_links[0]] # First 10 links
			else:
				last_links = last_links[0:no_links] # First link
				
				
			add_to_pool = list(add_to_pool.queue)
			for im in add_to_pool:
				pool.put(im)
			

def main():
	pygame.init()
	size = width, height = 1026, 768
	screen = pygame.display.set_mode(size)
	natural_rate = .5
	crawled_rate = 5
	nature_image_dir = "./hd_walk/"
	webcrawled_image_dir = "./webcrawled_images/"
	num_webcrawled_images_to_simultaneously_display = 4
	c = Canvas(natural_rate, crawled_rate, nature_image_dir, webcrawled_image_dir, screen, size, num_webcrawled_images_to_simultaneously_display)
	#Launch webcrawl in background		
	#worker = Thread(target=launch_image_crawler_daemon, args=(c.webcrawled_image_pool, c.last_links, c.webcrawled_image_dir, c.screen_size, c.pool_max_size, c.rate_crawled))
	#worker.setDaemon(True)
	#worker.start()
		
		
	# start music
	pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
	pygame.init()
	#pygame.mixer.init()
	#pygame.mixer.music.load('./music/e89.mp3')
	#pygame.mixer.music.play(-1)
	
	while 1:
		# Checking for quit event, and if so exiting
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
	
		c.refresh()
		pygame.display.flip()
		pygame.time.wait(60)
	
main()
