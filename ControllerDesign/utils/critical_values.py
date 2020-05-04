import control
import numpy as np
from sympy.solvers import solve
from sympy import Symbol
import argparse
K = Symbol('K')

def get_jW_intersect(num, den):
    G = control.tf(num,den)
    omega= control.phase_crossover_frequencies(G)
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
        T=(2*np.pi)/(omega[0][0])
        print("The jW-axis crossing occurs at: "+ str(round(omega[0][0],6)) + " with a value of K of: " + str(value_of_K[0])[0:7], "the critical period is T = ", T)
    else:
        value_of_K="No value of K",
        T= "No value of T",
        omega = "Non existent"
        print("There is no crossing of the jW-axis, review sisotool plot")
    return omega, value_of_K, T

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='critical_values', description='Gets the critical values of K, W and the corresponding T (period)')
    parser.add_argument(
        '--num_G', nargs="+",help='Coefficients of the numerator of the transfer function', required=True, type=int)
    parser.add_argument(
        '--den_G',  nargs="+",help='Coefficients of the denomintor of the transfer function', required=True, type=int)
    args = parser.parse_args()
    omega, K, T = get_jW_intersect(args.num_G,args.den_G)

    
