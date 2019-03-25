# -*- coding: utf-8 -*-

#Mass and balance form##

t = 0
ff = 0.5
f0 = 2800*.456
bem = 9000.
npax = 10
fuelmom0 = 14320.34


#--------payload-----------#

np = 400
cp = 400

#passengers = [90,90,90,90,90,90,90,90,90]
passengers = []
for i in range(npax-1):
    passengers.append(float(input('enter passenger "'+str(i)+'" weight:   ')))
    #5print(passengers)
    
##-----payload mass----####
pas = sum(passengers)
plw = pas+np+cp

#--- moment arms---#
seatloc = [131,131,214,214,251,251,288,288,170] 
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
    m = m*9.81
    
    payloadmom.append(m)
    print(payloadmom)
##total payload moment####
plm = sum(payloadmom)
## acting at ##
xpl = plm/(plw*9.81)

  
#----------BEM ------#

xcgbem = 7.5

bemm = xcgbem*bem*9.81

# -------ZFM ---------#

xcgzfm = (bemm+plm)/(bem+plw)

# ------ fuel weight ----#

#current fuel weight:
fused = float(input('fuel used:'))
fatm = f0 - fused*.456

fatmpounds = fatm/.456

xcgfuel0 = fuelmom0/f0

print('current fuel mass in pounds is', fatmpounds)
fuelmoment = float(input('enter current fuel moment from table'))
xcgfuel = fuelmoment/fatmpounds

fuelmoment = fuelmoment*.456/0.0254
# --- total balance --- #
#print(bemm)
#print(fuelmoment)
#print(plm)
moment = bemm+plm+fuelmoment
mass = fatm+bem+plw
xcg = moment/(mass*9.81)

print('the moment is ', moment,'n/m')
print('the mass is ', mass,' kg')
print('the center-of-gravity is located at', xcg,' m')


5












