
from multiprocessing import connection
import mysql.connector
from faker import Faker
import datetime
from dateutil.relativedelta import relativedelta
import numpy as np

base_stones = 8
base_brooms = 2
incom_delta = 2000

monthly_sum = 0
finances = 0

first_month = True

start_date = datetime.datetime(1980,9,10)

mydb = mysql.connector.connect(
  host="giniewicz.it",
  user="team5",
  password="te@mSP@ss",
  database="team5"
)

fake = Faker()

mycursor = mydb.cursor()

equipment = None
workers = None
matches = None

def fill_finances():
    fetch_data()
    
    date = start_date
    while (date + relativedelta(months=1)) < datetime.datetime.now():
        fill_month(date)
        date = date + relativedelta(months=1)

def fill_month(date):

    global monthly_sum 
    monthly_sum=0
    
    end_date = date + relativedelta(months=1)
    
    global first_month
    if first_month:
        first_month = False
        buy_base_equipment()
    else:
        buy_equipment(date, end_date)
        
    pay_for_month(date)
    create_travel_cost(date, end_date)
    
    create_incom(date, monthly_sum - finances)
    
    monthly_sum = 0

def fetch_data():
    global equipment
    mycursor.execute("SELECT id, typ_sprzetu FROM Sprzet")
    equipment = mycursor.fetchall()
    
    global workers
    mycursor.execute("SELECT id, pensja, data_zatrudnienia, data_odejscia FROM Pracownicy")
    workers = mycursor.fetchall()
    
    global matches
    mycursor.execute("SELECT id, data FROM Terminarz WHERE Miejsce_rozegrania_meczu = 'wyjazdowy'")
    matches = mycursor.fetchall()

def insert_equipment(data, kwota, typ_podmiotu, ID_podmiotu, uwagi, ilosc):
    global monthly_sum
    broken = np.random.uniform(0,1)
    monthly_sum = monthly_sum + kwota * ilosc
    mycursor.execute(
                     """INSERT INTO Finanse (data, kwota, typ_podmiotu, ID_podmiotu, uwagi, ilosc) 
                    VALUES (%s, %s, %s, %s, %s, %s)""",(data, kwota, typ_podmiotu, ID_podmiotu, uwagi,ilosc))

    mycursor.execute(
        """UPDATE Sprzet set ilosc =ilosc + %s WHERE id = %s """,(ilosc, ID_podmiotu)
    )
    
    if broken>0.7:
        mycursor.execute(
            """UPDATE Sprzet set ilosc_uszkodzonych_lub_zutylizowanych =ilosc_uszkodzonych_lub_zutylizowanych + %s WHERE id = %s """
            ,(ilosc, ID_podmiotu)
        )

def create_incom(date, min_incom):
    global finances
    incom = np.random.randint(min_incom, min_incom+incom_delta)
    finances = incom - min_incom
    mycursor.execute(
                     """INSERT INTO Finanse (data, kwota, typ_podmiotu, ID_podmiotu, uwagi, ilosc) 
                    VALUES (%s, %s, %s, %s, %s, %s)""",(date, incom, "sponsorzy", -1, "wsparcie od sponsorów", 1))    
        
def pay_for_month(date):
    global monthly_sum

    for worker in workers:
        if worker[2] < date.date() < worker[3]:
            hours = np.random.randint(16, 46)
            kwota = worker[1] * hours
            monthly_sum = monthly_sum + kwota
            mycursor.execute(
                         """INSERT INTO Finanse (data, kwota, typ_podmiotu, ID_podmiotu, uwagi, ilosc) 
                        VALUES (%s, %s, %s, %s, %s, %s)""",(date, kwota, "wypłata", worker[0], "wyplata", 1))
    
def create_travel_cost(date, end_date):
    global monthly_sum

    for match in matches:
        if date.date() < match[1] < end_date.date():
            kwota = np.random.randint(1000, 3000) #Koszt wyjazdu można pozmieniać
            monthly_sum = monthly_sum + kwota
            mycursor.execute(
                         """INSERT INTO Finanse (data, kwota, typ_podmiotu, ID_podmiotu, uwagi, ilosc) 
                        VALUES (%s, %s, %s, %s, %s, %s)""",(match[1], kwota, "wyjazd", match[0], "wyjazd", 1))
    
def buy_equipment(start_date, end_date):
    for eq in equipment:
        date = fake.date_between(start_date, end_date)
        count = np.random.randint(0,2)
        propability = np.random.uniform(0,1)
        if propability<0.9:
            continue

        elif eq[1] == "kamien":
            buy_stone(count, date, eq[0]) 
        elif eq[1] == "szczotka":
            buy_broom(count, date, eq[0])
        elif eq[1] == "buty":
            buy_shoes(count, date, eq[0])          
    
def buy_base_equipment():
    for eq in equipment:
        if eq[1] == "kamien":
            buy_stone(base_stones, start_date, eq[0]) 
        elif eq[1] == "szczotka":
            buy_broom(base_brooms, start_date, eq[0])
            
    
def buy_stone(count, date, s_id):
    price = np.random.randint(1000,5000)
    insert_equipment(date, price, "sprzet", s_id, "brak" ,count)

def buy_broom(count, date, s_id):
    price = np.random.randint(200,600)
    insert_equipment(date, price, "sprzet", s_id, "brak" ,count)
        
def buy_shoes(count, date, s_id):
    price = np.random.randint(300,1000)
    insert_equipment(date, price, "sprzet", s_id, "brak" , count)
          
try:
    fill_finances()
except BaseException as err:
    print(err)    
    
mydb.commit()
mycursor.close()
mydb.close()







