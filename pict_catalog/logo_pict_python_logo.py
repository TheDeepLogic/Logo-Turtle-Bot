t = None
#s = turtle.Screen()
#s.bgcolor("black")
#t.speed(10)
#t.pensize(2)
#t.pencolor("white")

def pylogo(turtle):
    global t
    t = turtle
    t.pd()
    half()
    get_pos()
    half()
    eye()
    sec_dot()
    pause()

def s_curve():
    for i in range(90):
        t.lt(1)
        t.fd(1)

def r_curve():
    for i in range(90):
        t.rt(1)
        t.fd(1)

def l_curve():
    s_curve()
    t.fd(80)
    s_curve()

def l_curve1():
    s_curve()
    t.fd(90)
    s_curve()

def half():
    t.fd(50)
    s_curve()
    t.fd(90)
    l_curve()
    t.fd(40)
    t.lt(90)
    t.fd(80)
    t.rt(90)
    t.fd(10)
    t.rt(90)
    t.fd(120) #on test
    l_curve1()
    t.fd(30)
    t.lt(90)
    t.fd(50)
    r_curve()
    t.fd(40)
    #t.end_fill()

def get_pos():
    t.pu()
    t.fd(20)
    t.rt(90)
    t.fd(10)
    t.rt(90)
    t.pd()

def eye():
    #t.pu()
    t.rt(90)
    t.fd(160)
    t.lt(90)
    t.fd(70)
    #t.pencolor("black")
    #t.dot(35)
    t.rcircle(1)

def sec_dot():
    t.lt(90)
    t.pu()
    t.fd(310)
    t.lt(90)
    t.fd(120)
    t.pd()
    t.rcircle(1)
    #t.dot(35)




#t.fillcolor("#306998")
#t.begin_fill()
#half()
#t.end_fill()
#get_pos()
#t.fillcolor("#FFD43B")
#t.begin_fill()
#half()
#t.end_fill()




def pause():
    #t.speed(2)
    for i in range(100):
        t.lt(90)
#pause()
