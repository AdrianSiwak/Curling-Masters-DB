from multiprocessing import connection
import mysql.connector
from faker import Faker
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

mydb = mysql.connector.connect(
  host="giniewicz.it",
  user="team5",
  password="te@mSP@ss",
  database="team5"
)

mycursor = mydb.cursor()

def create_equipment(eq_type):
    
    mycursor.execute(
                     """INSERT INTO Sprzet (typ_sprzetu, ilosc, ilosc_uszkodzonych_lub_zutylizowanych) 
                    VALUES (%s, %s, %s)""", (eq_type,0, 0))
    
eq_types = ["kamien", "szczotka", "buty"]
try:
    for eq_type in eq_types:
        create_equipment(eq_type)
except BaseException as err:
    print(err)
        
mydb.commit()
mycursor.close()
mydb.close()