# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 00:06:22 2019

@author: Harold
"""
from DataImport import *
import math as m
import matplotlib.pyplot as plt
from PyThrust import *

data = importData("FTISxprt-20190319_100832.mat")
#data = importData("Refdata.mat")
data.printVariables()

p0 = 101325.         
rho0 = 1.225
labda = -0.0065         
T0 = 288.15         
R = 287.058
g0 = 9.80665        
gamma = 1.4
Ws = 60500.
S = 30. #m^2
b = 15.911
AR = (b**2)/30.
# EXCEL VARIABLES=============================================================================

F_used_lbs = [360.,400.,435.,466.,503.,530.]
hpft = [10500.,10500.,10500.,10500.,10500.,10550.]            #pressure height
Vckts = [250.,220.,192.,157.,130.,114.] #calibrated speed in knots
TATC = [0,-3.2,-5.2,-8,-9.2,-9.8] 
t = [989., 1103., 1230., 1370., 1533., 1664.]
alpha = [1.4, 2.1, 3.1, 5.1, 8.3, 10.9]

# Conversions=============================================================================
F_used_kg = []
for i in F_used_lbs:
    a = i*0.453592
    F_used_kg.append(a)
    
#==============================================================================
# #     ================                  WEIGHTS =================                    ##
# 
#=========================Empty Mass=====================================================
Wempty_lbs = 9165.
Wempty_kg = Wempty_lbs * 0.453592
Wempty = Wempty_kg * g0
# 
#============================PAYLOAD==================================================

pilot1 = 93. #kg
pilot2 = 89.
coordinator = 140.
observer_1L = 75.
observer_1R = 85.
observer_2L = 74.5
observer_2R = 75.
observer_3L = 83.
observer_3R = 90.5
Payload = [pilot1,pilot2,coordinator,observer_1L, observer_1R,observer_2L,observer_2R,observer_3L,observer_3R]
Wp_kg = sum(Payload) #kg
Wp_kg = 904.79
#============================FUEL==================================================



block = 2800*0.453592 #kg
Wfuel_kg =[]
for i in F_used_kg:
    Wfuel_kg.append(block - i)



#==================================================================================================
W_kg = []
for i in Wfuel_kg:
    W_kg.append(Wempty_kg+Wp_kg+i)

W = []
for i in W_kg:
    W.append(i*9.80665)
print(W)


#==================================================================================================#
#=========================

hp = []
for i in hpft:
    a = i*0.3048
    hp.append(a)

Vc = []
for i in Vckts:
    a = i*0.514444
    Vc.append(a)
print(Vc)


Tm = []
for i in TATC:
    Tm.append(i+273.15)

p = []
for i in hp:
    a = p0*(1+((labda*i)/T0))**(-g0/(labda*R))
    p.append(a)

M = []
for i in Vc:
    a = m.sqrt((2/(gamma-1)) * ((1+(p0/p[Vc.index(i)])*((1+((gamma-1)/(2*gamma))*(rho0/p0)* i**2)**(gamma/(gamma-1))-1))**((gamma-1)/gamma)-1))
    M.append(a)

T = []
for i in Tm:
    a = i/(1+((gamma-1)/2)*M[Tm.index(i)]**2)
    T.append(a)
    
a = []
for i in T:
    b= m.sqrt(gamma*R*i)
    a.append(b)

Vt = []
for i in a:
    b = i*M[a.index(i)]
    Vt.append(b)

rho = []
for i in range(len(p)):
    rho.append(p[i]/(R*T[i]))

Ve = []
for i in Vt:
    Ve.append(i*m.sqrt(rho[Vt.index(i)]/rho0))

Ve_bar = []
for i in W:
    Ve_bar.append(Ve[W.index(i)]*m.sqrt(Ws/i))
    

Thrust = []
for i in t:
    Thrust.append(thrust(i,data))


Cl = []
for i in Ve_bar:
    Cl.append((W[Ve_bar.index(i)])/(0.5*rho[Ve_bar.index(i)]*(i**2)*S))

Cd = []
for i in Ve_bar:
    Cd.append((Thrust[Ve_bar.index(i)][0] + Thrust[Ve_bar.index(i)][1])/(0.5*rho[Ve_bar.index(i)]*((i)**2)*S))

Cl2 = []
for i in Cl:
    Cl2.append(i**2)

plt.figure(1)
#plt.subplot(211)
plt.plot(alpha,Cl,"go")
plt.plot(alpha,Cl,"g")
plt.xlabel("Angle of attack [deg]")
plt.ylabel("Lift Coefficient")
plt.title("Lift Coefficient vs. Angle of Attack")
plt.show()

plt.figure(2)
#plt.subplot(212)
plt.plot(Cl2,Cd,"ro")
plt.plot(Cl2,Cd,"r")
plt.xlabel("Lift Coefficient Squared")
plt.ylabel("Drag Coefficient")
plt.title("Drag Coefficient vs. Lift Coefficient Squared")
plt.show()

plt.figure(3)
#plt.subplot(212)
plt.plot(alpha,Cd,"bo")
plt.plot(alpha,Cd,"b")
plt.xlabel("Angle of attack [deg]")
plt.ylabel("Drag Coefficient")
plt.title("Drag Coefficient vs. Angle of Attack")
plt.show()
# =============================================================================
# dy = max(Cd) - min(Cd)
# dx = max(Cl2)-min(Cl2)
# slope = dy/dx
# =============================================================================
dy = []
for i in range(len(Cd)-1):
    dy.append(Cd[i+1] - Cd[i])
dx = []
for i in range(len(Cd)-1):
    dx.append(Cl2[i+1] - Cl2[i])
dY = np.average(dy)
dX = np.average(dx)
slope = dY/dX

dyy = max(Cl) - min(Cl)
dxx = max(alpha) - min(alpha)
dCl_dalpha = dyy/dxx

e = (1/slope)/(AR*m.pi)
CD_0 = []
for i in range(len(Cd)):
    CD_0.append( (Cd[i] - Cl2[i]*slope) )
Cd0 = np.average(CD_0)
CdC = []
for i in Cl:
    CdC.append(Cd0 + (i**2)/(m.pi*S*e))
    
plt.figure(4)
plt.plot(Cd,Cl,"mo", label="Measured Cd")
plt.plot(Cd,Cl,"m")
plt.plot(CdC,Cl,"ko", label="Linearized Cd")
plt.plot(CdC,Cl,"k")
plt.xlabel("Drag Coefficient")
plt.ylabel("Lift Coefficient")
plt.title("Drag Polar")
plt.show()
#for i in range(len(Cd)-1):
#==============================================================================

# for i in Cd:
#     if i == 5:
#         
#     else:        
#         dy.append( Cd[Cd.index(i)+1]-Cd[Cd.index(i)])
#     dx.append( Cl2[Cd.index(i)+1]-Cl2[Cd.index(i)])
# 
#==============================================================================

#==============================================================================
# for i in Cd:
#     if Cd.index(i) <5:
#         dy.append(Cd[Cd.index(i)+1] - Cd[Cd.index(i)])
#         dx.append(Cl2[Cd.index(i)+1] - Cl2[Cd.index(i)])
#     else: 
#         break
# slopes = []
# for i in dy:
#     slopes.append(i/(dx[dy.index(i)]))
# avg = sum(slopes)/len(slopes)
# 
#==============================================================================



    