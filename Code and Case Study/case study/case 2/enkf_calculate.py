import os
from numpy import *
import math
datapath1 = r'C:\Users\hong\Desktop\master thesis\coding and test for traffic count\yokohane\20041101_wangan'
datapath2 = r'C:\Users\hong\Desktop\master thesis\coding and test for traffic count\yokohane\wangan_rampin1101'
datapath3 = r'C:\Users\hong\Desktop\master thesis\coding and test for traffic count\yokohane\wangan_rampout1101'
datapath4 = r'C:\Users\hong\Desktop\master thesis\coding and test for traffic count\yokohane\wangan_base1101'

def get_measurement(count):  # get measurement according to time step, measurement at the main road, and ramps
    tccsv=os.listdir(datapath1)
    y=[]
    for i in range(108):
        y.append(-1.0)   # if no measurement, tag -1.0; no measurement will make no correction
    for i in range(0,len(tccsv)):
        # reverse
        file_y=open(datapath1+'\\'+tccsv[i],'r')
        lines=file_y.readlines()
        linearray=lines[count].split(',')
        if linearray[3]!='' and float(linearray[3])!=0.0:
            y[i]=float(linearray[3])
    file_y.close()
    rampincsv=os.listdir(datapath2)
    ramp_in=[]
    ramp_out=[]
    base=[]
    lenrmpin=len(rampincsv)
    for csv in rampincsv:
        # reverse
        file_r=open(datapath2+'\\'+csv,'r')
        lines=file_r.readlines()

        linearray=lines[count].split(',')
        if linearray[1]!='':
            ramp_in.append(float(linearray[1]))
        else:
            ramp_in.append(0.0)
        ramp_in.append(int(csv[0:3])-1)
    rampin=array(ramp_in).reshape(lenrmpin,2).T
    file_r.close()
    rampoutcsv=os.listdir(datapath3)
    lenrmpout=len(rampoutcsv)
    for csv in rampoutcsv:
        file_r=open(datapath3+'\\'+csv,'r')
        lines=file_r.readlines()
##        print '2',csv
##        print lines[180],i,'rampout'
        linearray=lines[count].split(',')
        if linearray[1]!='':
            ramp_out.append(float(linearray[1]))
        else:
            ramp_out.append(-1.0)
        ramp_out.append(int(csv[0:3])-1)
    file_r.close
    rampout=array(ramp_out).reshape(lenrmpout,2).T
##    os.system('pause')
    baseadd=os.listdir(datapath4)
    for i in range(lenrmpout):
        file_r=open(datapath4+'\\'+baseadd[i],'r')
        lines=file_r.readlines()
##        print '3',baseadd[i]
##        print lines[180],i,'base'
        linearray=lines[count].split(',')
        if linearray[1]!='':
            base.append(float(linearray[1]))
        else:
            base.append(-1.0)
    file_r.close
    basearray=array(base).reshape(1,lenrmpout)
    belta=[rampout[0]/basearray[0],rampout[1]]
    beta=array(belta).reshape(2,lenrmpout)
    for j in range(lenrmpout):
        if beta[0][j]>=1:
            beta[0][j]=0.99
        if basearray[0][j]==-1.0:
            beta[0][j]=-1.0
        if rampout[0][j]==-1.0:
            beta[0][j]=-1.0
##    print 'beta', beta
    return array(y).reshape(108,1),rampin,beta
    

def initial(): # initial with the velocity_mean and velocity_variance
    v_mean=[]
    v_variance=[]
    file_ini=open('meanvariance.csv','r')
    lines=file_ini.readlines()
    for i in range(len(lines)):
        linearray=lines[i].split(',')
        v_mean.append(float(linearray[0]))
        v_variance.append(float(linearray[1]))
    file_ini.close()
    return array(v_mean).reshape(145,1),array(v_variance).reshape(145,1)

def get_velocity(rho): # calculate the estimated velocity according to the estimated density
    v=[]
    for i in range(cellnumber):
        v1=vmax*(1-rho[i][0]/rhomax)
        v2=-wf*(1-rhomax/rho[i][0])
        if rho[i][0]<=rhoc:
            v.append(v1)
        if rho[i][0]>rhoc:
            v.append(v2)
    v=array(v).reshape(145,1)
    for i in range(cellnumber):
        if v[i][0]<0 or v[i][0]>vmax:
##            print 'v',v[i][0],rho[i][0],rho[i-1][0],rho[i+1][0]
            if v[i][0]<0:
                v[i][0]=0.0
            else:
                v[i][0]=vmax
##            os.system('pause')
##        print rho[i][0],i
    return v

