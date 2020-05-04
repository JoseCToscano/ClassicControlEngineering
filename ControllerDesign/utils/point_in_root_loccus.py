import argparse
import numpy as np
import control, math
from matplotlib import pyplot as plt 

def get_value_of_K(testing_point, G):
    plant_value = control.evalfr(G, testing_point)
    value_of_K = 1/abs(plant_value)
    return value_of_K

def find_angle (testing_point, G):
    degrees =math.degrees(np.angle(control.evalfr(G, testing_point)))
    radians = math.radians(degrees)
    return radians, degrees





if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='point_in_root_loccus', description='Propone un controlador en adelanto, su K correspondiente y el valor del error del estado estable')
    parser.add_argument(
        '--num_G', nargs="+",help='Coeficientes del numerador de la función de transferencia', required=True, type=int)
    parser.add_argument(
        '--den_G',  nargs="+",help='Coeficientes del denominador de la función de transferencia', required=True, type=int)
    parser.add_argument(
        '--test_point', nargs="+", help='FORMATO: -2 2j ->Punto que queremos agregar al root loccus ', action="store", required=True, type=complex )
    args = parser.parse_args()
    G = control.tf(args.num_G,args.den_G)
    testing_point = np.sum(args.test_point)
    radians, degrees = find_angle(testing_point, G)
    if (((degrees/180)%2)!= 0 and (degrees%180 == 0)):
        K= get_value_of_K(testing_point, G)
        print("This test point does belong to the root loccus with a value of K = ", K)
    else: 
        defficit = np.pi - radians
        if (defficit > np.pi):
            defficit -= np.pi
        print("This test point does not belong to the root loccus, the angle defficit is ", defficit , " rad or ", math.degrees(defficit), " degrees.")


