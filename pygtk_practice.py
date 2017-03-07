import sys, pygame
import time
import pygame.time
import Queue
import glob, os
import random
import webcrawler as WebCrawler

def populate_queue(img_dir, scale=None, screen_size=None):
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
    return q

def repopulate_nature_images():
    cwd = os.getcwd()
    print(cwd)
    #nature_image_dir = "../../image/nature_images/stop_motion_man_forest"
    nature_image_queue = Queue.Queue()
    for file in glob.glob("*.png"):
        image = pygame.image.load(file)
        nature_image_queue.put((image, image.get_rect()))
    return nature_image_queue

def main():
    pygame.init()
    size = width, height = 1026, 768
    black = 0, 0, 0

    # Downloading crawler images:
    WebCrawler.download_images(['http://www.caltech.edu/'])

    screen = pygame.display.set_mode(size)

    # start music
    pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('./music/piano.mp3')
    pygame.mixer.music.play(-1)

    # Load image with rectangular area
    past_images = {}
    virtual_image_queue = Queue.Queue()
    nature_image_queue = Queue.Queue()
    delete_queue = Queue.Queue()

    virtual_image_dir = "./image/virtual_images"
    nature_image_dir = "../../image/nature_images/stop_motion_man_forest"

    virtual_image_queue = populate_queue(virtual_image_dir, scale=0.5, screen_size=size)
    nature_image_queue = populate_queue(nature_image_dir)

    while 1:
        # Fills screen with a color
        screen.fill(black)

        # Checking for quit event, and if so exiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        # Repopulating queues if empty
        if virtual_image_queue.empty():
            # Later: Clean up if statements and put in helper function
            if 'virtual_images' in os.getcwd():
                virtual_image_queue = populate_queue("../../image/virtual_images", scale=0.5, screen_size=size)
            else:
                virtual_image_queue = populate_queue("../../../image/virtual_images", scale=0.5, screen_size=size)
        if nature_image_queue.empty():
            nature_image_queue = repopulate_nature_images()

        cur_nature_image = nature_image_queue.get()
        screen.blit(cur_nature_image[0], cur_nature_image[1])

        cur_virtual_image = virtual_image_queue.get()
        delete_queue.put(cur_virtual_image)
        past_images[cur_virtual_image[0]] = cur_virtual_image[1]

        # Displaying all of the images and using .blit to draw them
        for past_image in past_images:
            screen.blit(past_image, past_images[past_image])

        pygame.display.flip()
        pygame.time.wait(600)

main()
