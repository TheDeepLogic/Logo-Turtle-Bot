from random import *
from PIL import Image, ImageDraw, ImageOps
from util import *
import math

def sortlines(lines):
    print("optimizing stroke sequence...")
    clines = lines[:]
    slines = [clines.pop(0)]
    while clines != []:
        x,s,r = None,1000000,False
        for l in clines:
            d = distsum(l[0],slines[-1][-1])
            dr = distsum(l[-1],slines[-1][-1])
            if d < s:
                x,s,r = l[:],d,False
            if dr < s:
                x,s,r = l[:],s,True

        clines.remove(x)
        if r == True:
            x = x[::-1]
        slines.append(x)
    return slines

def rotate(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    rel_x, rel_y = mouse_x - self.x, mouse_y - self.y
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    self.image = pygame.transform.rotate(self.original_image, int(angle))
    self.rect = self.image.get_rect(center=self.position)
def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d
def visualize(lines):
    import turtle
    wn = turtle.Screen()
    t = turtle.Turtle()
    t.speed(0)
    t.pencolor('red')
    t.pd()
    mouse_x = -0
    mouse_y = 0
    #t.goto(-300,300)
    for i in range(0,len(lines)):
        for p in lines[i]:
            x = p[0]*640/1024-320
            y = -(p[1]*640/1024-320)
            d = distance([mouse_x,mouse_y],[x,y])
            x1 = mouse_x
            y1 = mouse_y
            x2 = x
            y2 = y
           # m = slope = (y1-y2)/(x1-x2)
           # y = m*x + b
           # b = y-intercept = (x1*y2 - x2*y1)/(x1-x2)


            rel_x, rel_y = mouse_x - x, mouse_y - y
            angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
            if angle > 0:
                t.right(angle)
            elif angle < 0:
                t.left(angle)
            

            import numpy as np
            p1 = np.array((mouse_x,mouse_y))
            p2 = np.array((x,y))
            sq = np.sum(np.square(p1 - p2))
            print(np.sqrt(sq))
            #t.forward(np.sqrt(sq))
            t.forward((d*640/1024-320)/180)
            #t.goto(p[0]*640/1024-320,-(p[1]*640/1024-320))
            #print(math.pi/2 - math.atan(x))
            #print(math.pi/2 - math.atan(y))
            #t.right(math.pi/2 - math.atan(x))
            #t.left(math.pi/2 - math.atan(y))
            mouse_x = x
            mouse_y = y
            #t.forward(x-y)
            t.pencolor('black')
        t.pencolor('red')
    turtle.mainloop()

if __name__=="__main__":
    import linedraw
    #linedraw.draw_hatch = False
    lines = linedraw.sketch(".\\images\\peppers.png")
    #lines = sortlines(lines)
    visualize(lines)