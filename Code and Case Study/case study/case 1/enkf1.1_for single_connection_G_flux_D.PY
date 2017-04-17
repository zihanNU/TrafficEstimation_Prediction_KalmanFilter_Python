import os
from numpy import *
datapath = r'C:\Users\hong\Desktop\master thesis\200411'

def get_measurement(count):          # get measurement
    csv9=['0411_27.csv', '0411_28.csv','0411_29.csv', '0411_30.csv', '0411_31.csv',  '0411_33.csv',  '0411_34.csv','0411_35.csv', '0411_37.csv']
    csv7=['0411_27.csv', '0411_29.csv', '0411_30.csv', '0411_31.csv',  '0411_34.csv', '0411_35.csv', '0411_37.csv']
    csv5=['0411_27.csv', '0411_29.csv', '0411_31.csv', '0411_34.csv', '0411_37.csv']
    y=[]
    for csv in csv9:
        # reverse
        file_y=open(datapath+'\\'+csv,'r')
        lines=file_y.readlines()
        for i in range ((count-1)*T+3392,count*T+3392):
            linearray=lines[i].split(',')
            y.append(float(linearray[5]))
    file_y.close()
    return array(y).reshape(9,1)

def initial(): # intialize the EnKF with the v_mean and v_variance
    v_mean=[]
    v_variance=[]
    file_ini=open('meanvariance.csv','r')
    lines=file_ini.readlines()
    for i in range(len(lines)):
        linearray=lines[i].split(',')
        v_mean.append(float(linearray[0]))
        v_variance.append(float(linearray[1]))
##    print v_mean
    file_ini.close()
    return array(v_mean).reshape(20,1),array(v_variance).reshape(20,1)

def get_velocity(rho):  # get the forecast velocity
    v=[]
    for i in range(cellnumber):
        if rho[i]<=rhoc:
            v.append(vmax*(1-rho[i]/rhomax))
        else:
            v.append(-wf*(1-rhomax/rho[i]))
    return array(v).reshape(20,1)

def get_rho(v):   # get estimate density
    rho=[]
    for i in range(cellnumber):
        #print v[i],vc
        if v[i]>=vc:
            rho.append(rhomax*(1-v[i]/vmax))
        else:
            rho.append(rhomax*(1/(1+v[i]/wf)))
##    print rho
    return array(rho).reshape(20,1)

def calculate(v1,v2):  # calculate the flow-in and flow-out with Daniel Work's function
    if v1>=v2:
        if vc>=v2:
            flow=v2*rhomax*(1/(1+v2/wf))
        else:
            if vc>=v1:
                v_temp=vc
            else:
                v_temp=v1
                flow=v_temp*rhomax*(1-v_temp/vmax)
    else:
        if v1>=vc:
            rho1=rhomax*(1-v1/vmax)
        else:
            rho1=rhomax*(1/(1+v1/wf))
        if v2>=vc:
            rho2=rhomax*(1-v2/vmax)
        else:
            rho2=rhomax*(1/(1+v2/wf))
        flow=min(rho1*v1,rho2*v2)
    return flow
            

def get_flow(v):  # calculate delta flow with two steps of flow-in and flow-out
    v_minus=abs(random.normal(v_ini[0],v_var[0]))
    v_plus=abs(random.normal(v_ini[cellnumber-1],v_var[cellnumber-1]))
    deltaflow=[]
    for i in range(cellnumber):
        if i==cellnumber-1:
            vj=v_plus  #vj to present v[i+1]
        else:
            vj=v[i+1]
        if i==0:
            vk=v_minus #vk to present v[i-1]
        else:
            vk=v[i-1]
        v1=v[i]
        v2=vj
        v3=vk
        flow1=calculate(v1,v2)     #get flow-in
        flow2=calculate(v3,v1)     #get flow-out
        deltaflow.append(flow1-flow2)   
    return array(deltaflow).reshape(20,1)

