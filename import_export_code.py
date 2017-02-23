import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('/Users/jackpatton/Documents/School/bookings.csv',sep=',',header = None)
name = df[0]
num = df[1]  
db = '/Users/jackpatton/Documents/School/airline_seating.db' 
conn = sqlite3.connect(db)
c = conn.cursor()
nrows =c.execute("SELECT nrows from rows_cols").fetchone()[0]  
seats = c.execute("SELECT seats from rows_cols").fetchone()    
nseats = nrows*len(seats[0])
seats_taken = c.execute("SELECT row, seat FROM seating WHERE name != '' ").fetchall() 
nseats_left = nseats - len(seats_taken)
passengers_refused = 0
passengers_separated = 0
seats_po = c.execute("SELECT row, seat from seating").fetchall() 
seats_left = np.zeros(nrows).astype(int)


def booking_split(i): 
    assign = sorted(seats_avai,key=lambda x: x[0])[0:num[i]]
    for j in assign:
        passengers_separated = passengers_separated + num[i]
        c.execute("""UPDATE metrics SET passengers_refused=? """, (passengers_separated,))

                                 

def update_booking(name,seat_assign):
    """if seats have been assigned succefully, update seats_taken, seats_avai and Table seat"""
    seats_taken.append([seat_assign[0],convert_numtoletter(seat_assign[1])])
    seats_avai.remove(seat_assign)
    c.execute("""UPDATE seating SET name =?  WHERE row=? and seat=?""",(name,seat_assign[0],convert_numtoletter(seat_assign[1])        


conn.commit()
conn.close()
