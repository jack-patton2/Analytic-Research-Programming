# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:46:47 2017

@author: Ruyue
"""


import sqlite3
import pandas as pd
import numpy as np

#def read_file(f):
df = pd.read_csv('/Users/Ruyue/Documents/Smurfit Bussiness Analytics/Semester2/ARI_Programing2/bookings.csv',sep=',',header = None)
name = df[0]
num = df[1]  
db = '/Users/Ruyue/Documents/Smurfit Bussiness Analytics/Semester2/ARI_Programing2/airline_seating.db' 
conn = sqlite3.connect(db)
c = conn.cursor()
nrows =c.execute("SELECT nrows from rows_cols").fetchone()[0]  #number of rows in the plane
seats = c.execute("SELECT seats from rows_cols").fetchone()    #seats in a row
nseats = nrows*len(seats[0]) #total number of seats
seats_taken = c.execute("SELECT row, seat FROM seating WHERE name != '' ").fetchall() 
passengers_refused = 0
passengers_separated = 0
seats_po = c.execute("SELECT row, seat from seating").fetchall() #get structure of seats


def convert_list(l):
    'convert a list of tuples to a list of lists'
    l = [list(elem) for elem in l]
    return l

seats_po = convert_list(seats_po)
seats_taken = convert_list(seats_taken)

def convert_letter(list1,str2):
    'convert letters in seats to interger'
    for i in range(len(list1)):
        for j in range(len(str2)):
            if list1[i][1] == str2[j]:
                list1[i][1] = j+1
    return list1

seats_po = convert_letter(seats_po,seats[0])
seats_taken = convert_letter(seats_taken,seats[0])

seats_avai=[x for x in seats_po if x not in seats_taken]

def seats(seats_avai):
    """number of seats left in each row""" 
    seats_left = np.zeros(nrows).astype(int)
    for i in range(len(seats_avai)):       
        for j in range(nrows):
            if seats_avai[i][0] == j+1:
                seats_left[j] += 1
    return seats_left

seats_left = seats(seats_avai)
seats_left = list(enumerate(seats_left,start=1))

seats = c.execute("SELECT seats from rows_cols").fetchone() 
def convert_numtoletter(n):
    L = seats[0][n-1] #letter
    return L

def booking_single(i):
    assign = sorted(seats_avai,key=lambda x: x[0])[0]
    update_booking(name[i],assign)

                
def are_together(num,row,k):
    """check if the seats in the available row are together,otherwise, count seats_split """
    for i in range(num):
        if [row,k+i] not in seats_avai:
            return False
    return True


def booking_multi(i):
    for row,n in seats_left:
        if num[i] <= n:
            for j in seats_avai:
                if j[0] == row:
                    k = j[1]           
                    if are_together(num[i],row,k):
                        for x in range(num[i]):
                            assign=[row,k+x]
                            update_booking(name[i],assign)
                            print(k,assign,num[i])
                    return True
    return False


def booking_split(i,passengers_separated): 
    assign = sorted(seats_avai,key=lambda x: x[0])[0:num[i]]
    for j in assign:
        passengers_separated = passengers_separated + num[i]
        c.execute("""UPDATE metrics SET passengers_refused=? """, (passengers_separated,))

                                 

def update_booking(name,seat_assign):
    """if seats have been assigned succefully, update seats_taken, seats_avai and Table seat"""
    seats_taken.append([seat_assign[0],convert_numtoletter(seat_assign[1])])
    seats_avai.remove(seat_assign)
    c.execute("""UPDATE seating SET name =?  WHERE row=? and seat=?""",(name,seat_assign[0],convert_numtoletter(seat_assign[1])))


########### _main_############                    
for i in range(len(num)):        
    # no seats left
    if len(seats_avai) == 0:
        print("all seats are booked")
        passengers_refused = passengers_refused + num[i]
        c.execute("""UPDATE metrics SET passengers_refused=? """, (passengers_refused,))
        
    # the number of seats not enough for this booking
    elif len(seats_avai) < num[i]:
        print('booking exceeds #seats avaliable')
        passengers_refused = passengers_refused + num[i]
        c.execute("""UPDATE metrics SET passengers_refused=? """, (passengers_refused,))
    
    # the seats can be assigned
    else:
        # there is only one passenger in the booking
        if num[i]==1:
            booking_single(i)
                
        # there are more than 1 passengers and it's possible to be together
        elif num[i]<=len(seats[0]) and num[i] <= max(seats_left, key = lambda f:f[1])[1]:
            booking_multi(i)
            # seats can't be assigned together
            if booking_multi(i)==False:
                booking_split(i,passengers_separated)     
                print('split ',i)       
        # passengers have to be split
        else:
            booking_split(i,passengers_separated)
            print('split ',i)  
            

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

conn = sqlite3.connect(db)
c = conn.cursor()
dff= c.execute("SELECT row, seat,name FROM seating ").fetchall() 
dF = pd.DataFrame(dff)
dF2 = dF[2]
df1 = pd.DataFrame({'A': dF2[0:15], 'B': dF2[15:30], 'C': dF2[30:45], 'D': dF2[45:60]},  index=[0,1, 2, 3,4,5,6,7,8,9,10,11,12,13,14])
b = [x for x in dF2[15:30]]
df1['B']=b
c = [x for x in dF2[30:45]]
d = [x for x in dF2[45:60]]
df1['C']=c
df1['D']=d
