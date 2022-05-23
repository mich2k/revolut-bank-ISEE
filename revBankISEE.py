#! /usr/bin/python3
import pprint
import csv
from datetime import date, timedelta, datetime

dic={} 


# filename & year, you can change these 2 vars.

filename='statement.csv'
year=2020       # it will lookup for correct calendar 


# import whole given calendar in the dic


init_date=date(year,1,1)
end_date=date(year,12,31)
curr_date=init_date
while curr_date != end_date:
    dic[str(curr_date)]=[0,0]
    curr_date+= timedelta(days=1)

# import data
#pprint.pprint(dic) 
with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    back_date =''
    curr_date=''
    lc=0



    for row in csv_reader:
        if(lc != 0):
            if(row[12] != ''):
                if(dic.get(row[1].split(' ')[0]) is None):
                    dic[row[1].split(' ')[0]] = [round(float(row[12]),2), 1]
                else:
                    tmp=dic.get(row[1].split(' ')[0])
                    tmp[0] = tmp[0] + float(row[12])
                    tmp[1] = tmp[1] +1
                    dic[row[1].split(' ')[0]]=tmp
        lc+=1
        
# rounds dict to 2 floating digits

# adds data to missing days from calc statement in order to fill missing gaps
i=0
for k,v in dic.items():
    if(i==0):
        i+=1
        continue
    if(v[1] == 0):
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                back_date=str(datetime.fromisoformat(k)-timedelta(days=1)).split(' ')[0]
                if(row[1].split(' ')[0] == back_date and row[12] != '' and dic.get(k)[1]==0):
                    tmp=[float(row[12]),1]
                    dic[k]=tmp
                    continue
            #Missing in csv file, lookup in the dict..
            if(dic.get(k)[1]==0):
                back_date=str(datetime.fromisoformat(k)-timedelta(days=1)).split(' ')[0]
                tmp=dic.get(back_date).copy()   # NOT by reference
                tmp[1]=1
                dic[k]=tmp

# only at this point the dic has full and valid data

#pprint.pprint(dic)  # remove this comment if you want to display the full dictionary, strongly 
                        # suggested to double check with your official statement

# Avg calc phase...

year_sum=0

for k,v in dic.items():
    curr=v[0]/v[1]
    #print(k,curr)      # remove comment if you want to display all day-by-day averages
    year_sum+=curr

if(year%4==0 and year%100!=0 or year%400==0):
    year_days=366
    print(f"L'anno {year} e' bisestile, considero 366 giorni.")
else:
    year_days=365

print(f"La giacenza media e' '{round(year_sum/year_days,2)}'.")
