import sys, pygame
import time
import pygame.time
import glob, os
import random
from canvas import Canvas


def main():
	pygame.init()
	size = width, height = 1026, 768
	screen = pygame.display.set_mode(size)
	natural_rate = .5
	crawled_rate = .5
	nature_image_dir = "hd_walk/"
	webcrawled_image_dir = "webcrawled_images/"
	num_webcrawled_images_to_simultaneously_display = 4
	c = Canvas(natural_rate, crawled_rate, nature_image_dir, webcrawled_image_dir, screen, size, num_webcrawled_images_to_simultaneously_display)
	
	# start music
	pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.load('./music/e89.mp3')
	pygame.mixer.music.play(-1)
	
	while 1:
		# Checking for quit event, and if so exiting
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
	
		c.refresh()
		pygame.display.flip()
		pygame.time.wait(60)
	
main()
