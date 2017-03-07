import sys, pygame
import time
import pygame.time
import Queue
import glob, os
import random


def repopulate_nature_images():
    cwd = os.getcwd()
    print(cwd)
    #nature_image_dir = "../../image/nature_images/stop_motion_man_forest"
    nature_image_queue = Queue.Queue()
    for file in glob.glob("*.png"):
        image = pygame.image.load(file)
        nature_image_queue.put((image, image.get_rect()))
    return nature_image_queue



pygame.init()
size = width, height = 1026, 768
black = 0, 0, 0

screen = pygame.display.set_mode(size)

# start music
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('piano.mp3')
pygame.mixer.music.play(-1)

# Load image with rectangular area
past_images = {}
virtual_image_queue = Queue.Queue()
nature_image_queue = Queue.Queue()
delete_queue = Queue.Queue()

virtual_image_dir = "./image/virtual_images"
nature_image_dir = "../../image/nature_images/stop_motion_man_forest"

cwd = os.getcwd()
print(cwd)
os.chdir(virtual_image_dir)
for file in glob.glob("*.png"):
    image = pygame.image.load(file)
    w,h = image.get_size()
    image = pygame.transform.scale(image, (int(0.5*w), int(0.5*h)))
    rect1 = image.get_rect()
    rect1.center = (random.randint(0, width), random.randint(0, height))
    virtual_image_queue.put((image, rect1))
for file in glob.glob("*.jpg"):
    image = pygame.image.load(file)
    w,h = image.get_size()
    image = pygame.transform.scale(image, (int(0.5*w), int(0.5*h)))
    rect1 = image.get_rect()
    rect1.center = (random.randint(0, width), random.randint(0, height))
    virtual_image_queue.put((image, rect1))

cwd = os.getcwd()
print(cwd)
os.chdir(nature_image_dir)
for file in glob.glob("*.png"):
    image = pygame.image.load(file)
    rect1 = image.get_rect()
    virtual_image_queue.put((image, rect1))

while 1:
    # Checking for quit event, and if so exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if not virtual_image_queue.empty():
        if nature_image_queue.empty():
            nature_image_queue = repopulate_nature_images()

        # Fills screen with a color
        screen.fill(black)

        cur_nature_image = nature_image_queue.get()
        screen.blit(cur_nature_image[0], cur_nature_image[1])

        cur_virtual_image = virtual_image_queue.get()
        delete_queue.put(cur_virtual_image)
        past_images[cur_virtual_image[0]] = cur_virtual_image[1]

        # Displaying all of the images and using .blit to draw them
        for past_image in past_images:
            screen.blit(past_image, past_images[past_image])

        # Makes display on the screen visible
        pygame.display.flip()

        # Waits between images
        pygame.time.wait(600)
