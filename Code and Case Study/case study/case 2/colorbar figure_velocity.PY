from matplotlib import pylab
from numpy import *

with open('velocity_a_test32.csv','r') as file1:
    lines=file1.readlines()
    z=[]
    m=[]
    for i in range(0,180):
        linearray=lines[i].split(',')
        for j in range(126):
            for k in range(1):
                p=float(linearray[j])
                z.append(p)
        for k in range(1):
                p=float(linearray[126][1:7].rstrip('\n'))
                z.append(p)
    z=array(z).reshape(180,127)
    m=z.T
    print z.shape
##    print z
##    pylab.xticks(arange(20),'0','5','10','15','20')
##    pylab.xticks(arange(180),'7.30','8.00','8.30','9.00','9.30','10.00','11.30')
    pylab.subplot(111)
    pylab.ylabel('Cell Number')
    pylab.xlabel('Time')
##    pylab.xmajorLocator=fig.MultipleLocator(10)
##    pylab.ylim(0,100)
    pylab.title('2004.Nov.3(Wen.), 7:30-10:30')
    pylab.pcolor(m,vmin= 10,vmax= 110)
    b=pylab.colorbar(shrink=0.76)
    pylab.imshow(pylab.clip(m,10,110))
##    b.shrink(0.8)
    pylab.savefig('yokohane_a_11032t.png',dpi=150)
    print 'over'
