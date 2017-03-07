import os
import random
from multiprocessing import Queue
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def entry():

    return render_template('entry_page.html')

@app.route('/main')
def main():
    image_src1 = 'dice.png'
    image_src2 = 'panda.jpg'

    """
    q = Queue.Queue()
    q.put(image_src1)
    q.put(image_src2)

    timer = request.args.get('timer')
    if timer:
        try:
            timer = int(timer)
        except:
            timer = None
    """

    return render_template('main_page.html', image_src=image_src1)
