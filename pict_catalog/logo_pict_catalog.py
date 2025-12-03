def arcr90(logo):
    for i in range(1,360/4,1):
        logo.fd(1)
        logo.rt(1)
def arcl90(logo):
    for i in range(1,360/4,1):
        logo.fd(1)
        logo.lt(1)
def arcr60(logo):
    for i in range(1,360/6,1):
        logo.fd(1)
        logo.rt(1)
def arcl60(logo):
    for i in range(1,360/6,1):
        logo.fd(1)
        logo.lt(1)
def arcr(logo,degrees):
    for i in range(1,degrees,1):
        logo.fd(1)
        logo.rt(1)
def arcl(logo,degrees):
    for i in range(1,degrees,1):
        logo.fd(1)
        logo.lt(1)    
def lcircle(logo,radius):
    radius = radius / logo.modifier
    for i in range(1,360,1):
        logo.fd(radius)
        logo.lt(1)
def rcircle(logo,radius):
    radius = radius / logo.modifier
    for i in range(1,360,1):
        logo.fd(radius)
        logo.rt(1)

def swirlstar(logo):
    for i in range(1,1800,1):
        logo.fd(10)
        logo.rt(i+0.1)
        
def berry(logo):
    for i in range(1,8,1):
        logo.rt(45)
        for i in range(1,4,1):
            for i in range(1,90,1):
                logo.fd(2)
                logo.rt(2)
            logo.rt(90)                

def fan(logo):
    for i in range(1,60,1):
        logo.pu()
        logo.rt(20)
        logo.pd()
        for i in range(1,3,1):
            logo.arcr(logo,50)
            logo.arcr(logo,60)
            logo.arcl(logo,50)
            logo.arcl(logo,90)
            logo.bk(logo,50)
            logo.lt(logo,90)
def fourside(logo):
    #REPEAT 2 [FD 60 RT 30 FD 60 RT 150]
    for i in range(1,2,1):
        logo.fd(60)
        logo.rt(30)
        logo.fd(60)
        logo.rt(150)
def sun(logo):
    logo.pd()
    for i in range(1,72,1):
        logo.fourside(logo)
        logo.rt(5)
    logo.pu()
def fleur(logo):
    logo.pd()
    for i in range(1,9,1):
        logo.fourside(logo)
        logo.rt(30)
    logo.pu()
def flower(logo):
    logo.pd()
    for i in range(1,18,1):
        logo.fourside(logo)
        logo.rt(20)
    logo.pu()
def square(logo,size):
    logo.pd()
    logo.fd(size*32)
    logo.pu()
    logo.lt(90)
    logo.pd()
    logo.fd(size*32)
    logo.pu()
    logo.lt(90)
    logo.pd()
    logo.fd(size*32)
    logo.pu()
    logo.lt(90)
    logo.pd()
    logo.fd(size*32)
    logo.pu()
    logo.lt(90)
    #logo.fd((size*32)+(3*32))
def rabbit(logo):
    logo.pd()
    logo.head(logo)
    logo.arcl(logo,7.5)
    logo.arcl(logo,90)
    logo.rt(60)
    logo.body(logo)
def body(logo):
    logo.arcr(logo,20)
    logo.arcr(logo,60)
    logo.lcircle(logo,3.5)
    logo.arcl(logo,20)
    logo.arcl(logo,60)
    logo.arcr(logo,1.5)
    logo.arcr(logo,180)
    logo.arcr(logo,20)
    logo.arcr(logo,60)
    logo.lt(60)
    logo.arcr(logo,50)
    logo.arcr(logo,30)
    logo.arcl(logo,50)
    logo.arcl(logo,30)
    logo.arcr(logo,1.5)
    logo.arcr(logo,180)
    logo.arcr(logo,50)
    logo.arcr(logo,30)
def ears(logo):
    logo.ear(logo)
    logo.rt(150)
    logo.ear(logo)
def ear(logo):
    logo.arcr(logo,30)
    logo.arcr(logo,60)
    logo.rt(logo,120)
    logo.arcr(logo,30)
    logo.arcr(logo,60)
def head(logo):
    logo.ears(logo)
    logo.arcl(logo,7)
    logo.arcl(logo,540)
def star(logo,points,length,iterations):
    '''
    Draw a 'n' pointed star with 'length' sides

    Args:
        sides: number of points
        length: length of each side
    '''
    angle = 180.0 - 180.0 / points
    logo.pd()
    itcalc = (360/iterations)
    for _ in range(iterations):
        for _ in range(points):
            logo.fd(length)
            logo.lt(angle)
            logo.fd(length)
        #if itcalc != 360:
        logo.lt(itcalc)

    logo.pu()
    logo.fd((length)+(3*32))
def poolball(logo):
    logo.circle(logo,1.5)
    logo.circle(logo,2.25)
def eyeball(logo):
    logo.circle(logo,0.75)
    logo.circle(logo,1.5)
    logo.circle(logo,2.25)
def circle(logo,size):
    logo.pd()
    for i in range(1,360,1):
        logo.fd(size)
        logo.rt(1)