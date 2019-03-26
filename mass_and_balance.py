# -*- coding: utf-8 -*-

#Mass and balance form##

t = 0
ff = 0.5
f0 = 2800.*.453592
bem = 9165.*.453592
npax = 10
fuelmom0 = 14320.34


#--------payload-----------#

np = 0
cp = 220*.453592

passengers = [93,89,75,85,74.5,75,83,90.5,140]
#passengers = []
#for i in range(npax-1):
 #   passengers.append(float(input('enter passenger "'+str(i)+'" weight:   ')))
    #5print(passengers)
    
##-----payload mass----####
pas = sum(passengers)
plw = pas+np+cp

#--- moment arms---#
seatloc = [131,131,214,214,251,251,288,150,170] 
for i in range(len(seatloc)):
    seatloc[i] = seatloc[i]*0.0254
xnp = 74*0.0254
xcp = 321*0.0254
### -- payload moments ---##
payloadmom = []
for i in range(npax+1):
    print(i)
    if i == 9:
        m = xnp*np
    elif i == 10:
        m = xcp*cp
    else: 
        m = float(seatloc[i])*float(passengers[i])
    m = m*9.80665
    
    payloadmom.append(m)
    print(payloadmom)
##total payload moment####
plm = sum(payloadmom)
#print('payloadmom',plm)
#print('payload weight',plw)
## acting at ##
xpl = plm/(plw*9.80665)
#print('payload cg',xpl)
  
#----------BEM ------#

xcgbem = 7.421372

bemm = xcgbem*bem*9.80665

# -------ZFM ---------#

print('zero fuel moment xcg',xcgzfm)
# ------ fuel weight ----#

#current fuel weight:
fused = float(input('fuel used:'))
fatm = f0 - fused*.453592

fatmpounds = fatm/.453592
print(fatmpounds)
xcgfuel0 = fuelmom0/f0

print('current fuel mass in pounds is', fatmpounds)
fuelmoment = float(input('enter current fuel moment from table'))
xcgfuel = fuelmoment/fatmpounds
print(xcgfuel)
fuelmoment = fuelmoment*.11298
# --- total balance --- #
#print(bemm)
#print(fuelmoment)
#print(plm)
moment = bemm+plm+fuelmoment
mass = fatm+bem+plw
xcg = moment/(mass*9.80665)

print('the moment is ', moment,'n/m')
print('the mass is ', mass,' kg')
print('the center-of-gravity is located at', xcg,' m')


5