def get_rho(v):  # calculate the estimated density
    rho=[]
    for i in range(cellnumber):
        rho1=rhomax*(1-v[i][0]/vmax)
        rho2=rhomax*(1/(1+v[i][0]/wf))
        if v[i][0]>=vc:
            m=rho1
        else:
            if v[i][0]<vc:
                m=rho2
        rho.append(m)
    rho=array(rho).reshape(145,1)
    for i in range(cellnumber):
        if rho[i][0]<0 or rho[i][0]>rhomax:
##            print 'rho',rho[i][0],v[i][0],t,i
            if rho[i][0]<0:
                rho[i][0]=1
            else:
                rho[i][0]=rhomax
##            os.system('pause')
##            else:
##                print 'mis',v[i][0],t,i
##                os.system('pause')

    return rho

def calculate(rho1,rho2,rho3,nettype,cell_no,rampin,beta):  # calculate the delta flow for each cell
    rampin=array(rampin).reshape(2,9)
    beta=array(beta).reshape(2,9)
    Si_minus=min(vmax*rho1,QM)
    Ri=min(QM,wf*(rhomax-rho2))
    Si=min(vmax*rho2,QM)
    Ri_plus=min(QM,wf*(rhomax-rho3))
##    if Si_minus<0 or Si<0 or Ri<0 or Ri_plus<0:
##        print 'flow ability',Si_minus, Si, Ri, Ri_plus
    beta_cell=-2.0
    rampin_cell=-2.0
    if nettype==0:
        flowin=min(Si_minus,Ri)
        flowout=min(Si,Ri_plus)
    if nettype==1:
        for i in range (9):
            if rampin[1][i]==cell_no:
                rampin_cell=rampin[0][i]
        if Si_minus+rampin_cell<=Ri:
            flowin=Si_minus+rampin_cell
        else:
            flowin=Ri
        flowout=min(Si,Ri_plus)
    if nettype==2:
        for i in range (9):
            betacount=0
            if beta[0][i]==-1.0:  # change beta where no sensor data for beta
                betacount=betacount+1
        for i in range (9):
            if beta[0][i]==-1.0:
                beta[0][i]=(sum(beta[0])+betacount)/(9-betacount)
            if beta[1][i]==cell_no:
                beta_cell=beta[0][i]
        flowin=min(Si_minus,Ri)
        flowout=min(Si,Ri_plus/(1-beta_cell))
    deltaflow=flowin-flowout
##    if abs(deltaflow)>1000:
##        print 'd',deltaflow,nettype,flowin, flowout,cell_no
##        print Si_minus, Si, Ri, Ri_plus
##        os.system('pause')
    return deltaflow


def get_flow(v,rho,rampin,beta): # calculate cell type, original, ramp_in or ramp_out and then calculate the deltaflow with 'calculate'
    v_minus=(random.normal(v_ini[0][0],Q))
    v_plus=(random.normal(v_ini[cellnumber-1][0],Q))
    deltaflow=[]
    for i in range(cellnumber):
        nettype=0
        outno=[2,3,48,66,78,85,107,124,142]
        inno=[7,58,69,89,104,111,117,130,143]
        if v_minus>=vc:
            rhoi_minus=rhomax*(1-v_minus/vmax)
        else:
            rhoi_minus=rhomax*(1/(1+v_minus/wf))
        if v_plus>=vc:
            rhoi_plus=rhomax*(1-v_plus/vmax)
        else:
            rhoi_plus=rhomax*(1/(1+v_plus/wf))
        if i+1 in outno:
            nettype=2  #offramp
        if i+1 in inno:
            nettype=1  #onramp
        if i!=cellnumber-1:
            rhoi_plus=rho[i+1][0]
        if i!=0:
            rhoi_minus=rho[i-1][0]
        rhoi=rho[i][0]
        dflow=calculate(rhoi_minus,rhoi,rhoi_plus,nettype,i,rampin,beta)
        deltaflow.append(dflow)
    return array(deltaflow).reshape(145,1)

def get_H(): # get the H matrix
    h=[]
    file_h=open('H3.csv','r')
    lines=file_h.readlines()
    for i in range (len(lines)):
        linearray=lines[i].split(',')
        for j in range(cellnumber):
            h.append(float(linearray[j]))
    h=array(h)
    h=h.reshape(108,145)
    file_h.close()
    return h

