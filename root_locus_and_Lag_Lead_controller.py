import math  
import cmath  
from fpdf import FPDF
import numpy as np
from matplotlib import pyplot as plt 
import control
from sympy.solvers import solve
from sympy import Symbol
pdf = FPDF()
pdf.add_page()
pdf.set_xy(10, 10)
pdf.set_font('arial', 'B', 12.0)
pdf.cell(200, 10, "Root Locus answersheet", 0, 2, 'L')
pdf.cell(200, 10, "-José Toscano", 0, 2, 'L')
s = Symbol('s')
t = Symbol('t')
K = Symbol('K')
num2=[1,2]
den2=[1,2,3]
num4=[1]
den4=[1,6,11,6]
num1=[1]
den1=[1,5,6,0]
num3=[1,3]
den3=[1,7,14,8,0]
num5=[1]
den5=[1,3,2]
num6=[1]
den6=[1, 0, -1]

num=num6
den=den6
G = control.tf(num,den)
H = 1
G_feedbacked = control.feedback(G,H)
control.sisotool(G_feedbacked)
print(G)
print(G_feedbacked)
testing_points=[-1.5, -1.5+2j, -2+2j]
poles, zeros = control.pzmap(G, True, True)
all_points = np.concatenate([[-np.Infinity] ,zeros,poles])
all_points.sort()
all_real_points = np.real(all_points[np.isreal(all_points)])
print("Range in real axis :")
pdf.cell(60, 10, "Range in real axis :", 0, 2, 'L')
range_of_real_axis= []
for i in range(len(all_real_points)-1,0, -2):
    print("From " + str(all_real_points[i-1]) + " to " + str(all_real_points[i]))
    pdf.set_font('arial', '', 11.0)
    pdf.cell(60, 10, "From " + str(round(all_real_points[i-1])) + " to " + str(round(all_real_points[i])), 0, 2, 'L')
    range_of_real_axis += [all_real_points[i-1], all_real_points[i]]
t, y = control.step_response(G, None, 0, 0)
print("The starting points are:"+ str(poles))
pdf.set_font('arial', 'B', 12.0)
pdf.cell(200, 10, "The starting points are:", 0, 2, 'L')
pdf.set_font('arial', '', 11.0)
pdf.cell(200, 10,  str(poles), 0, 2, 'L')
print("The ending points are:" + str(zeros))
pdf.set_font('arial', 'B', 12.0)
pdf.cell(200, 10, "The ending points are:", 0, 2, 'L')
pdf.set_font('arial', '', 11.0)
pdf.cell(200, 10,  str(zeros), 0, 2, 'L')
print("The total number of branches is: " + str(len(poles)))
pdf.set_font('arial', 'B', 12.0)
pdf.cell(200, 10, "The total number of branches is: ", 0, 2, 'L')
pdf.set_font('arial', '', 11.0)
pdf.cell(200, 10,  str(len(poles)), 0, 2, 'L')
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
pdf.set_font('arial', 'B', 12.0)
pdf.cell(200, 10, "Break-away/Break-in  points are: " , 0, 2, 'L')
pdf.set_font('arial', '', 11.0)
pdf.cell(200, 10,str(breakaway_points), 0, 2, 'L')
pdf.set_font('arial', 'B', 12.0)
pdf.cell(200, 10,"The departure/arrival angles for poles/zeros are the following:", 0, 2, 'L')
pdf.set_font('arial', '', 11.0)
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
    pdf.cell(200, 10, "Angle for s=" + str(poles[i-1]) + "is:    " + str(values_equation), 0, 2, 'L')
    

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
    pdf.cell(200, 10, "Angle for s=" + str(zeros[i-1])+ "is:    " + str(values_equation), 0, 2, 'L')

pdf.set_font('arial', 'B', 12.0)
pdf.cell(200, 10, "Asymptotes:", 0, 2, 'L')
pdf.set_font('arial', '', 11.0)

