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
print("Tm =",Tm)


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
for i in p:
    rho.append(i/(R*T[p.index(i)]))

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
plt.subplot(211)
plt.plot(alpha,Cl)

plt.subplot(212)
plt.plot(Cl2,Cd)
plt.show()

# =============================================================================
# dy = max(Cd) - min(Cd)
# dx = max(Cl2)-min(Cl2)
# slope = dy/dx
# =============================================================================
dy = []
dx = []
for i in range(len(Cd)-1):
    dy.append( Cd[i+1]-Cd[i])
    dx.append( Cl2[i+1]-Cl2[i])
