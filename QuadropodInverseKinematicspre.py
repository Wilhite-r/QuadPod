import math
from QuadropodServos import ServoInstructions
a0 = 0  # shoulder arm length
a1 = 5  # upper uarm length
a2 = 5  # lower arm/end effetor length

def evaluator(a1,a2,x,y): # inverse kinematic equations
    t1 = math.pi/2 - (math.pi/2 - math.atan2( (a1**3*x + a1*x*(-a2**2 + x**2 + y**2) + \
         math.sqrt(-(a1**2*y**2*(a1**4 + (-a2**2 + x**2 + y**2)**2 - \
         2*a1**2*(a2**2 + x**2 + y**2)))))/(a1**2*(x**2 + y**2)),\
         (a1**3*y**2 + a1*y**2*(-a2**2 + x**2 + y**2) - \
         x*math.sqrt(-(a1**2*y**2*(a1**4 + (-a2**2 + x**2 + y**2)**2 -\
         2*a1**2*(a2**2 + x**2 + y**2)))))/(a1**2*y*(x**2 + y**2))))

    t2 = math.acos((x**2 + y**2 - a1**2 - a2**2)/(2 * a1 * a2))
    return[t1,t2]

def get_lower(a1,a2,r,z): # ggets the angles of the lower part of the arm
    x = z
    y = r
    [t1,t2] = get_lower(a1,a2,x,y)
    return [t1 * 360/ (2 * math.pi),t2 * 360/ (2 * math.pi)]


def cart_to_cyl(x,y,z): #converts cartesian to cylindrical
    r = (x**2 + y**2)**(1/2)
    theta = math.atan2(y, x)
    return [r, theta, z]


def get_angles(frontright,frontleft,backright,backleft,a0,a1,a2):#returns a list of [theta0,theta1,theta2] (all in rad)

    #convert to cylindrical
    frontright = cart_to_cyl(frontright[0],frontright[1],frontright[2])
    frontleft = cart_to_cyl(-frontleft[0],frontleft[1],frontleft[2]) #the x value is negative because the side is flipped. I assume global coordinates
    backright = cart_to_cyl(frontleft[0],frontleft[1],frontleft[2])
    backleft = cart_to_cyl(-backleft[0], backleft[1], backleft[2]) #the x value is negative because the side is flipped. I assume global coordinates
    
    #solve for the angles
    [frt1, frt2] = get_lower(a1, a2, frontright[0] - a0, frontright[2])
    [flf1, flf2] = get_lower(a1, a2, frontleft[0] - a0, frontleft[2])
    [brt1, brt2] = get_lower(a1, a2, backright[0] - a0, backright[2])
    [blf1, blf2] = get_lower(a1, a2, backleft[0] - a0, backleft[2])
    
    #returns a list of [theta0,theta1,theta2] 
    return ServoInstructions([frontright[1], frt1, frt2],[backright[1], brt1, brt2],[frontleft[1], flf1, flf2],[backleft[1], blf1, blf2])