if len(poles) == len(zeros):
    print("There are no asymptotes")
    pdf.cell(200, 10, "There are no asymptotes", 0, 2, 'L')
if (len(poles) != len(zeros)):
    try:
        LugarDeAsintotas = (np.sum(poles)-np.sum(zeros))/(len(poles)-len(zeros))
        print("Lugar de las asíntotas es: " + str(np.real(LugarDeAsintotas)))
        pdf.cell(200, 10, "Lugar de las asíntotas es: " + str(np.real(LugarDeAsintotas)), 0, 2, 'L')
        constant=list(range(-1,10,1))
        for i in range(0,(len(poles)-len(zeros))):
            angulos_asintotas = ((2*constant[i]+1)*180)/(len(poles)-len(zeros))
        print("angulos de las asintotas: " + str(angulos_asintotas))
        pdf.cell(200, 10,"angulos de las asintotas: " + str(angulos_asintotas), 0, 2, 'L')
    except:
        print("Exception made")

omega= control.phase_crossover_frequencies(G)
pdf.set_font('arial', 'B', 12.0)
pdf.cell(200, 10, "jW - axis crossing:", 0, 2, 'L')
pdf.set_font('arial', '', 11.0)
if (omega[0].any()) and (omega[0][0] != 0):
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
    pdf.cell(200, 10,"The jW-axis crossing occurs at: "+ str(round(omega[0][0],6)) + " with a value of K of: " + str(value_of_K[0])[0:6] , 0, 2, 'L')
    print()
else:
    control.sisotool(G)
    print("There is no crossing of the jW-axis, review sisotool plot")
    pdf.cell(200, 10,"There is no crossing of the jW-axis, review sisotool plot", 0, 2, 'L')
