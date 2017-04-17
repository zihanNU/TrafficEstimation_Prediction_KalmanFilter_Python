import os
from numpy import *
datapath = r'C:\Users\hong\Desktop\master thesis\coding and test for traffic count\yokohane\20041102_yokohane'

def get_measurement(count):
    tccsv=os.listdir(datapath)
    y=[]
    for i in range (127):
        y.append(0.0)
    for i in range(0,len(tccsv)):
        # reverse
        file_y=open(datapath+'\\'+tccsv[i],'r')
        lines=file_y.readlines()
        linearray=lines[count].split(',')
        if len(linearray)>3 and linearray[3]!='':
            y[int(tccsv[i][0:3])-1] = float(linearray[3])
        else:
            y[int(tccsv[i][0:3])-1]= 0
    file_y.close()
    line=','.join(str(speed)for speed in y)
    file_ysave.write(line+'\n')           ## to record all measurement in one

if __name__ == "__main__":
    file_ysave=open('y_measure_1102.csv','w')
    for i in range(1,180+1):
        print i
        ymeasure=get_measurement(i)
    file_ysave.close()
