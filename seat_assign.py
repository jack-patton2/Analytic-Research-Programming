# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 13:46:47 2017

@author: Ruyue
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
#def read_file(f):
df = pd.read_csv('/Users/Ruyue/Documents/Smurfit Bussiness Analytics/Semester2/ARI/Programing2/bookings.csv',sep=',',header = None)
name = df[0]
num = df[1]
    #return name,num

#def booking(name,num):    
db = '/Users/Ruyue/Documents/Smurfit Bussiness Analytics/Semester2/ARI/Programing2/airline_seating.db' 
conn = sqlite3.connect(db)
c = conn.cursor()
nrows =c.execute("SELECT nrows from rows_cols").fetchone()[0]  #number of rows in the plane
seats = c.execute("SELECT seats from rows_cols").fetchone()    #seats in a row
nseats = nrows*len(seats[0]) #total number of seats
seats_taken = c.execute("SELECT row, seat FROM seating WHERE name != '' ").fetchall() 
nseats_left = nseats - len(seats_taken)
passengers_refused = 0
passengers_separated = 0
# plot real-time seats booking status
seats_po = c.execute("SELECT row, seat from seating").fetchall() #get structure of seats

# function(update everytime): if a seat is booked, then it turns red


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
def convert_numtoletter(n):
    L = seats[0][n-1]#letter
    return L
        

def plot_seats(seats_po,seats_taken):
# plot seats
# get x-axis lables
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
    if nseats_left == 0 or nseats_left < num[i]:
        s = 'no booking is avaliable'
        passengers_refused = passengers_refused + num
        c.execute("""UPDATE metrics SET passengers_refused=? """, (passengers_refused,))
        print(s)
        i += 1
    else:
        if num[i]==1:
            for row,n in seats_avai:
                if row == seats_sor[0][0]:
                    seats_taken.append([row,n])
                    seats_avai.remove([row,n])
                    update_seats_sor(seats_avai)
                    c.execute("UPDATE seating SET name =?  WHERE row=? and seat=?",(name[i],row,convert_numtoletter(n)))
                    break           
            plot_seats(seats_po,seats_taken)
            break

        if num[i]<=len(seats[0]):
            row1 = []
            start = []
            for row,n in seats_sor:
                if num[i] <= n:
                    row1.append(row)
            for [j,k] in seats_avai:
                if j in row1 and k <=len(seats[0])-num[i]+1:
                    start.append(seats_avai[j,k])
            for j,k in start:
                if are_together(num,j,k):
                    for l in range(num):
                        seats_taken.append(seats_avai[j,k+l])
                        seats_avai.remove([j,k+l])
                        update_seats_sor(seats_avai)
                        c.execute("UPDATE seating SET name =?  WHERE row=? and seat=?",(name[i],j,convert_numtoletter(k+l)))
                    break
                else:
                    for range(num-1,1)#no #num of seats together,split 
                       
        else: 
            rows_need = math.ceil(num[i]/len(seats[0]))
            rows2 = [] #seats more than booking number
            for row,n in seats_sor:
                if n == len(seats[0]):
                    rows1.append(row) 
        plot_seats(seats_po,seats_taken)
            
       
        
def find_seats_together(num):
    for i in range(1,nrows+1):
        if num < max(seats_left):

#number of seats left in each row
seats_left = np.zeros(nrows).astype(int)
def update_seats_sor(seats_avai):
    for i in range(len(seats_avai)):    
        for j in range(nrows):
            if seats_avai[i][0] == j+1:
                seats_left[j] += 1 
    seats_left = list(enumerate(seats_left,start=1))
    seats_sor = sorted(seats_left,key=lambda x: x[1])# sorted left seats
    delete_zeros(seats_sor)
    
def delete_zeros(seats_sor):
    """delete unavailable rows"""
    for i in seats_sor:
        if seats_sor[0][1]==0:
            seats_sor = seats_sor.remove(seats_sor[0][1] )
                 
#function used to chech if seats together 
def are_together(num,j,k):
    """check if the seats in the available row together,otherwise, count seats_split """
    for i in range(num):
        if [j,k+i] not in seats_avai:
            return False
    return True
        

    

    


















# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
def find_rows(num,seats_left):
    """ find available rows"""
    rows1 =[] #seats equivalent to the booking number      
    rows2 = [] #seats more than booking number
    for row,n in seats_left:
        if n == num:
            rows1.append(row) 
        if n > num:
            rows2.append(row)
    return rows1,rows2   