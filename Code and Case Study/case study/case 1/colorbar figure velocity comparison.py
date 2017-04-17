def func(sss):
    from matplotlib import pylab
    from numpy import *
    from matplotlib.colors import LinearSegmentedColormap

    cdict = {'red':  ((0.0, 0.0, 0.0),
                       (0.25,0.0, 0.0),
                       (0.5, 0.8, 1.0),
                       (0.75,1.0, 1.0),
                       (1.0, 0.4, 1.0)),

              'green': ((0.0, 0.0, 0.0),
                        (0.25,0.0, 0.0),
                        (0.5, 0.9, 0.9),
                        (0.75,0.0, 0.0),
                        (1.0, 0.0, 0.0)),

              'blue':  ((0.0, 0.0, 0.4),
                        (0.25,1.0, 1.0),
                        (0.5, 1.0, 0.8),
                        (0.75,0.0, 0.0),
                        (1.0, 0.0, 0.0))
        }
    blue_red = LinearSegmentedColormap('BlueRed', cdict)
    pylab.register_cmap(cmap=blue_red)

    pylab.rcParams['image.cmap'] = 'BlueRed'

    with open('velocity_9sensors_analysis_1.csv','r') as file1:
        lines=file1.readlines()
        z1=[]
        m1=[]
        norm=[]
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
    with open('velocity_'+sss+'sensors_analysis_1.csv','r') as file2:
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
        fig=pylab.figure()
        ax=fig.add_subplot(111)
        ax.set_ylabel('Cell Number')
        ax.set_xlabel('Time')
    ##    pylab.xmajorLocator=fig.MultipleLocator(10)
    ##    pylab.ylim(0,100)
        ax.set_title('2004.Nov.3(Wed.), 8:30-10:30')
        diff=(m2-m1)
        max=diff.max()
        min=diff.min()
        for i in diff:
            for j in i:
                if (j>0):
                    print j
                    j=j/max
                    print j
                else:
                    j=-j/min
                norm.append(j)
        norm=array(norm).reshape(100,120)
        imag=pylab.imshow(norm)
        cb=pylab.colorbar(imag,shrink=0.87,ticks=[-3,-2,-1,0,1,2,3,4])
        cb.set_ticklabels([str(round(min,2)),'0',str(round(max,2))],update_ticks=True)
        #pylab.show()
        pylab.savefig('9-'+sss+'.png',dpi=150)
        print 'over'
if __name__=='__main__':
    print 's'
    func('7')
    func('72')
    func('73')
    func('5')
