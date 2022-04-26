from datetime import datetime
import numpy as np
import pandas as pd
import datetime
la1 = pd.read_csv("LA_data1.csv")
la2 = pd.read_csv("LA_data2.csv")
la3 = pd.read_csv("LA_data3.csv")
la4 = pd.read_csv("LA_data4.csv")
def whichday(day,monthi):
    monthlengths = [31,28,31,30,31,30,31,31,30,31,30,31]
    if day < monthlengths[monthi]:
        return day,monthi
    else:
        return whichday(day-monthlengths[monthi],monthi+1)
theday = -1
total = []
month = 0
day = 0
stupid11flag = False
howmanyhere = 24
for i,startpage in enumerate([la1,la2,la3,la4]):
    laarray = startpage.values
    for j in range(laarray.shape[0]):
        if "M" == laarray[j,1][0]:
            
            firstflag = True
            if howmanyhere != 24:
                smallday, smallmonth = whichday(theday,0)
                print(smallmonth + 1, smallday + 1)
            theday += 1

            day,month = whichday(theday,0)
            month = month + 1
            day = day + 1
            
            howmanyhere = 0
            if int(laarray[j+1,1][:2]) == 11:
                stupid11flag = True
        elif (int(laarray[j,1].split(":")[1][:2]) == 53):
            howmanyhere += 1
            if firstflag:
                hour = 0
                firstflag = False
            
            else:
                houradjust = 12 if ((laarray[j,1][-2:] == 'PM') and (int(laarray[j,1].split(":")[0]) != 12)) else 0
                hour = int(laarray[j,1].split(":")[0]) + houradjust
            if stupid11flag:
                hour = 23
                
                newday,newmonth = whichday(theday-1,0)
                newmonth = newmonth + 1
                newday = newday + 1
                date = datetime.datetime(2018,newmonth,newday,hour,int(laarray[j,1].split(":")[1][:2]))
                laarray[j,1] = date
                total.append(laarray[j,1:])
                stupid11flag = False
            else:

                date = datetime.datetime(2018,month,day,hour,int(laarray[j,1].split(":")[1][:2]))
                laarray[j,1] = date
                total.append(laarray[j,1:])

total = np.array(total)
total = pd.DataFrame(total)
print(total.head())
total.columns = ["Time", "Temp", "Dew Point", "Humidity", "Wind", "Wind Speed", "Wind Gust", "Pressure", "Precip", "Condition"]
total.to_csv("LA_data.csv")
