#! /usr/bin/python3
import pprint
import csv
from datetime import date, timedelta, datetime

dic={} 


# filename & year

# whole calendar in the dict (full automatic) !

year=2020

init_date=date(year,1,1)
end_date=date(year,12,31)
curr_date=init_date
while curr_date != end_date:
    dic[str(curr_date)]=[0,0]
    curr_date+= timedelta(days=1)

# import data
#pprint.pprint(dic) 
with open('dest.csv') as csv_file:  # hardcoded filename
    csv_reader = csv.reader(csv_file, delimiter=',')
    back_date =''
    curr_date=''
    lc=0
    inner_splitter=0
    inner_additioner=0.0



    for row in csv_reader:  # begin reading .csv rows
        if(lc != 0):
            if(row[12] != ''):
               # dic[str(row[1])]+=float(row[12])
                if(dic.get(row[1].split(' ')[0]) is None):
                    dic[row[1].split(' ')[0]] = [round(float(row[12]),2), 1]
                else:
                    tmp=dic.get(row[1].split(' ')[0])
                    tmp[0] = tmp[0] + float(row[12])
                    tmp[1] = tmp[1] +1
                    dic[row[1].split(' ')[0]]=tmp
        lc+=1
#pprint.pprint(dic)     
# rounds dict

#dic = {key : [round(dic[key][0], 2), dic[key][1]] for key in dic}   # before time delta

#pprint.pprint(dic) 

# adds data to missing days from calc statement
i=0
for k,v in dic.items():
    if(i==0):
        i+=1
        continue
    if(v[1] == 0):
        with open('dest.csv') as csv_file:  # hardcoded filename
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                back_date=str(datetime.fromisoformat(k)-timedelta(days=1)).split(' ')[0]
                if(row[1].split(' ')[0] == back_date and row[12] != '' and dic.get(k)[1]==0):
                    tmp=[float(row[12]),1]
                    dic[k]=tmp
                    print(f"on {k} i gave {tmp}")
                    continue
            #if i arrive here means there was not the date in the csv file, so i have to lookup in the dict
            if(dic.get(k)[1]==0):
                back_date=str(datetime.fromisoformat(k)-timedelta(days=1)).split(' ')[0]
                tmp=dic.get(back_date).copy()   # NOT by reference
                tmp[1]=1
                dic[k]=tmp

# only at this point the dic has full and valid data

#pprint.pprint(dic)  # remove this comment if you want to display the full dictionary, strongly 
                # suggested to double check with your official statement

# proceeding with avg calc..

year_sum=0
pprint.pprint(dic)

for k,v in dic.items():
    curr=v[0]/v[1]
    #print(k,curr)      # remove comment if you want to display all day-by-day averages
    year_sum+=curr

if(year%4==0 and year%100!=0 or year%400==0):
    year_days=366
    print(f"L'anno {year} e' bisestile, considero 366 giorni.")
else:
    year_days=365

print(f"L'isee e' '{round(year_sum/year_days,2)}'.")
