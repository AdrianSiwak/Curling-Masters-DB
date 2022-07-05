from multiprocessing import connection
import mysql.connector
import numpy as np
from datetime import date, timedelta
from random import choices

#Nazwy drużyn wymyślone z głowy
Przeciwnicy = ['Equipe de curling de Paris','El equipo de curling de Bogota','Bialostocka druzyna curlingowa','Bydgoska druzyna curlingowa', 'Gdanska druzyna curlingowa', 'Katowicka druzyna curlingowa', 'Kielecka druzyna curlingowa', 'Krakowska druzyna curlingowa', 'Lublelska druzyna curlingowa', 'lodzka druzyna curlingowa', 'Olsztynska druzyna curlingowa','Opolska druzyna curlingowa', 'Poznanska druzyna curlingowa', 'Rzeszowska druzyna curlingowa', 'Szczecinska druzyna curlingowa', 'Warszawska druzyna curlingowa', 'Zielono Gorska druzyna curlingowa','Lwowska druzyna curlingowa','Berliner Curling-Team','Prazsky curlingovy tym']

def daty(data_początkowa,data_koncowa,liczba_meczy):
    """Wybiera tyle dat ile ma podanych meczy do rozegrania w okresie między dwoma podanymi datami"""
    daty = [data_początkowa]
    while data_początkowa != data_koncowa:
        data_początkowa += timedelta(days=1)
        daty.append(data_początkowa)
    data = choices(daty, k=liczba_meczy)
    return data

#łączy z bazą
mydb = mysql.connector.connect(
    host="giniewicz.it",
    user="team5",
    password="te@mSP@ss",
    database="team5"
)

mycursor = mydb.cursor()

#Rok rozpoczęcia generowania danych
year = 1980

place = ['wyjazdowy', 'domowy']

#Rok zakończenia
while year<2027:
    liczba_gier = (year - 1960)//2 + np.random.randint(-5,5) # Wymyślona funkcja na ilość meczy
    lista_dat = daty(date(year, 10, 1),date(year+1, 5, 30),liczba_meczy=liczba_gier) #Lista dat na mecze w podanym okresie (nie grają w wakacje)
    lista_przeciwnicy = [] # Tu będą losowani przeciwnicy
    for i in range(liczba_gier):
        val = (str(lista_dat[i]),str(np.random.choice(Przeciwnicy)),np.random.choice(place)) #zamieniam na stringi by pasowało do Query
        sql = """INSERT INTO Terminarz (data,przeciwnik,Miejsce_rozegrania_meczu) 
        VALUES (%s, %s,%s);"""
        mycursor.execute(sql, val)

        mydb.commit()
    year += 1
