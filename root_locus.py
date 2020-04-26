import math  
import cmath  
from fpdf import FPDF
import numpy as np
from matplotlib import pyplot as plt 
import control
from sympy.solvers import solve
from sympy import Symbol
s = Symbol('s')
t = Symbol('t')
K = Symbol('K')
num2=[1,2]
den2=[1,2,3]
num4=[1 ,-8,15]
den4=[1,3,2]
num1=[1]
den1=[1,3,2,0]
num3=[1,3]
den3=[1,7,14,8,0]
num5=[1]
den5=[1,3,2,0]
pdf = FPDF()
#pdf.add_page()
#pdf.set_xy(10, 10)
#pdf.set_font('arial', 'B', 12.0)
#pdf.cell(200, 10, "Root Locus answersheet", 0, 2, 'L')
#pdf.cell(200, 10, "-José Toscano", 0, 2, 'L')

num=num5
den=den5
G = control.tf(num,den)
print(G)
poles, zeros = control.pzmap(G, True, True)
all_points = np.concatenate([[-np.Infinity] ,zeros,poles])
all_points.sort()
all_real_points = np.real(all_points[np.isreal(all_points)])
print("Range in real axis :")
##pdf.cell(60, 10, "Range in real axis :", 0, 2, 'L')
range_of_real_axis= []
for i in range(len(all_real_points)-1,0, -2):
    print("From " + str(all_real_points[i-1]) + " to " + str(all_real_points[i]))
   ##pdf.set_font('arial', '', 11.0)
   ##pdf.cell(60, 10, "From " + str(round(all_real_points[i-1])) + " to " + str(round(all_real_points[i])), 0, 2, 'L')
    range_of_real_axis += [all_real_points[i-1], all_real_points[i]]
t, y = control.step_response(G, None, 0, 0)
print("The starting points are:"+ str(poles))
#pdf.set_font('arial', 'B', 12.0)
#pdf.cell(200, 10, "The starting points are:", 0, 2, 'L')
#pdf.set_font('arial', '', 11.0)
#pdf.cell(200, 10,  str(poles), 0, 2, 'L')
print("The ending points are:" + str(zeros))
#pdf.set_font('arial', 'B', 12.0)
#pdf.cell(200, 10, "The ending points are:", 0, 2, 'L')
#pdf.set_font('arial', '', 11.0)
#pdf.cell(200, 10,  str(zeros), 0, 2, 'L')
print("The total number of branches is: " + str(len(poles)))
#pdf.set_font('arial', 'B', 12.0)
#pdf.cell(200, 10, "The total number of branches is: ", 0, 2, 'L')
#pdf.set_font('arial', '', 11.0)
#pdf.cell(200, 10,  str(len(poles)), 0, 2, 'L')
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
#pdf.set_font('arial', 'B', 12.0)
#pdf.cell(200, 10, "Break-away/Break-in  points are: " , 0, 2, 'L')
#pdf.set_font('arial', '', 11.0)
#pdf.cell(200, 10,str(breakaway_points), 0, 2, 'L')

all_points_imaginary_form = np.imag(all_points[np.isreal(all_points)])

#pdf.set_font('arial', 'B', 12.0)
#pdf.cell(200, 10,"The departure/arrival angles for poles/zeros are the following:", 0, 2, 'L')
#pdf.set_font('arial', '', 11.0)
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
   ##pdf.cell(200, 10, "Angle for s=" + str(poles[i-1]) + "is:    " + str(values_equation), 0, 2, 'L')
    

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
   ##pdf.cell(200, 10, "Angle for s=" + str(zeros[i-1])+ "is:    " + str(values_equation), 0, 2, 'L')

#pdf.set_font('arial', 'B', 12.0)
#pdf.cell(200, 10, "Asymptotes:", 0, 2, 'L')
#pdf.set_font('arial', '', 11.0)

if len(poles) == len(zeros):
    print("There are no asymptotes")
   ##pdf.cell(200, 10, "There are no asymptotes", 0, 2, 'L')
if (len(poles) != len(zeros)):
    try:
        LugarDeAsintotas = (np.sum(poles)-np.sum(zeros))/(len(poles)-len(zeros))
        print("Lugar de las asíntotas es: " + str(np.real(LugarDeAsintotas)))
       ##pdf.cell(200, 10, "Lugar de las asíntotas es: " + str(np.real(LugarDeAsintotas)), 0, 2, 'L')
        constant=list(range(-1,10,1))
        for i in range(0,(len(poles)-len(zeros))):
            angulos_asintotas = ((2*constant[i]+1)*180)/(len(poles)-len(zeros))
        print("angulos de las asintotas: " + str(angulos_asintotas))
       ##pdf.cell(200, 10,"angulos de las asintotas: " + str(angulos_asintotas), 0, 2, 'L')
    except:
        print("Exception made")

