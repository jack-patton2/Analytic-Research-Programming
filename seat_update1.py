# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:46:47 2017

@author: Ruyue
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
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
nseats_left = nseats - len(seats_taken)
passengers_refused = 0
passengers_separated = 0
seats_po = c.execute("SELECT row, seat from seating").fetchall() #get structure of seats
seats_left = np.zeros(nrows).astype(int)
def seats(seats_avai):
    """number of seats left in each row""" 
    for i in range(len(seats_avai)):    
        for j in range(nrows):
            if seats_avai[i][0] == j+1:
                seats_left[j] += 1
    return seats_left
seats_left = list(enumerate(seats_left,start=1))

def convert_list(l):
    'convert a list of tuples to a list of lists'
    l = [list(elem) for elem in l]
    return l
seats_po = convert_list(seats_po)
seats_taken = convert_list(seats_taken)
seats_left = convert_list(seats_left)

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
def convert_numtoletter(n):
    L = seats[0][n-1]#letter
    return L
convert_numtoletter(3)       

def booking_single(i):
    assign = sorted(seats_avai,key=lambda x: x[0])[0]
    update_booking(name[i],assign)
    #plot_seats(seats_po,seats_taken)
                
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
                        for l in range(num[i]):
                            assign=[row,k+l]
                            update_booking(name[i],assign)
                            #plot_seats(seats_po,seats_taken)
                            return True
    return False


def booking_split(i): 
    assign = sorted(seats_avai,key=lambda x: x[0])[0:num[i]]
    for j in assign:
        passengers_separated = passengers_separated + num[i]
        c.execute("""UPDATE metrics SET passengers_refused=? """, (passengers_separated,))

                                 

def update_booking(name,seat_assign):
    """if seats have been assigned succefully, update seats_taken, seats_avai and Table seat"""
    seats_taken.append([seat_assign[0],convert_numtoletter(seat_assign[1])])
    seats_avai.remove(seat_assign)
    c.execute("""UPDATE seating SET name =?  WHERE row=? and seat=?""",(name,seat_assign[0],convert_numtoletter(seat_assign[1])))

def plot_seats(seats_po,seats_taken):
# plot seats
# get x-axis lables
# function(update everytime): if a seat is booked, then it turns red
    labels = []
    for i in range(len(seats[0])):
        labels.append(seats[0][i]) 
    x = []
    y = []
    x_taken = []
    y_taken = []
    for i in range(len(seats_po)):
        x.append(seats_po[i][1])
        y.append(seats_po[i][0])
    for i in range(len(seats_taken)):
        x_taken.append(seats_taken[i][1])
        y_taken.append(seats_taken[i][0])
    plt.plot(x, y, 'go')
    plt.plot(x_taken,y_taken,'ro')
    plt.xticks(x, labels)
    plt.axis([0,len(seats[0])+1, 0, nrows+1])
    plt.grid()
    plt.show()
plot_seats(seats_po,seats_taken)
                          
for i in range(len(num)):        
    # no seats left
    if nseats_left == 0:
        print("all seats are booked")
        passengers_refused = passengers_refused + num[i]
        c.execute("""UPDATE metrics SET passengers_refused=? """, (passengers_refused,))
        
    # the number of seats not enough for this booking
    elif nseats_left < num[i]:
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
            booking_split(i)     
                    
        # passengers have to be split
        else:
            booking_split(i)
               
                        

        

#


# Committing changes and closing the connection to the database file
conn.commit()
conn.close()


