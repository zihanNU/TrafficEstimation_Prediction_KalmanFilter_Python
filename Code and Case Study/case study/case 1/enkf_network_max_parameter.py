import os
from scipy.optimize import minimize
from scipy.linalg  import det
from numpy import *
#datapath = r'C:\Users\hong\Desktop\master thesis\200411'
datapath = r'C:\Users\hong\Desktop\para_opti\200411'

def get_measurement(count):
    csv9=['0411_27.csv', '0411_28.csv','0411_29.csv', '0411_30.csv', '0411_31.csv',  '0411_33.csv','0411_34.csv', '0411_35.csv', '0411_37.csv']
    csv7=['0411_27.csv', '0411_29.csv', '0411_30.csv', '0411_31.csv',  '0411_34.csv', '0411_35.csv', '0411_37.csv']
    csv5=['0411_27.csv', '0411_29.csv', '0411_31.csv', '0411_34.csv', '0411_37.csv']
    y=[]
    for csv in csv7:
        # reverse
        file_y=open(datapath+'/'+csv,'r')
        lines=file_y.readlines()
        for i in range ((count-1)*T+3392,count*T+3392):
            linearray=lines[i].split(',')
            y.append(float(linearray[5]))
    file_y.close()
##    x=[]
##    for i in range(20):
##        x.append(0)
##    x[1]=y[8]
##    x[3]=y[7]
##    x[5]=y[6]
##    x[7]=y[5]
##    x[10]=y[4]
##    x[12]=y[3]
##    x[15]=y[2]
##    x[18]=y[1]
##    x[19]=y[0]
##    line=','.join(str(speed)for speed in x)
##    file_ysave.write(line+'\n')           ## to record all measurement in one 
    ramp=[]
    csvramp=['0411_32.csv','0411_33.csv', '0411_36.csv']
    for csv in csvramp:
        # reverse
        file_r=open(datapath+'/'+csv,'r')
        lines=file_r.readlines()
        for i in range ((count-1)*T+3392,count*T+3392):
            linearray=lines[i].split(',')
            ramp.append(float(linearray[4]))
    ramp=array(ramp).reshape(3,1)
    file_r.close()
    rampin=ramp[2]
    belta=ramp[0]/ramp[1]    
    return array(y).reshape(7,1)
    

def initial():
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

def get_velocity(rho,para):
    vmax =para[0]
    rhomax=para[1]
    rhoc=para[2]
    wf=rhoc*vmax/rhomax
    vc = vmax*(1-rhoc/rhomax)
    QM= vc*rhoc
    v=[]
    for i in range(cellnumber):
        rhoi=rho[i][0]
#        print rhoi,rhomax
        if rhoi<=rhoc:
            v.append(vmax*(1-rhoi/rhomax))
        else:
            v.append(-wf*(1-rhomax/rhoi))
    return array(v).reshape(20,1)

def get_rho(v,para):
    vmax =para[0]
    rhomax=para[1]
    rhoc=para[2]
    wf=rhoc*vmax/rhomax
    vc = vmax*(1-rhoc/rhomax)
    QM= vc*rhoc
    rho=[]
    for i in range(cellnumber):
        vi=v[i][0]
        #print v[i],vc
        if vi>=vc:
            rho.append(rhomax*(1-vi/vmax))
        else:
            rho.append(rhomax*(1/(1+vi/wf)))
##    print rho
    return array(rho).reshape(20,1)

def calculate(rho1,rho2,rho3,nettype,para):
    vmax =para[0]
    rhomax=para[1]
    rhoc=para[2]
    wf=rhoc*vmax/rhomax
    vc = vmax*(1-rhoc/rhomax)
    QM= vc*rhoc
    Si_minus=min(vmax*rho1,QM)
    Ri=min(QM,wf*(rhomax-rho2))
    Si=min(vmax*rho2,QM)
    Ri_plus=min(QM,wf*(rhomax-rho3))
    if nettype==0:
        flowin=min(Si_minus,Ri)
        flowout=min(Si,Ri_plus)
    if nettype==1:
        if Si_minus+rampin<=Ri:
            flowin=Si_minus+rampin
        else:
            flowin=Ri
        flowout=min(Si,Ri_plus)
    if nettype==2:
        flowin=min(Si_minus,Ri)
        flouout=min(Si,Ri_plus/(1-belta))
    return flowin-flowout
            
def get_flow(v,rho,para):
    vmax =para[0]
    rhomax=para[1]
    rhoc=para[2]
    wf=rhoc*vmax/rhomax
    vc = vmax*(1-rhoc/rhomax)
    QM= vc*rhoc
    v_minus=abs(random.normal(v_ini[0],v_var[0]))
    v_plus=abs(random.normal(v_ini[cellnumber-1],v_var[cellnumber-1]))
    if v_minus>=vc:
        rhoi_minus=rhomax*(1-v_minus/vmax)
    else:
        rhoi_minus=rhomax*(1/(1+v_minus/wf))
    if v_plus>=vc:
        rhoi_plus=rhomax*(1-v_plus/vmax)
    else:
        rhoi_plus=rhomax*(1/(1+v_plus/wf))
    nettype=0
    deltaflow=[]
    for i in range(cellnumber):
        if cellnumber==9:
            nettype=2  #offramp
        if cellnumber==13:
            nettype=1  #onramp
        if i!=cellnumber-1:
            rhoi_plus=rho[i+1]
        if i!=0:
            rhoi_minus=rho[i-1]
        rhoi=rho[i]
        dflow=calculate(rhoi_minus,rhoi,rhoi_plus,nettype,para)
        deltaflow.append(dflow)
    return array(deltaflow).reshape(20,1)