def enkf(v_ana,y,rampin,beta):
    v_forecast=[]
    v_analysis=[]
    y_revise=y.reshape(108,1)
    rho=[] # cellnumberv
    v_forecast=array(v_ana).reshape(k,cellnumber,1)
    v_analysis=array(v_ana).reshape(k,cellnumber,1)
    for j in range(k):   # calculate the estimated density for next time step according to the current density and delta flow
        rho=get_rho(v_analysis[j])
        deltaflow=get_flow(v_analysis[j],rho,rampin,beta)
        n=random.normal(0,Q)      
        deltarho=T/60.0/0.25*deltaflow
        newrho= rho+T/60.0/0.25*deltaflow
        for n in range(cellnumber-1):
            if newrho[n][0]<0 or newrho[n][0]>rhomax:
                newrho[n][0]=(newrho[n+1][0]+newrho[n-1][0])*0.5
        if newrho[cellnumber-1][0]<0 or newrho[cellnumber-1][0]>rhomax:
            newrho[cellnumber-1][0]=newrho[n-1][0]+random.normal(0,2)
        v_forecast[j]=get_velocity(newrho)
    sumv_f=v_forecast[0]
    for i in range(1,k):
        sumv_f=sumv_f+v_forecast[i]
    v_mean=sumv_f/k
    error=matrix(v_forecast[0]-v_mean)
    errorT=error.T
    sumerror=(error*errorT)
    for i in range(1,k):
        error=matrix(v_forecast[i]-v_mean) #horinzon]
        errorT=error.T #vertical
        sumerror=sumerror+(error*errorT)
    P_ens=sumerror/(k-1)
##    print 'P',P_ens
    H=get_H()
    HT=H.T
    m=matrix(H)*P_ens*matrix(HT)+Rn
    G_ens=(P_ens*HT*(m.I)).reshape(145,108)
    for i in range(k):
        x=random.normal(0,R)
##        print 'x',x
        HX=(matrix(H)*matrix(v_forecast[i])).reshape(108,1)
        for j in range(108):
            y_revise[j][0]=y[j][0]
            if y[j][0]==-1:
                y_revise[j][0]=HX[j][0]
            if y[j][0]>vmax:
                y_revise[j][0]=vmax
                print 'no y',y_revise[j][0],j
##                os.system('pause')
        v_analysis[i]=v_forecast[i]+G_ens*(y_revise-HX+random.normal(0,R))           # correct the estimation with the forecast and the kalman gain  
        for n in range(cellnumber):
                if n ==cellnumber-1:
                    v_analysis[i][n][0]=v_analysis[i][n-1][0]*0.5
                else:
                    v_analysis[i][n][0]=v_analysis[i][n-1][0]*0.5+v_analysis[i][n+1][0]*0.5
    sumv_a=v_analysis[0]
    for i in range(1,k):
        sumv_a=sumv_a+v_analysis[i]
    v_anamean=sumv_a/k
    result1=v_anamean.reshape(1,145)
    result2=v_mean.reshape(1,145)
    line1=','.join(str(speed)for speed in result1[0])
    line2=','.join(str(speed)for speed in result2[0])
    file_vforecast.write(line2+'\n')
    file_vanalysis.write(line1+'\n')
    print 'v shape', v_analysis.shape
    return 1

if __name__ == "__main__":    
    global t,T,vmax,rhomax,rhoc,wf,vc,QM,rampin,beta,k,cellnumber,Q,R,Rn,v_ini,v_a
    rampin=[]
    beta=[]
    vmax =140.0
    rhomax=190.0
    rhoc=40.0
    wf=rhoc*vmax/rhomax
    vc = vmax*(1-rhoc/rhomax)
    QM= vc*rhoc
    T=1
    k=1000
    Rn=[]
    ymeasure=[]
    v_ini=[]
    a=[]
    cellnumber=145
    Q=2
    R=4
    file_vforecast=open('velocity_f_w.csv','w')
    file_vanalysis=open('velocity_a_w1101t.csv','w')
    for i in range(108*108):
        Rn.append(0)
    Rn=array(Rn).reshape(108,108)
    for i in range(108):
        for j in range(108):
            if i==j:
                Rn[i][j]=R*R
    Rn=matrix(Rn)
    ymeasure,rampin,beta=get_measurement(0)
    H=get_H()
    for t in range(0,180/T):
        v_a=[]
        print t
        ymeasure,rampin,beta=get_measurement(t)
        for yi in range(108-5):
            if ymeasure[yi]<0:
                ymeasure[yi]=ymeasure[yi-4]/2.0+ymeasure[yi+4]/2.0
        v_ini=array((matrix(H)).I*ymeasure).reshape(cellnumber,1)  # y is start from before estimation and to make the initial velocity
        for i in range(0,cellnumber-1):
            if v_ini[i][0]==0.0 or v_ini[i][0]<0: # no sensor, make the average
                v_ini[i][0]=(v_ini[i-1][0]/2.0+v_ini[i+1][0]/2.0)
        if v_ini[cellnumber-1][0]<0:
                v_ini[cellnumber-1][0]=v_ini[cellnumber-1-1][0]
        for j in range(0,k):
            p=(random.normal(v_ini,Q))
            v_a.append(p)
        v_a=array(v_a).reshape(k,cellnumber,1)
        ymeasure,rampin,beta=get_measurement(t+1)
        a=enkf(v_a,ymeasure,rampin,beta)
       
##    file_ysave.close()
    file_vforecast.close
    file_vanalysis.close
    print 'over'
        
##    print v_hat
        
