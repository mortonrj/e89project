import sys, pygame
import time
import pygame.time
import glob, os
import random
from canvas_mt import Canvas
import webcrawler as WebCrawler



def main():
	pygame.init()
	size = width, height = 1026, 768
	screen = pygame.display.set_mode(size)
	natural_rate = .5
	crawled_rate = 5
	nature_image_dir = "./hd_walk/"
	webcrawled_image_dir = "./webcrawled_images/"
	num_webcrawled_images_to_simultaneously_display = 6
	c = Canvas(natural_rate, crawled_rate, nature_image_dir, webcrawled_image_dir, screen, size, num_webcrawled_images_to_simultaneously_display)
		
		
	# start music
	pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
	pygame.init()
	#pygame.mixer.init()
	#pygame.mixer.music.load('./music/e89.mp3')
	#pygame.mixer.music.play(-1)
	
	# Init joystick
	joystick = pygame.joystick.Joystick(0)
	joystick.init()
	
	while 1:
		# Checking for quit event, and if so exiting
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
			#if event.type == pygame.KEYDOWN:
			#	print('KEYDOWN')
			#	c.change_nat_rate(-1)
			#if event.type == pygame.KEYUP:
			#	print('KEYUP')
			#	c.change_nat_rate(1)

		# Check axis
		axis_reading = .2 * joystick.get_axis(1)
		c.change_nat_rate(axis_reading)
		c.change_crawl_rate(axis_reading)
		
		# Check button
		if joystick.get_button(0):
			c.change_simultanous_images(1)
		elif joystick.get_button(1):
			c.change_simultanous_images(-1)
	
		c.refresh()
		pygame.display.flip()
	
main()