def get_H():
    h=[]
    file_h=open('H_7sensors.csv','r')
    lines=file_h.readlines()
    for i in range (len(lines)):
        linearray=lines[i].split(',')
        for j in range(cellnumber):
            h.append(float(linearray[j]))
    h=array(h)
    h=h.reshape(7,20)
##    print h.shape
    file_h.close()
    return h

def enkf(v_analysis,y,para0):
    para=para0.reshape(3,1)
    vmax =para[0]
    rhomax=para[1]
    rhoc=para[2]
    wf=rhoc*vmax/rhomax
    vc = vmax*(1-rhoc/rhomax)
    QM= vc*rhoc
    v_forecast=[]
    rho=[] # cellnumber
    v_forecast=array(v_analysis)
    v_analysis=array(v_analysis)
    for j in range(k):
##        print v_analysis[j]
        rho=get_rho(v_analysis[j],para)
        deltaflow=get_flow(v_analysis[j],rho,para)
        n=random.normal(0,Q)
        v_forecast[j]=get_velocity(rho-T/60/0.1*deltaflow,para)+n
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
    P_ens=sumerror/(k-1)
##    print 'P',P_ens
    H=get_H()
    HT=H.T
    m=matrix(H)*matrix(HT)+Rn
    G_ens=P_ens*HT*(m.I)
##    print 'G',G_ens
    likeli_ens=0
    for i in range(k):
        x=random.normal(0,R)
        v_analysis[i]=v_forecast[i]+G_ens*(y-matrix(H)*matrix(v_forecast[i])+x)
        delta=y-matrix(H)*matrix(v_forecast[i])
        Rm=matrix(Rn)
        likeli_ens=exp(-0.5*delta.T*Rm.I*delta)+likeli_ens
    sumv_a=v_analysis[0]
    for i in range(1,k):
        sumv_a=sumv_a+v_analysis[i]
    v_anamean=sumv_a/k
    v_anamean=v_anamean.reshape(1,20)
    v_mean=sumv_f/k
    result=v_mean.reshape(1,20)
    line1=','.join(str(speed)for speed in v_anamean[0])
##    line2=','.join(str(speed)for speed in result[0])
##    file_vforecast.write(line2+'\n')
##    file_vanalysis.write(line1+'\n')
    return -log(likeli_ens)

def get_likelihood(para):
    hood=0
    print para
    for i in range(120/T):
        ymeasure=get_measurement(i)
        hood=enkf(v_analysis,ymeasure,para)+hood
    print "hood=:",hood
    return hood

if __name__ == "__main__":    
    global T,rampin,rampout,belta,k,cellnumber,Q,R,Rn,v_ini,v_var
    likelihood=[]
    T=1
    rampin=0.0
    belta=0.0
    k=100
    Rn=[]
    ymeasure=[]
    v_ini=[]
    v_var=[]
##    v_estimate=[]
    v_analysis=[]
    cellnumber=20
    R=[6.4,6.4,6.4,6.4,6.4,6.4,6.4]
    Q=[3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2,3.2]
##    R=[4,4,4,4,4]
##    Q=[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    Q=array(Q).reshape(20,1)
    R=array(R).reshape(7,1)
##    file_vforecast=open('velocity_72sensors_forecast_1.csv','w')
##    file_vanalysis=open('velocity_7sensors_analysis_1.csv','w')
##    file_ysave=open('y20041103_9.30_10.00','w')
    for i in range(49):
        Rn.append(0)
    Rn=array(Rn).reshape(7,7)
    for i in range(7):
        for j in range(7):
            if i==j:
                Rn[i][j]=6.4*6.4
    print Rn.shape
    v_ini,v_var=initial()
    for i in range(k):
        p=abs(random.normal(v_ini,sqrt(v_var)))
        if p.any>=0:
            v_analysis.append(p)
    file_hood=open('hood','w')       
##    for vm in range(80,120):
##        for rhom in range(160,200):
##            for rhoc in range(30,50):
##                para=[vm,rhom,rhoc]
##                hood=get_likelihood(para)[0][0]
##                likelihood.append(likelihood)
##                file_hood.write(str(likelihood)+'\n')
    para0=[[98],[180],[40]]
    bnd=((80,120),(160,200),(35,45))
    print para0
    para_o=minimize(get_likelihood,para0,method='Powell')
##    print 'Estimater parameters: ', paraopti
##    print 'real parameters:',para
    a=array(likelihood)
    print min(a)
    print a.index(min(a))
    print 'over'
    file_hood.close()
##    file_vforecast.close
##    file_vanalysis.close
        
        
##    print v_hat
        
