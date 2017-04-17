from matplotlib import pylab
from numpy import *

with open('velocity_9sensors_analysis_1.csv','r') as file1:
    lines=file1.readlines()
    z1=[]
    m1=[]
    for i in range(0,120):
        linearray=lines[i].split(',')
        for j in range(19):
            for k in range(5):
                p=float(linearray[j])
                z1.append(p)
        for k in range(5):
                p=float(linearray[19].rstrip('\n'))
                z1.append(p)
    z1=array(z1).reshape(120,100)
    m1=z1.T
with open('velocity_73sensors_analysis_1.csv','r') as file2:
    lines=file2.readlines()
    z2=[]
    m2=[]
    for i in range(0,120):
        linearray=lines[i].split(',')
        for j in range(19):
            for k in range(5):
                p=float(linearray[j])
                z2.append(p)
        for k in range(5):
                p=float(linearray[19].rstrip('\n'))
                z2.append(p)
    z2=array(z2).reshape(120,100)
    m2=z2.T
##    print z
##    pylab.xticks(arange(20),'0','5','10','15','20')
##    pylab.yticks(arange(120),'8.30','9.00','9.30','10.00','10.00')
    pylab.ylabel('Cell Number')
    pylab.xlabel('Time')
##    pylab.xmajorLocator=fig.MultipleLocator(10)
##    pylab.ylim(0,100)
    pylab.title('2004.Nov.3(Wen.), 8:30-10:30')
    pylab.imshow(m1-m2)
    pylab.colorbar()
    pylab.savefig('9-73.png',dpi=150)
    print 'over'
