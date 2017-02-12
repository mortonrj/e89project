from Tkinter import *
master = Tk()
height = 1000
width = 1000
w = Canvas(master, width=width, height=height)
w.pack()

w.create_line(0, 0, height, width)

w.create_rectangle(50, 25, 150, 75, fill="blue")

mainloop()
