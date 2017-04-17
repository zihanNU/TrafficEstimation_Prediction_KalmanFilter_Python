import os
from numpy import *
datapath = r'C:\Users\hong\Desktop\master thesis\coding and test for traffic count\yokohane\04-11-03'

def tcdata(manageid,numberid):
    tccsv=os.listdir(datapath)
    dataitem=['','','','','']
    file_redata=open(numberid+'_'+manageid+'.csv','w')
    for csv in tccsv:
        file_data=open(datapath+'\\'+csv,'r')
        lines=file_data.readlines()
        linearray=lines[10].split(',')
        for j in range(1,len(linearray)):
            s=linearray[j].decode('s-jis')
            managementid=s[0:2]+'-'+s[3:5]+'-'+s[6:9]        # format the sensor id and compare with the sensor list
            if managementid==(manageid):
                for k in range(461,643):
                    lineitem=lines[k].split(',')                  
                    dataitem=[lineitem[0],lineitem[j],lineitem[j+2],lineitem[j+4],lineitem[j+6]]
                    datajoin=','.join(item for item in dataitem)
                    file_redata.write(datajoin+'\n')
                file_redata.close()
                return
            else:
                j=j+8
    file_data.close()
    return 

if __name__ == "__main__":
    manageid=[]
    numberid=[]
    file_sensor=open('1.csv','r')
    lines=file_sensor.readlines()
    for i in range (0,len(lines)):
        linearray=lines[i].split(',')
        manageid.append(linearray[1])      # sensor id
        numberid.append(linearray[9])      # cell number
    file_sensor.close()
    for i in range(0,len(lines)):
        tcdata(manageid[i],numberid[i])
    print 'v'
        
