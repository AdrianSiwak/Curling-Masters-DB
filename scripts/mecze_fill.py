from multiprocessing import connection
import mysql.connector
import numpy as np
from datetime import date

mydb = mysql.connector.connect(
  host="giniewicz.it",
  user="team5",
  password="te@mSP@ss",
  database="team5"
)

def create_match_stats():
    us = np.random.randint(0,12)
    them = np.random.randint(0,12)

    result = ""

    if us < them: 
        result = "przegrana"
    elif us > them:
        result = "wygrana"
    else: 
        result = "remis"

    return result, us, them


def create_matches():
    today = date.today()

    mycursor = mydb.cursor()

    mycursor.execute("""SELECT id FROM Terminarz WHERE data < %s""", (today,))

    myresult = mycursor.fetchall()

    for match_id in myresult:
        stats = create_match_stats()
        mycursor.execute("""INSERT INTO Mecze (id, rezultat, Wynik_naszej_druzyny, Wynik_druzyny_przeciwnej) 
                        VALUES (%s, %s, %s, %s)""", match_id + stats)
    mydb.commit()
    mycursor.close()
       
    
create_matches()