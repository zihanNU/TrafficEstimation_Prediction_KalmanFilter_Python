from matplotlib import pylab
from matplotlib.backends.backend_pdf import PdfPages
import os
import numpy as np

file1=open('ttotal.csv','r')
t1=[]
t2=[]
t3=[]
t4=[]
t5=[]
t6=[]
lines=file1.readlines()
for i in range(1,181):
    linearray1=lines[0].split(',')
    linearray2=lines[1].split(',')
    linearray3=lines[2].split(',')
    linearray4=lines[3].split(',')
    linearray5=lines[4].split(',')
    linearray6=lines[5].split(',')
    t1.append(linearray1[i])
    t2.append(linearray2[i])
    t3.append(linearray3[i])
    t4.append(linearray4[i])
    t5.append(linearray5[i])
    t6.append(linearray6[i])
fig=pylab.figure(figsize=(16,9))
ax1=fig.add_subplot(131)
l1=ax1.plot(t1,'b-',markersize=30)
l4=ax1.plot(t4,'k.-',markersize=5)
ax2=fig.add_subplot(132)
l2=ax2.plot(t2,'r-',markersize=30)
l5=ax2.plot(t5,'k.-',markersize=5)
ax3=fig.add_subplot(133)
l3=ax3.plot(t3,'g-',markersize=30)
l6=ax3.plot(t6,'k.-',markersize=5)
text=['7:30','7:50','8:10','8:30','8:50','9:10','9:30','9:50','10:10','10:30']
fig.legend((l4,l5,l6),('Wangan Nov.01','Wangan Nov.02','Wangan Nov.03'),loc='lower right')
ax1.set_title('Travel Time, Nov 01',fontsize=15)
ax1.set_xlabel('Departure Time',fontsize=15)
ax1.set_ylabel('Travel Time1 (minute)',fontsize=15)
ax1.set_ylim([20,60])
ax2.set_title('Travel Time Difference, Nov 02',fontsize=15)
ax2.set_xlabel('Departure Time',fontsize=15)
ax2.set_ylabel('Travel Time (minute)',fontsize=15)
ax2.set_ylim([20,60])
ax1.set_xticks([0,60,120,180])
ax1.set_xticklabels(['7:30','8:30','9:30','10:30'])
ax2.set_xticks([0,60,120,180])
ax2.set_xticklabels(['7:30','8:30','9:30','10:30'])
ax3.set_xticks([0,60,120,180])
ax3.set_xticklabels(['7:30','8:30','9:30','10:30'])
ax3.set_title('Travel Time Difference, Nov 03',fontsize=15)
ax3.set_xlabel('Departure Time',fontsize=15)
ax3.set_ylabel('Travel Time (minute)',fontsize=15)
ax3.set_ylim([20,60])
pylab.xticks([0,60,120,180],['7:30','8:30','9:30','10:30'])
##fig.legend((l1,l2,l3),('More minute on Yokohane Line, Nov.01','More minute on Yokohane Line, Nov.02','More minute on Yokohane Line, Nov.03'),loc='lower center')
##pylab.show()
##ax3.set_xticks(np.arange(180),text)
##fig.legend((l1,l2,l3,l4,l5,l6),('Yokohane Nov.01','Yokohane Nov.02','Yokohane Nov.03','Wangan Nov.01','Wangan Nov.02','Wangan Nov.03'),loc='upper leftpylab.xticks([0,60,120,180],['7:30','8:30','9:30','10:30'])
##pylab.show()
pylab.savefig('t22.png',dpi=150)
file1.close()
print 'over'
