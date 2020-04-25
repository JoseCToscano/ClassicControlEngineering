import control
print("Code started")

num=[1]
den=[1,3,2]
sys1 = control.tf(num, den)
print(sys1)
