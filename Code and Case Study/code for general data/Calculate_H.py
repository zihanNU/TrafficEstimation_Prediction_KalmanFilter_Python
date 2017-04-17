import os
from numpy import *
datapath = r'C:\Users\hong\Desktop\master thesis\coding and test for traffic count\yokohane\04-11-03'

def tcdata(manageid,numberid):
# read the overall original data
    tccsv=os.listdir(datapath)
    dataitem=['','','','','']
    file_redata=open(numberid+'_'+manageid+'.csv','w')
    for csv in tccsv:
        file_data=open(datapath+'\\'+csv,'r')
        lines=file_data.readlines()
        linearray=lines[10].split(',')
        for j in range(1,len(linearray)):
            s=linearray[j].decode('s-jis')
            managementid=s[0:2]+'-'+s[3:5]+'-'+s[6:9] # to format the sensor id
            if managementid==(manageid):
                for k in range(462,642):
                    lineitem=lines[k].split(',')                  
                    dataitem=[lineitem[0],lineitem[j],lineitem[j+2],lineitem[j+4],lineitem[j+6]] # to select time, traffic volume, large vehicle volume, speed and occupancy
                    datajoin=','.join(item for item in dataitem)
                    file_redata.write(datajoin+'\n')
                file_redata.close()
                return
            else:
                j=j+8 # for next sensor data
    file_data.close()
    file_redata.close()
    return 

if __name__ == "__main__":
    manageid=[]
    numberid=[]
    H=[]
    for i in range(108*145):  # sensor number and cell number, all together for a H matrix
        H.append(0)
    H=array(H).reshape(108,145)
    file_H=open('H3.csv','w')
    file_sensor=open('1.csv','r')
    lines=file_sensor.readlines()
    for i in range (0,len(lines)):
        linearray=lines[i].split(',')
        print int(linearray[9]),i
        H[i][int(linearray[9])-1]=1 # when a cell has a sensor, the related H matrix item should be changed into 1 otherwise remain 0
    for i in range(108):
        for j in range(144):
            file_H.write(str(H[i][j])+',')
        file_H.write(str(H[i][144])+'\n')
        manageid.append(linearray[1])  # sensor id
        numberid.append(linearray[10])  # cellnumber
    file_sensor.close()
    file_H.close()
##    for i in range(0,len(manageid)):
##        print manageid[i],numberid[i]
##        tcdata(manageid[i],numberid[i])
    print 'over'
        
