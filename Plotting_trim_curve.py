from DataImport import *
import math as m
import matplotlib.pyplot as plt
from PyThrust import *

data = importData("FTISxprt-20190319_100832.mat")
data.printVariables()
d = 0.686 #diameter JT15D-4 engine in m
Cm_Tc = -0.0064
p0 = 101325.         
rho0 = 1.225
labda = -0.0065         
T0 = 288.15         
R = 287.058
g0 = 9.80665        
gamma = 1.4
Ws = 60500.     
Ts_per_engine = [(2021.01, 2339.69),(2066.55, 2366.19),(2080.34, 2400.34),(2142.15, 2462.07),(1979.23, 2291.18),(1964.18, 2278.94),(1920.19, 2236.73)]
Ts = []
for i in Ts_per_engine:
    Ts.append(sum(i))
    
S = 30. #m^2

t = [1905., 1975., 2037., 2100., 2207., 2278., 2345.]
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

F_used_lbs = [592.,613.,624.,638.,665.,679.,699.]

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
aoa_deg = [5.,5.9,6.9,7.9,4.2,3.6,3.4]
aoarad = []
for i in aoa_deg:
    aoarad.append(m.radians(i))
de_eq_meas = [-0.02,-0.7,-1.1,-1.7,0.2,0.4,0.7]
Fe_aer_excl = [1.,-19.,-30.,-46.,25.,48.,80.]
hpft = [10500.,10640.,10750.,10930.,10040.,9740.,9250.]            #pressure height
hp = []
for i in hpft:
    a = i*0.3048
    hp.append(a)
Vckts = [159.,149.,141.,130.,170.,180.,189.] #calibrated speed in knots
Vc = []
for i in Vckts:
    a = i*0.514444
    Vc.append(a)
print(Vc)

TATC = [-6.8,-7.5,-7.8,-8.2,-5.5,-4.8,-4.] 
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
    
    
dx_cg = -0.0308464425
dd_e = ((-0.8- (- 0.2) ) *m.pi )/180  #change in deflection elevator
Cn = []
for i in W:
    Cn.append(i/(0.5*rho[W.index(i)]*(Ve_bar[W.index(i)]**2)*S ))
c_bar = 2.0569
Cm_d = []
for i in Cn:
    a = (-1/dd_e)*i*(dx_cg/c_bar)
    Cm_d.append(a)
Fe_aer = []
for i in Fe_aer_excl:
    Fe_aer.append(i * (Ws/W[Fe_aer_excl.index(i)])) #Getting from Fe_aer to Fe*_aer 
#Elaborate why Fe_f = 0 in report

plt.show

Thrust = []
for i in t:
    Thrust.append(thrust(i,data))
Tc = []
for i in Ve_bar:
    Tc.append( (Thrust[Ve_bar.index(i)][0] + Thrust[Ve_bar.index(i)][1]) / (0.5 * rho[Ve_bar.index(i)] * (i**2) * (d**2) ))
Tcs = []
for i in Ts:
    Tcs.append(i/(0.5*rho[Ts.index(i)] * (Ve_bar[Ts.index(i)]**2)*(d**2)))

Cm_d = -1.5429544597341283
d_eq = []
for i in Tcs:
    d_eq.append(m.radians(de_eq_meas[Tcs.index(i)]) - (1./(Cm_d))*Cm_Tc * (i - Tc[Tcs.index(i)]))
dy = min(d_eq) - max(d_eq)
dx = max(aoarad)-min(aoarad)
dde_dalpha = dy/dx

Cm_alpha = dde_dalpha*(-Cm_d)


aoa = []
for a in aoarad:
    aoa.append((a*180)/(m.pi))
plt.figure(1)
#plt.subplot(311)
plt.plot(sorted(Ve_bar),sorted(Fe_aer),"go")
plt.plot(sorted(Ve_bar),sorted(Fe_aer),"g")
plt.title("Elevator force curve")
plt.ylabel("Elevator force [N]")
plt.xlabel("Reduced equivalent airspeed [m/s]")
plt.show()
plt.figure(2)
#plt.subplot(312)
plt.plot(sorted(Ve_bar),sorted(d_eq),"ro")
plt.plot(sorted(Ve_bar),sorted(d_eq),"r")
plt.ylabel("Elevator deflection angle [rad]")
plt.title("Elevator trim curve")
plt.xlabel("Reduced equivalent airspeed [m/s]")
plt.show()
#plt.subplot(313)
plt.figure(3)
plt.plot(sorted(aoa),sorted(d_eq)[::-1],"o")
plt.plot(sorted(aoa),sorted(d_eq)[::-1],"b")
plt.xlabel("Angle of attack [deg]")
plt.ylabel("Elevator deflection angle [rad]")
plt.title("Elevator deflection vs. angle of attack")
plt.show()


