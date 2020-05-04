import math  
import cmath  
import numpy as np
from matplotlib import pyplot as plt 
import control
from sympy.solvers import solve
from sympy import Symbol
import utils.critical_values as cval 
s = Symbol('s')
t = Symbol('t')
K = Symbol('K')
#Some hard-coded values
num=[1]
den=[1,3,2]
H = 1

#Transfer Function
G = control.tf(num,den)
G_feedbacked = control.feedback(G,H)
control.sisotool(G_feedbacked)
print("OPEN LOOP TRANSFER FUNCTION")
print(G)
print("CLOSE LOOP TRANSFER FUNCTION")
print(G_feedbacked)
poles, zeros = control.pzmap(G, True, True)
all_points = np.concatenate([[-np.Infinity] ,zeros,poles])
all_points.sort()
all_real_points = np.real(all_points[np.isreal(all_points)])
print("Range in real axis :")
range_of_real_axis= []
for i in range(len(all_real_points)-1,0, -2):
    print("From " + str(all_real_points[i-1]) + " to " + str(all_real_points[i]))
    range_of_real_axis += [all_real_points[i-1], all_real_points[i]]
print("The starting points are:"+ str(poles))
print("The ending points are:" + str(zeros))
print("The total number of branches is: " + str(len(poles)))
sum_of_inverse_zeros = 0
sum_of_inverse_poles = 0
for zero in zeros:
    sum_of_inverse_zeros += 1/(s-zero)
for pole in poles:
    sum_of_inverse_poles += 1/(s-pole)
eqn = sum_of_inverse_zeros - sum_of_inverse_poles
values_of_s = solve(eqn, s)
breakaway_points=[]
for j in range(0,len(values_of_s)):
    for i in range(0,len(range_of_real_axis)-1, 2):
        try:
            if (values_of_s[j] > range_of_real_axis[i] and values_of_s[j] < range_of_real_axis[i+1]):
                breakaway_points += [round(values_of_s[j], 4)]
        except:
                print("An exception occurred")
print("Break-away/Break-in  points are: " + str(breakaway_points))
for i in range(1,len(poles)+1):
    #print("testing point is: " + str(poles[i-1]))
    sum_of_poles_angles=0
    sum_of_zeros_angles=0
    for j in range(0,len(zeros)):
        angle=0
        x1 = np.real(poles[i-1])
        y1 = np.imag(poles[i-1])
        x2 = np.real(zeros[j])
        y2 = np.imag(zeros[j])
        if((x1==x2)and(y1==-y2)and(y1!=0)):
            angle=90
        if (x1 != x2):
            angle = math.degrees(math.atan((y2-y1)/(x2-x1)))
            if ( x1 < x2 and angle==0):
                angle = 180
            if ( x2 < x1 and angle==0):
                angle = 0
        sum_of_zeros_angles += angle
        #print("  angle for point" + str(zeros[j]) + " is " + str(angle))
    #print("sum of angles: " + str(sum_of_zeros_angles)    )
    for k in range(0,len(poles)):
        angle=0
        x1 = np.real(poles[i-1])
        y1 = np.imag(poles[i-1])
        x2 = np.real(poles[k])
        y2 = np.imag(poles[k])
        if((x1==x2)and(y1==-y2)and(y1!=0)):
            angle=90
        if (x1 != x2):
            angle = math.degrees(math.atan((y2-y1)/(x2-x1)))
            if ( x1 < x2 and angle==0):
                angle = 180
            if ( x2 < x1 and angle==0):
                angle = 0
        sum_of_poles_angles += angle
        #print("  angle for point" + str(poles[k]) + " is " + str(angle))
    #print("sum of poles: " + str(sum_of_zeros_poles)    )
    sum_angles_zeros = np.sum(sum_of_zeros_angles)
    sum_angles_poles = np.sum(sum_of_poles_angles)

    values_equation = sum_angles_zeros - sum_angles_poles - 180
    if values_equation < 0:
        values_equation += 360

    print("Angle for s=" + str(poles[i-1]) + "is:" + str(values_equation))    

for i in range(1,len(zeros)+1):
    #print("testing point is: " + str(zeros[i-1]))
    sum_of_poles_angles=0
    sum_of_zeros_angles=0
    for j in range(0,len(zeros)):
        angle=0
        x1 = np.real(zeros[i-1])
        y1 = np.imag(zeros[i-1])
        x2 = np.real(zeros[j])
        y2 = np.imag(zeros[j])
        if(x1==x2):
            angle=90
        if((x1==x2)and(y1==y2)):
            angle=0
        if (x1 != x2):
            angle = math.degrees(math.atan((y2-y1)/(x2-x1)))
            if ( x1 < x2 and angle==0):
                angle = 180
            if ( x2 < x1 and angle==0):
                angle = 0
        sum_of_zeros_angles += angle
        #print("  angle for point" + str(zeros[j]) + " is " + str(angle))
    #print("sum of angles: " + str(sum_of_zeros_angles)    )
    for k in range(0,len(poles)):
        angle=0
        x1 = np.real(zeros[i-1])
        y1 = np.imag(zeros[i-1])
        x2 = np.real(poles[k])
        y2 = np.imag(poles[k])
        if(x1==x2):
            angle=90
        if((x1==x2)and(y1==y2)):
            angle=0
        if (x1 != x2):
            angle = math.degrees(math.atan((y2-y1)/(x2-x1)))
            if ( x1 < x2 and angle==0):
                angle = 180
            if ( x2 < x1 and angle==0):
                angle = 0
        sum_of_poles_angles += angle
        #print("  angle for point" + str(poles[k]) + " is " + str(angle))
    #print("sum of poles: " + str(sum_of_zeros_poles)    )
    sum_angles_zeros = np.sum(sum_of_zeros_angles)
    sum_angles_poles = np.sum(sum_of_poles_angles)

    values_equation = (sum_angles_zeros - sum_angles_poles - 180)*-1
    if values_equation < 0:
        values_equation += 360
    print("Angle for s=" + str(zeros[i-1])+ "is: " + str(values_equation))

if len(poles) == len(zeros):
    print("There are no asymptotes")
if (len(poles) != len(zeros)):
    try:
        LugarDeAsintotas = (np.sum(poles)-np.sum(zeros))/(len(poles)-len(zeros))
        print("Lugar de las asíntotas es: " + str(np.real(LugarDeAsintotas)))
        constant=list(range(-1,10,1))
        for i in range(0,(len(poles)-len(zeros))):
            angulos_asintotas = ((2*constant[i]+1)*180)/(len(poles)-len(zeros))
        print("angulos de las asintotas: " + str(angulos_asintotas))
    except:
        print("Exception made")

omega,k,T = cval.get_jW_intersect(num,den)























