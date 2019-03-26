from DataImport import *
import math as m
import matplotlib.pyplot as plt
from PyThrust import *

data = importData("FTISxprt-20190319_100832.mat")
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

F_used_lbs = [717.,739.]

F_used_kg = []
for i in F_used_lbs:
    a = i*0.453592
    F_used_kg.append(a)

block = 2800.*0.453592 #kg
Wfuel_kg =[]
for i in F_used_kg:
    Wfuel_kg.append(block - i)

W = [] #Weights for "shift in center of gravity" in EXCEL
for i in F_used_kg:
    W.append((Wempty_kg + Wp_kg+ (block - i))*g0)
# =============================================================================
#     
# ===================================EXCEL VARIABLES==========================================
Fe_aer_excl = [1.,-31.]
t = [2422.,2507.]

hpft = [9630.,9690.]            #pressure height
hp = []
for i in hpft:
    a = i*0.3048
    hp.append(a)
Vckts = [160.,159.] #calibrated speed in knots
Vc = []
for i in Vckts:
    a = i*0.514444
    Vc.append(a)


TATC = [-6.,-0.8] 
Tm = []
for i in TATC:
    Tm.append(i+273.15)
p = []
for i in hp:
    a = p0*(1+((labda*i)/T0))**(-g0/(labda*R))
    p.append(a)

M = []
for i in p:
    a = m.sqrt((2/(gamma-1)) * ((1+(p0/i)*((1+((gamma-1)/(2*gamma))*(rho0/p0)* Vc[p.index(i)]**2)**(gamma/(gamma-1))-1))**((gamma-1)/gamma)-1))
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
    
    

dx_cg = -0.04303655
dd_e = ((-0.8- (- 0.2) ) *m.pi )/180  #change in deflection elevator
Cn = []
for i in W:
    Cn.append(i/(0.5*rho[W.index(i)]*(Ve_bar[W.index(i)]**2)*S ))
c_bar = 2.0569
Cm_d = []
for i in Cn:
    a = (-1/dd_e)*i*(dx_cg/c_bar)
    Cm_d.append(a)

Thrust = []
for i in t:
    Thrust.append(thrust(i,data))
