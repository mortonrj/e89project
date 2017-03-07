import sys, pygame
import time
import pygame.time
import Queue
import glob, os

pygame.init()
size = width, height = 600, 600
black = 0, 0, 0

screen = pygame.display.set_mode(size)


image2 = pygame.image.load("./image/virtual_images/dice.png")
image = pygame.image.load("./image/virtual_images/panda.jpg")

# start music
pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('piano.mp3')
pygame.mixer.music.play(-1)

# Load image with rectangular area
past_images = {}
image_queue = Queue.Queue()
delete_queue = Queue.Queue()

image_dir = "./image/virtual_images"
os.chdir(image_dir)
for file in glob.glob("*.png"):
    image = pygame.image.load('./image/virtual_images/' +  file)
    image_queue.put(image, image.get_rect())
for file in glob.glob("*.jpg"):
    print(file)
image_queue.put((image, image.get_rect()))
image_queue.put((image2, image2.get_rect()))


while 1:
    # Checking for quit event, and if so exiting
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if not image_queue.empty():
        # Fills screen with a color
        screen.fill(black)

        cur_image = image_queue.get()
        delete_queue.put(cur_image)
        past_images[cur_image[0]] = cur_image[1]

        # Displaying all of the images and using .blit to draw them
        for past_image in past_images:
            screen.blit(past_image, past_images[past_image])

        # Makes display on the screen visible
        pygame.display.flip()

        # Waits between images
        pygame.time.wait(600)
