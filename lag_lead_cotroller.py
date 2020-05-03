import argparse
import numpy as np
import control, math
from matplotlib import pyplot as plt 
from sympy import Symbol
from sympy.solvers import solve
#LEAD CONTROLLER DESIGN

def generate_lead_controller(G,testing_point):
    angle_G_evaluated_at_testpoint=math.degrees(np.angle(control.evalfr(G, testing_point)))
    defficit = 180-angle_G_evaluated_at_testpoint
    if defficit <90:
        new_zero = np.real(testing_point)
        angle_new_pole= 90 - defficit
    else:
        new_zero = 0
        angle_new_zero=math.degrees(np.angle(control.evalfr(control.series(control.tf([1,0],1),G),testing_point)))
        if angle_new_zero<0:
            angle_new_pole= 180 + angle_new_zero
        else: 
            angle_new_pole= -180 - angle_new_zero
    distance_pole_zero = (np.imag(testing_point)/math.tan(math.radians(angle_new_pole)))
    new_pole = np.real(testing_point) - distance_pole_zero
    if new_zero == 0:
        num_and_controler_zero = 1
    num_and_controler_zero = np.concatenate([[1], [-new_zero]])
    den_and_controler_pole = np.concatenate([[1], [-new_pole]])
    lead_controller = control.tf(num_and_controler_zero, den_and_controler_pole)
    return lead_controller

def get_value_of_K(controller, testing_point, G):
    controler_and_plant = control.series(G,controller)
    lead_controller_value = control.evalfr(controler_and_plant, testing_point)
    value_of_K_lead_controller = 1/abs(lead_controller_value)
    return value_of_K_lead_controller

def get_steady_state_error(system):
    controler_and_plant_evaluated_at_0 = control.evalfr(system, 0)
    if(np.isinf(controler_and_plant_evaluated_at_0)):
        return 0
    else:
        return abs(1/(1+controler_and_plant_evaluated_at_0*value_of_K_lead_controller))

def lag_controller_design(error, percentage_to_reduce, lead_controller, G, K_lead):
    lead_at_0 = control.evalfr(lead_controller, 0)
    plant_at_0 = control.evalfr(G, 0)
    error_lag_lead_ss = error_ss - percentage_to_reduce
    x = Symbol('x')
    equation = (1/(1+x*control.evalfr(control.series(lead_controller, G),0)*K_lead))-error_lag_lead_ss
    return solve(equation,x), error_lag_lead_ss
                

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='lag_controller', description='Propone un controlador en adelanto, su K correspondiente y el valor del error del estado estable')
    parser.add_argument(
        '--num_G', nargs="+",help='Coeficientes del numerador de la función de transferencia', required=True, type=int)
    parser.add_argument(
        '--den_G',  nargs="+",help='Coeficientes del denominador de la función de transferencia', required=True, type=int)
    parser.add_argument(
        '--test_point', nargs="+", help='FORMATO: -2 2j ->Punto que queremos agregar al root loccus ', action="store", required=True, type=complex )
    args = parser.parse_args()
    G = control.tf(args.num_G,args.den_G)
    testing_point = np.sum(args.test_point)
    lead_controller = generate_lead_controller(G,testing_point)
    print("-------------------PLANT-------------------")
    print(G)
    print("---------------LEAD CONTROLLER-------------")
    print(lead_controller)
    #find value of K for this testing point
    value_of_K_lead_controller = get_value_of_K(lead_controller,testing_point,G)
    print("the VALUE OF K corresponding to this testing point is " + str(value_of_K_lead_controller))
    #Steady State Error of LEAD CONTROLLER
    error_ss= get_steady_state_error(control.series(G,lead_controller))
    print("the STEADY STATE ERROR for the lead controller is " + str(error_ss))
    print("-----------LAG-LEAD CONTROLLER-----------")
    beta, error_lag_lead_ss = lag_controller_design(error_ss, 0.1, lead_controller, G, value_of_K_lead_controller)
    print ("The ß of the lag-lead controller is ", str(beta), "for an error of ", str(error_lag_lead_ss))