omega= control.phase_crossover_frequencies(G)
#pdf.set_font('arial', 'B', 12.0)
#pdf.cell(200, 10, "jW - axis crossing:", 0, 2, 'L')
#pdf.set_font('arial', '', 11.0)
if omega[0][0] != 0:
    s=omega[0][0]*1j
    power=0
    num_with_values = []
    den_with_values =[]
    for i in range(len(num),0,-1):
        num_with_values += [(num[i-1]*K*s**power)]
        power +=1
    power=0
    for i in range(len(den),0,-1):
        den_with_values += [(den[i-1]*s**power)]
        power +=1
    all_elements = np.concatenate([num_with_values,den_with_values])
    value_of_K = np.real(solve(np.sum(all_elements), K))
    print("The jW-axis crossing occurs at: "+ str(round(omega[0][0],6)) + " with a value of K of: " + str(value_of_K[0])[0:7])
   ##pdf.cell(200, 10,"The jW-axis crossing occurs at: "+ str(round(omega[0][0],6)) + " with a value of K of: " + str(value_of_K[0])[0:6] , 0, 2, 'L')
    print()
else:
    control.sisotool(G)
    print("There is no crossing of the jW-axis, review sisotool plot")
   ##pdf.cell(200, 10,"There is no crossing of the jW-axis, review sisotool plot", 0, 2, 'L')
#f = plt.figure()
#control.sisotool(G)
#plt.show()
#pdf.output('control_root_locus_4.pdf', 'F')

testing_point = -0.5+1j
for i in range(1,2):
    #print("testing point is: " + str(poles[i-1]))
    sum_of_poles_angles=0
    sum_of_zeros_angles=0
    for j in range(0,len(zeros)):
        angle=0
        x1 = np.real(testing_point)
        y1 = np.imag(testing_point)
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
        if angle < 0:
            angle = 180-abs(angle) 
        sum_of_zeros_angles += angle
        print("  angle for point" + str(zeros[j]) + " is " + str(angle))
    print("sum of zeros: " + str(sum_of_zeros_angles)    )
    for k in range(0,len(poles)):
        angle=0
        x1 = np.real(testing_point)
        y1 = np.imag(testing_point)
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
        if angle < 0:
            angle = 180-abs(angle) 
        sum_of_poles_angles += angle
        print("  angle for point" + str(poles[k]) + " is " + str(angle))
    print("sum of poles: " + str(sum_of_poles_angles)    )
    sum_angles_zeros = np.sum(sum_of_zeros_angles)
    sum_angles_poles = np.sum(sum_of_poles_angles)
    angle_of_testing_point = sum_angles_zeros - sum_angles_poles
    if angle_of_testing_point < 0:
        angle_of_testing_point += 360

    print("Angle for testing point " + str(testing_point) + "is:" + str(angle_of_testing_point))
    if (angle_of_testing_point/180)%2 == 1:
        print("the point" + str(testing_point) + " does belong to the root loccus")
    else:
        print((angle_of_testing_point/180)%1)
        angle_defficit = 180-((angle_of_testing_point/180)%1 * 180)
        print("the point" + str(testing_point) + " does not belong to the root loccus. The angle deficit is: " + str(angle_defficit) + " degrees, or " + str(round(math.radians(angle_defficit),4)) + " radians.")

#Lead Controler Design
new_zero = np.real(testing_point)
angle_new_pole= 90 - angle_defficit
distance_pole_zero = (np.imag(testing_point)/math.tan(math.radians(angle_new_pole)))
new_pole = new_zero - distance_pole_zero
print("The zero of the Lead Controler is in S=" +str(new_zero))
print("The pole of the Lead Controler is in S=" +str(new_pole))
#evaluate G*Controler and find magnitude
num_evaluated=1
den_evaluated=1
num_and_controler_zero = np.concatenate([zeros, [new_zero]])
den_and_controler_pole = np.concatenate([poles, [new_pole]])
for i in range(0,len(num_and_controler_zero)):
    real_part = -np.real(num_and_controler_zero[i])+np.real(testing_point)
    imag_part = -np.imag(num_and_controler_zero[i])+np.imag(testing_point)
    sum_value = np.complex(real_part,imag_part)
    num_evaluated *= sum_value
    #print(num_evaluated)
for i in range(0,len(den_and_controler_pole)):
    real_part = -np.real(den_and_controler_pole[i])+np.real(testing_point)
    imag_part = -np.imag(den_and_controler_pole[i])+np.imag(testing_point)
    sum_value = np.complex(real_part,imag_part)
    den_evaluated *= sum_value
    #print(den_evaluated)
G_evaluated_testpoint = num_evaluated/den_evaluated
controller = control.tf([1, -new_zero],[1,-new_pole])
lead_controller = control.series(G,controller)
print(lead_controller)
response = control.evalfr(lead_controller, testing_point)
value_of_K_testing_point = round(1/abs(response),4)
magnitud_K = (1/abs(response))
print(magnitud_K)

