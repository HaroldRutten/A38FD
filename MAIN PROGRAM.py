import math as m
import matplotlib.pyplot as plt
p0 = 101325.         
rho0 = 1.225
labda = -0.0065         
T0 = 288.15         
R = 287.058
g0 = 9.80665        
gamma = 1.4
Ws = 60500.     
F_used_lbs = [664.,694.,730.,755.,798.,825.,846.]

F_used_kg = []
for i in F_used_lbs:
    a = i*0.453592
    F_used_kg.append(a)

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

pilot1 = 95. #kg
pilot2 = 92.
coordinator = 74.
observer_1L = 66.
observer_1R = 61.
observer_2L = 75.
observer_2R = 78.
observer_3L = 86.
observer_3R = 68.
Payload = [pilot1,pilot2,coordinator,observer_1L, observer_1R,observer_2L,observer_2R,observer_3L,observer_3R]
Wp_kg = sum(Payload) #kg

#============================FUEL==================================================



block = 4050.*0.453592 #kg
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
hpft = [6060.,6350.,6550.,6880.,6160.,5810., 5310.]            #pressure height
hp = []
for i in hpft:
    a = i*0.3048
    hp.append(a)
Vckts = [161,150,140,130,173,179,192] #calibrated speed in knots
Vc = []
for i in Vckts:
    a = i*0.514444
    Vc.append(a)
print(Vc)

TATC = [5.5,4.5,3.5,2.5,5.0,6.2,8.2] 
Tm = []
for i in TATC:
    Tm.append(i+273.15)
print("Tm =",Tm)

F_used_lbs = 360.
F_used_kg = F_used_lbs * 0.453592
d_eq_meas = 2.8     #UP FOR DISCUSSION THIS LAST ONE
Fe_aer_excl = [0.,-23.,-29.,-46.,26.,40.,83.]

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
for i in p:
    rho.append(i/(R*T[p.index(i)]))

Ve = []
for i in Vt:
    Ve.append(i*m.sqrt(rho[Vt.index(i)]/rho0))

Ve_bar = []
for i in W:
    Ve_bar.append(Ve[W.index(i)]*m.sqrt(Ws/i))
# ===================================Determining ==========================================



# 
# =============================================================================

#===================================FORCE CURVE===========================================
Fe_aer = []
for i in Fe_aer_excl:
    Fe_aer.append(i * (Ws/W[Fe_aer_excl.index(i)]))  #Getting from Fe_aer to Fe*_aer 
#Elaborate why Fe_f = 0 in report

plt.plot(Ve_bar,Fe_aer)
plt.show

#t = [2239.,2240.,2484.,2576.,2741.,2840.,2920.]
#plt.plot(t,Fe_aer)
#plt.show

