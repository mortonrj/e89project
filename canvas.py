import time



class Canvas:
	def __init__(self, natural, crawled, nat_folder, num_webcrawled_images_to_simultaneously_display=3):
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
		self.positions_of_webcrawled_images = Queue.Queue()
		self.cur_webcrawled_images = Queue.Queue()
		self.webcrawled_image_pool = Queue.Queue()
		self.pool_max_size = 10

		self.canvas_width = get_width(cur_nat_image) # Assumes all natural images are same resolution
		# Used to make sure that we web crawler images that are too big are discarded
		self.canvas_length = get_length(cur_nat_image)
	
	
	def refresh(self, current_time):
		time_since_last_refresh = time.time() - self.last_time
		self.time_since_nat_image_update += time_since_last_refresh
		self.time_since_crawled_image_update += time_since_last_refresh
		if self.time_since_natural_image_update > self.rate_natural:
			time_since_crawled_image_update = 0
			update_natural_image()
		if self.time_since_crawled_image_update > self.rate_crawled:
			time_since_nat_image_update = 0
			update_crawled_images()
			
		# Convert cur_nat_image_index to a pygame image and display
		nat_im_path = self.nat_im_path + '/' +  self.nat_image_names[self.cur_nat_image_index]
		
		# convert cur_webcraweled_images to pygame images and overlay
		
	
	def update_natural_image():
		self.cur_nat_image_index = (self.cur_nat_image_index + 1) % self.num_nat_images
			
	# TODO eventually: Fade out one image, fade in one image
	def update_crawled_images():
		if len(self.webcrawled_image_pool) == 0:
			self.refill_pool()
		newest_image = self.webcrawled_image_pool.pop()
		# Evict image
		if len(self.cur_webcraweled_images == self.num_webcrawled_images_to_simultaneously_display):
			self.cur_webcraweled_images.pop()
			self.positions_of_webcrawled_images.pop()
		self.cur_webcraweled_images.push(newest_image)
		self.positions_of_webcrawled_images.push(self.gen_position(newest_image))

	def gen_position(image):
		# Use image dim and canvas dim to gen positions_of_webcrawled_images
		new_position = ...
		return new_position
		
	def refill_pool():
		# Make sure len of pool becomes self.pool_max_size