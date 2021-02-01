import math
from QuadropodServos import ServoInstructions
a0 = 1 #shoulder arm length
a1 = 5 #upper uarm length
a2 = 5 #lower arm/end effetor length

def evaluator(a1,a2,x,y): # inverse kinematic equations
    if y == 0:
        y = 0.001
    if x == 0:
        x = 0.001
    x1 = 0
    if x < 0:
        x1 = x
        x = -x
    t1 =   - (math.pi/2 - math.atan2( (a1**3*x + a1*x*(-a2**2 + x**2 + y**2) + \
         math.sqrt(-(a1**2*y**2*(a1**4 + (-a2**2 + x**2 + y**2)**2 - \
         2*a1**2*(a2**2 + x**2 + y**2)))))/(a1**2*(x**2 + y**2)),\
         (a1**3*y**2 + a1*y**2*(-a2**2 + x**2 + y**2) - \
         x*math.sqrt(-(a1**2*y**2*(a1**4 + (-a2**2 + x**2 + y**2)**2 -\
         2*a1**2*(a2**2 + x**2 + y**2)))))/(a1**2*y*(x**2 + y**2))))

    t2 = math.acos((x**2 + y**2 - a1**2 - a2**2)/(2 * a1 * a2))
    if  x1 < 0:
        t1 = -t1
        t2 = -t2
    return[t1,t2]

def get_lower(a1,a2,r,z): # ggets the angles of the lower part of the arm
    x = r
    y = -z
    [t1,t2] = evaluator(a1,a2,x,y)
    return [t1,t2]

def cart_to_cyl(x,y,z): #converts cartesian to cylindrical
    r = (x**2 + y**2)**(1/2)
    theta = math.atan2(y,x)
    return [r,theta,z]

def get_angles(frontright,backright,frontleft,backleft,a0,a1,a2):#returns a list of [theta0,theta1,theta2] (all in deg)
      
    #convert to cylindrical
    frontright = cart_to_cyl(frontright[0],frontright[1],frontright[2])
    frontleft = cart_to_cyl(-frontleft[0],frontleft[1],frontleft[2]) #the x value is negative because the side is flipped. I assume global coordinates
    backright = cart_to_cyl(backright[0],backright[1],backright[2])
    backleft = cart_to_cyl(-backleft[0], backleft[1], backleft[2]) #the x value is negative because the side is flipped. I assume global coordinates
    
    #solve for the angles
    [frt1, frt2] = get_lower(a1, a2, frontright[0] - a0, frontright[2])
    [flf1, flf2] = get_lower(a1, a2, frontleft[0] - a0, frontleft[2])
    [brt1, brt2] = get_lower(a1, a2, backright[0] - a0, backright[2])
    [blf1, blf2] = get_lower(a1, a2, backleft[0] - a0, backleft[2])
    
    
    #returns a list of [theta0,theta1,theta2] 
    results = [[math.pi/2 + frontright[1], math.pi/2 -frt1, math.pi - frt2],\
               [math.pi/2 - frontleft[1], math.pi/2 + flf1, flf2],\
               [math.pi/2 - backright[1], math.pi/2 + brt1, brt2],\
               [math.pi/2 + backleft[1], math.pi/2 -blf1, math.pi - blf2]]
    final = []
    index1 = 0
    for element in results:
        legvec = []
        index = 0
        for value in element:
            if index != 2:
                offset = 1/18 * math.pi
            elif index1 == 0 or index1 == 3:
                offset = 2/18 * math.pi 
            new_val = 9/8 * 180/math.pi * (value - offset)
            legvec.append(new_val)
            index = index + 1
            offset = 0
        final.append(legvec) 
        index1 += 1
    return ServoInstructions(final[0], final[2], final[1], final[3])