def get_H():
    h=[]
    file_h=open('H_9sensors.csv','r')
    lines=file_h.readlines()
    for i in range (len(lines)):
        linearray=lines[i].split(',')
        for j in range(cellnumber):
            h.append(float(linearray[j]))
    h=array(h)
    h=h.reshape(9,20)
##    print h.shape
    file_h.close()
    return h

def enkf(v_analysis,y):
    v_forecast=[]
    rho=[] 
    v_forecast=array(v_analysis)
    v_analysis=array(v_analysis)
    for j in range(k):
##        print v_analysis[j]
        rho=get_rho(v_analysis[j])
        deltaflow=get_flow(v_analysis[j])
        n=random.normal(0,Q)
        v_forecast[j]=get_velocity(rho-T/60/0.1*deltaflow)+n
    sumv_f=v_forecast[0]
    for i in range(1,k):
        sumv_f=sumv_f+v_forecast[i]
    v_mean=sumv_f/k
    errorT=matrix(v_forecast[0]-v_mean)
    error=errorT.T
    sumerror=abs(error*errorT)
    for i in range(1,k):
        error=matrix(v_forecast[i]-v_mean) #horinzon
        errorT=error.T #vertical
        sumerror=sumerror+abs(error*errorT)
    P_ens=sumerror/(k-1)       # get the covariance matrix
##    print 'P',P_ens
    H=get_H()
    HT=H.T
    m=matrix(H)*matrix(HT)+Rn
    G_ens=P_ens*HT*(m.I)          # get the kalman gain
##    print 'G',G_ens
    for i in range(k):
        x=random.normal(0,R)
        v_analysis[i]=v_forecast[i]+G_ens*(y-matrix(H)*matrix(v_forecast[i])+x)       # correct the forecast velocity with the forecast and kalman gain
    sumv_a=v_analysis[0]
    for i in range(1,k):
        sumv_a=sumv_a+v_analysis[i]
    v_anamean=sumv_a/k
    v_anamean=v_anamean.reshape(1,20)
    v_mean=sumv_f/k
    result=v_mean.reshape(1,20)
    line1=','.join(str(speed)for speed in v_anamean[0])
    line2=','.join(str(speed)for speed in result[0])
    file_vforecast.write(line2+'\n')
    file_vanalysis.write(line1+'\n')
    return line1

if __name__ == "__main__":    
    global T,vmax,rhomax,rhoc,wf,vc,k,cellnumber,Q,R,Rn,v_ini,v_var,v_estimate
    vmax =100.24606798
    rhomax=184.46672118
    rhoc=40.29179605
    wf=rhoc*vmax/rhomax
    vc=vmax*(1-rhoc/rhomax)
    k=1000
    T=1
    Rn=[]
    ymeasure=[]
    v_ini=[]
    v_var=[]
    v_hat=[]
    v_estimate=[]
    v_analysis=[]
    cellnumber=20
##    R=[12.8,12.8,12.8,12.8,12.8,12.8,12.8,12.8,12.8]
##    Q=[6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4]
    R=[6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4,6.4]
    Q=[3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2]
    Q=array(Q).reshape(20,1)
    R=array(R).reshape(9,1)
    file_vforecast=open('velocity_9sensors_forecast_1test_opt.csv','w')
    file_vanalysis=open('velocity_9sensors_analysis_1test_opt.csv','w')
##    file_ysave=open('y20041103_9.30_10.00','w')
    for i in range(81):
        Rn.append(0)
    Rn=array(Rn).reshape(9,9)
    for i in range(9):
        for j in range(9):
            if i==j:
                Rn[i][j]=6.4*6.4
    print Rn.shape
    v_ini,v_var=initial()
    for i in range(k):
        p=abs(random.normal(v_ini,sqrt(v_var)))
        if p.any>=0:
            v_analysis.append(p)
    for i in range(120/T):
        ymeasure=get_measurement(i)
        v_hat.append(enkf(v_analysis,ymeasure))
##        print v_hat
    print 'over'
##    file_ysave.close()
    file_vforecast.close
    file_vanalysis.close
        
        
##    print v_hat
        
