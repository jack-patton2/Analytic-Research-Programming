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

def seats_left_(seats_avai):
    """number of seats left in each row""" 
    seats_left = np.zeros(nrows).astype(int)
    for i in range(len(seats_avai)):       
        for j in range(nrows):
            if seats_avai[i][0] == j+1:
                seats_left[j] += 1
    seats_left = convert_list(list(enumerate(seats_left,start=1)))
    return seats_left

seats_left = seats_left_(seats_avai)


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
                while j[0] == row:
                    k = j[1]
                    if are_together(num[i],row,k):
                        for x in range(num[i]):
                            assign=[row,k+x]
                            update_booking(name[i],assign)
                        return True

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
            seats_left = seats_left_(seats_avai)  
        # there are more than 1 passengers and it's possible to be together
        elif num[i] <= len(seats[0]) and num[i] <= max(seats_left, key = lambda f:f[1])[1]:
            if booking_multi(i):
                seats_left = seats_left_(seats_avai)
            # seats can't be assigned together
            else: 
                assign = sorted(seats_avai,key=lambda x: x[0])[0:num[i]]
                passengers_separated = passengers_separated + num[i]
                for j in assign:
                    update_booking(name[i],j)
                    seats_left = seats_left_(seats_avai)
                    c.execute("""UPDATE metrics SET passengers_separated=? """, (passengers_separated,)) 
                print('split ',i)       
        # passengers have to be split
        else:
            assign = sorted(seats_avai,key=lambda x: x[0])[0:num[i]]
            passengers_separated = passengers_separated + num[i]
            for j in assign:                
                update_booking(name[i],j)
                seats_left = seats_left_(seats_avai)
                c.execute("""UPDATE metrics SET passengers_separated=? """, (passengers_separated,))  
            

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()

