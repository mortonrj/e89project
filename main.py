import sched, time
import sys
import networkx as nx
import numpy as np
import fetcher as Fetcher
import matplotlib.mlab as mlab
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import Queue
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib
import Tkinter as tk
import webcrawler as WebCrawler
from PIL import Image, ImageTk
from io import BytesIO
import random



def main():
    # Tkinter setup
    height = 1000
    width = 1000
    root = tk.Tk()
    cv = tk.Canvas(root, width=width, height=height)
    cv.pack()


    # Scheduler and timer setup
    current_pages = ["http://www.caltech.edu/"]




    url = "http://imgs.xkcd.com/comics/python.png"
    raw_data =urlopen(url).read()
    im = Image.open(BytesIO(raw_data))
    image = ImageTk.PhotoImage(im)
    x = random.randrange(100)
    y = random.randrange(100)
    cv.create_image(x, y, image=image, anchor='nw')


    """
    q, images = WebCrawler.run_crawler(current_pages, 1)
    for i in images:
        try:
            print(i)
            image_url = tk.PhotoImage(data=i)
            image_byt = urlopen(image_url).read()
            image_b64 = base64.encodestring(image_byt)
            cv.create_image(10, 10, image=image_b64, anchor='nw')
            time.sleep(5)
        except:
            pass
    """

    '''
    while True:
        q, images = WebCrawler.run_crawler(current_pages, 1)
        print('hello')
        print(images)
        for i in images:
            try:
                print(i)
                photo = tk.PhotoImage(data=i)
                cv.create_image(10, 10, image=photo, anchor='nw')
                time.sleep(5)
            except:
                pass

            time.sleep(20)
            current_pages = [q.get()]
    '''
    root.mainloop()




main()
