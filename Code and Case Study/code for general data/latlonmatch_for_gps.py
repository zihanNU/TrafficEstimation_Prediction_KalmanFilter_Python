#datapath = r'\\fukuda_lab_nhd\BackUP\Tonny\Research\EvaluationbyTaxiProbeData\DATA\03ProbeMaster\DRM1800'
datapath = r'C:\Users\Zihan\Documents\STUDY\GPSdata'


def calcu_meas():
    import os
    dirs=os.listdir(datapath)
    curdir=0
    count=0
    num=0
    for diri in dirs:
        num=num+1
        record=open(str(num),'w')
        print("Current dir:",dir)
        curdir=curdir+1
        print count
        print("Processed dirs: %d/%d"%(curdir,len(dirs)))
        csvs=os.listdir(datapath+'\\'+diri)
        length=len(csvs)
        print length
        for csv in csvs:
            print ("csv",csv)
            GPSdata=open(datapath+'\\'+diri+'\\'+csv,'r')
            lines=GPSdata.readlines()
            countline=0
            for line in lines:
                if countline ==0:
                    countline=countline+1
                    continue
                linearray=line.split(',')
                carnum=linearray[1]
        	speed=linearray[27]
       		lat=float(linearray[6])
       		lon=float(linearray[7])
        	data=linearray[3]
        	time=linearray[4]
        	cellnumber=-1
                # provide the longitude and latitude range for each cell
                if lon>=139.7418 and lon<=139.76320 and lat>=35.6495 and lat<=35.6525:
                    if lon >=139.7418 and lon<=139.7431 and lat<=35.6524 and lat>=35.6521:
                        cellnumber=1
                    if lon >=139.743 and lon<=139.744 and lat<=35.6522 and lat>=35.6520:
                        cellnumber=2
                    if lon >=139.744 and lon<=139.745 and lat<=35.652 and lat>=35.6517:
                        cellnumber=3
                    if lon >=139.745 and lon<=139.747 and lat<=35.6517 and lat>=35.6516:
                        cellnumber=4
                    if lon >=139.747 and lon<=139.748 and lat<=35.6516 and lat>=35.6515:
                        cellnumber=5
                    if lon >=139.748 and lon<=139.749 and lat<=35.6515 and lat>=35.6513:
                        cellnumber=6
                    if lon >=139.749 and lon<=139.751 and lat<=35.6507 and lat>=35.6502:
                        cellnumber=7
                    if lon >=139.750 and lon<=139.751 and lat<=35.6502 and lat>=35.6499:
                        cellnumber=8
                    if lon >=139.751 and lon<=139.753 and lat<=35.6499 and lat>=35.6498:
                        cellnumber=9
                    if lon >=139.753 and lon<=139.754 and lat<=35.6501 and lat>=35.6498:
                        cellnumber=10
                    if lon >=139.754 and lon<=139.755 and lat<=35.6503 and lat>=35.6501:
                        cellnumber=11    
                    if lon >=139.755 and lon<=139.756 and lat<=35.6503 and lat>=35.6501:
                        cellnumber=12
                    if lon >=139.756 and lon<=139.757 and lat<=35.6501 and lat>=35.6499:
                        cellnumber=13
                    if lon >=139.757 and lon<=139.758 and lat<=35.6499 and lat>=35.6498:
                        cellnumber=14
                    if lon >=139.758 and lon<=139.759 and lat<=35.6498 and lat>=35.6497:
                        cellnumber=15
                    if lon >=139.759 and lon<=139.760 and lat<=35.6497 and lat>=35.6496:
                        cellnumber=16
                    if lon >=139.760 and lon<=139.761 and lat<=35.64972 and lat>=35.64958:
                        cellnumber=17
                    if lon >=139.761 and lon<=139.762 and lat<=35.64972 and lat>=35.64958:
                        cellnumber=18
                    if lon >=139.762 and lon<=139.763 and lat<=35.6503 and lat>=35.6496:
                        cellnumber=19  
                    record.write(carnum+','+data+','+time+','+str(lat)+','+str(lon)+','+str(cellnumber)+','+speed+'\n')    

            count=count+1
            GPSdata.close
        record.close
    return count

if __name__=='__main__':
    logfile=open('log.txt','w')
    logfile.close()
    
    count=calcu_meas()
    logfile.close()
    record.close()
