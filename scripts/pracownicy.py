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

fake = Faker()

def next_worker(worker):
    join_date=None
    leave_date=None
    
    if (datetime.datetime.now() - relativedelta(months=1)).date() < worker[4]:
        join_date = worker[4]
        leave_date = None
    else:
        join_date = worker[4]
        leave_date = fake.date_between(join_date, datetime.datetime.now())
        
    pay = np.random.randint(20,40)

    return fake.first_name(), fake.last_name(), worker[2], join_date, leave_date, pay
        

def create_workers(posting):
    join_date = datetime.datetime(1980,8,20)
    leave_date = fake.date_between(join_date, datetime.datetime.now())
    pay = np.random.randint(20,40)
    worker = (fake.first_name(), fake.last_name(), posting, join_date, leave_date, pay)
    
    mycursor.execute(
                     """INSERT INTO Pracownicy (imie, nazwisko, stanowisko, data_zatrudnienia, data_odejscia, pensja) 
                    VALUES (%s, %s, %s, %s, %s, %s)""", worker)
    
    while (worker[4] != None):
        worker = next_worker(worker)
        print(worker)
        
        mycursor.execute(
                     """INSERT INTO Pracownicy (imie, nazwisko, stanowisko, data_zatrudnienia, data_odejscia, pensja) 
                    VALUES (%s, %s, %s, %s, %s, %s)""", worker)
    
try:
    create_workers("trener")
    create_workers("fizjoterapeuta")
    create_workers("księgowy")
except BaseException as err:
    print(err)


mydb.commit()
mydb.close()