pdf.set_font('arial', 'B', 12.0)
pdf.cell(200, 10, "Evaluating Test points:" + str(testing_points), 0, 2, 'L')
pdf.set_font('arial', '', 11.0)
for x in range(0,len(testing_points)):
    testing_point=testing_points[x]
    angle_G_evaluated_at_testpoint=math.degrees(np.angle(control.evalfr(G, testing_point)))
    print("angle for test point: " + str(testing_point) + " is "+ str(angle_G_evaluated_at_testpoint))
    pdf.cell(200, 10,"angle for test point: " + str(testing_point) + " is "+ str(angle_G_evaluated_at_testpoint), 0, 2, 'L')
    if (((angle_G_evaluated_at_testpoint/180)%2)!= 0 and (angle_G_evaluated_at_testpoint%180 == 0)):
        print("This test point does belong to the root loccus")
        pdf.cell(200, 10,"This test point does belong to the root loccus", 0, 2, 'L')
        #find value of K for this testing point
        plant_value = control.evalfr(G, testing_point)
        value_of_K_plant = 1/abs(plant_value)
        print("the value of K corresponding to this testing point is " + str(value_of_K_plant))
        pdf.cell(200, 10,"the value of K corresponding to this testing point is " + str(value_of_K_plant), 0, 2, 'L')
    else:
        defficit = 180-angle_G_evaluated_at_testpoint
        if(defficit <= 90):
            print("this test point does not belong to the root loccus, the angle defficit is: " + str(defficit) + " degrees or " + str(math.radians(defficit)) + " radians")
            pdf.cell(200, 10,"this test point does not belong to the root loccus, the angle defficit is: " + str(defficit) + " degrees", 0, 2, 'L')
            pdf.cell(200, 10," or " + str(math.radians(defficit)) + " radians", 0, 2, 'L')
            #LEAD CONTROLLER DESIGN
            new_zero = np.real(testing_point)
            new_pole = 0
            angle_new_pole= 90 - defficit
            if angle_new_pole != 0:
                distance_pole_zero = (np.imag(testing_point)/math.tan(math.radians(angle_new_pole)))
                new_pole = new_zero - distance_pole_zero
            num_and_controler_zero = np.concatenate([[1], [-new_zero]])
            den_and_controler_pole = np.concatenate([[1], [-new_pole]])
            if new_pole == 0:
                den_and_controler_pole = 1
            if new_zero == 0:
                num_and_controler_zero = 1
            lead_controller = control.tf(num_and_controler_zero, den_and_controler_pole)
            print("LEAD CONTROLLER")
            print(lead_controller)
            pdf.set_font('arial', 'B', 12.0)
            pdf.cell(200, 10, "LEAD CONTROLLER:", 0, 2, 'L')
            pdf.set_font('arial', '', 11.0)
            if new_zero!= 0:
                pdf.cell(200, 10,"the zero of the lead controller is located in " + str(new_zero), 0, 2, 'L')
            else:
                pdf.cell(200, 10,"there is no need of an extra zero ", 0, 2, 'L')
            if new_pole != 0:
                pdf.cell(200, 10,"the pole of the lead controller is located in" + str(new_pole), 0, 2, 'L')
            else:
                pdf.cell(200, 10,"there is no need of an extra pole ", 0, 2, 'L')
            #find value of K for this testing point
            controler_and_plant = control.series(G,lead_controller)
            lead_controller_value = control.evalfr(controler_and_plant, testing_point)
            value_of_K_lead_controller = 1/abs(lead_controller_value)
            print("the value of K corresponding to this testing point is " + str(value_of_K_lead_controller))
            pdf.cell(200, 10,"the value of K corresponding to this testing point is " + str(value_of_K_lead_controller), 0, 2, 'L')
            #Steady State Error of LEAD CONTROLLER
            #Lead-Controller evaluated at s=0
            lead_at_0 = control.evalfr(lead_controller, 0)
            plant_at_0 = control.evalfr(G, 0)
            controler_and_plant_evaluated_at_0 = control.evalfr(controler_and_plant, 0)
            input_to_plant = control.tf([1],[1,0]) #step input
            s_of_FVT = control.tf([1,0],[1]) #s value of FVT
            #input_times_s_at_0 = control.evalfr(control.series(input_to_plant,s_of_FVT),0)
            if(np.isinf(controler_and_plant_evaluated_at_0)):
                error_ss=0
            else:
                error_ss = abs(1/(1+controler_and_plant_evaluated_at_0*value_of_K_lead_controller))
            print("the error of the steady state value for the lead controller is " + str(error_ss))
            pdf.cell(200, 10,"the error of the steady state value for the lead controller is " + str(error_ss), 0, 2, 'L')
            #Lag-lead controller design
            if(error_ss != 0):    
                print("LAG-LEAD CONTROLLER")
                pdf.set_font('arial', 'B', 12.0)
                pdf.cell(200, 10, "LAG-LEAD CONTROLLER:", 0, 2, 'L')
                pdf.set_font('arial', '', 11.0)
                #for an error of 10% less 
                error_lag_lead_ss = error_ss - 0.1
                x = Symbol('x')
                equation = (1/(1+x*lead_at_0*plant_at_0*value_of_K_lead_controller))-error_lag_lead_ss
                beta = solve(equation,x)
                print ("The ß of the lag-lead controller is ", str(beta[0]), "for an error of ", str(error_lag_lead_ss))
                pdf.cell(200, 10,"The ß of the lag-lead controller is " + str(beta[0]) + "for an error of " + str(error_lag_lead_ss), 0, 2, 'L')
            else: 
                print("Since the steady state is already 0 with the Lead controller, there is no need for a lag controller")
                pdf.cell(200, 10,"Since the steady state is already 0 with the Lead controller, there is no need for a lag controller", 0, 2, 'L')
        else: 
            print("Defficit is greater than 90º or π rads: we havent seen this case in class (more than one pole/zero is needed")
            pdf.cell(200, 10,"Defficit is greater than 90º or pi rads: we havent seen this case in class (more than one pole/zero is needed", 0, 2, 'L')

pdf.output('HomeWork_LeadControler_2.pdf', 'F')

        





















