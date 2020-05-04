import control
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
import argparse
K = Symbol('K')

def get_PID_coefficients(Ku, Tu):
    Kp = 0.6*Ku
    Ki = 1.2*Ku/Tu
    Kd = 0.075*Ku*Tu
    return Kp, Ki, Kd

def get_P_coefficients(Ku, Tu):
    Kp = 0.5*Ku
    Ki = 0
    Kd = 0
    return Kp, Ki, Kd

def get_PI_coefficients(Ku, Tu):
    Kp = 0.45*Ku
    Ki = 0.54*Ku/Tu
    Kd = 0
    return Kp, Ki, Kd

def get_PD_coefficients(Ku, Tu):
    Kp = 0.8*Ku
    Ki = 0
    Kd = 0.1*Ku*Tu
    return Kp, Ki, Kd

def get_Pessen_Integration_coefficients(Ku, Tu):
    Kp = 0.7*Ku
    Ki = 1.75*Ku/Tu
    Kd = 0.105*Ku*Tu
    return Kp, Ki, Kd

def get_Some_Overshoot_coefficients(Ku, Tu):
    Kp = Ku/3
    Ki = ((2/3)*Ku)/Tu
    Kd = ((1/9)*Ku)/Tu
    return Kp, Ki, Kd

def get_No_Overshoot_coefficients(Ku, Tu):
    Kp = 0.2*Ku
    Ki = ((2/5)*Ku)/Tu
    Kd = ((1/15)*Ku)/Tu
    return Kp, Ki, Kd

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Ziegler_Nichols_Method', description='Returns the coefficients for a classic PID, PI or PD controller')
    parser.add_argument(
        '-Ku', '--Ku', help='Value of K for the jW-axis crossing', required=True, type=float)
    parser.add_argument(
        '-Tu','--Tu', help='Oscilation period', required=True, type=float)
    parser.add_argument(
        '--type',  help='Type of controller', required=True, type=str, choices=['PID', 'P', 'PI', 'PD', 'PessenInegration', 'SomeOvershoot', 'NoOvershoot' ])
    args = parser.parse_args()
    controller = {
        'PID': get_PID_coefficients,
        'P': get_P_coefficients,
        'PI': get_PI_coefficients,
        'PD': get_PD_coefficients,
        'PessenInegration': get_Pessen_Integration_coefficients,
        'SomeOvershoot': get_Some_Overshoot_coefficients,
        'NoOvershoot': get_No_Overshoot_coefficients,
    }
    Kp, Ki, Kd = controller[args.type](args.Ku,args.Tu)
    print ("The coefficient for a ", args.type , " controller are: ", "Kp = ", Kp , "Ki = ", Ki, "Kd = ", Kd)
    
