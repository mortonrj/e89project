import time
import webcrawler as WebCrawler
import os
import Queue
import pygame
import glob

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
		
	def populate_queue(self, img_dir, scale=None, screen_size=None):
		cwd = os.getcwd()
		q = Queue.Queue()
		os.chdir(img_dir)
		for type in ["*.png", "*.jpg", "*.gif"]:
			for file in glob.glob(type):
				image = pygame.image.load(file)
				rect1 = image.get_rect()
				if scale:
					w,h = image.get_size()
					image = pygame.transform.scale(image, (int(scale*w), int(scale*h)))
				if screen_size:
					width, height = screen_size
					rect1.center = center=(random.randint(0, width), random.randint(0, height))
				q.put((image, rect1))
				
		os.chdir(cwd)
		return q

	
	def refresh(self):
		time_since_last_refresh = time.time() - self.last_time
		self.time_since_natural_image_update += time_since_last_refresh
		self.time_since_crawled_image_update += time_since_last_refresh
		if self.time_since_natural_image_update > self.rate_natural:
			time_since_crawled_image_update = 0
			self.update_natural_image()
		if self.time_since_crawled_image_update > self.rate_crawled:
			time_since_nat_image_update = 0
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
		newest_image = self.webcrawled_image_pool.pop()
		# Evict image
		if len(self.cur_webcraweled_images == self.num_webcrawled_images_to_simultaneously_display):
			self.cur_webcraweled_images.pop()
		self.cur_webcraweled_images.push(newest_image)
		
	def refill_pool(self):
		# Make sure len of pool becomes self.pool_max_size
		# Later: Clean up if statements and put in helper function
		
		# Delete all images in virtual images
		files = glob.glob(self.webcrawled_image_dir + '/*')
		for f in files:
			os.remove(f)
		
		# Refull virtual images
		q, self.last_links = WebCrawler.download_images(self.last_links)
		self.last_links = self.last_links[0:min(10, len(self.last_links))] # Last 10 links
		self.webcrawled_image_pool = self.populate_queue(self.webcrawled_image_dir, scale=0.5, screen_size=self.screen_size)

  