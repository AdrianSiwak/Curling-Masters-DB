from multiprocessing import connection
import mysql.connector
import numpy as np
from datetime import date, timedelta
from random import choices
#Lista najpopularniejszych polskich imion i nazwisk
imiona_listaM = ['Adam', 'Andrzej', 'Arkadiusz', 'Artur', 'Bartosz', 'Grzegorz', 'Jan', 'Jozef', 'Krzysztof', 'Maciej', 'Marcin', 'Marek', 'Patryk', 'Pawel', 'Piotr', 'Stanislaw', 'Tomasz','Michal', 'Wieslaw', 'Zbigniew', 'lukasz']
imiona_listaK = ['Agata', 'Agnieszka', 'Anna', 'Barbara', 'Ewa', 'Joanna', 'Justyna', 'Katarzyna', 'Krystyna', 'Maja', 'Maria', 'Martyna', 'Malgorzata', 'Monika', 'Paulina', 'Roza', 'Sylwia', 'Zofia']
nazwiska_listaM = ['Ambrzykowski','Augustyniak','Bartodziej', 'Bereszynski', 'Borowik', 'Boruc', 'Brodacki', 'Blaszczykowski', 'Cienciala', 'Czarniecki', 'Dzik', 'Dabek', 'Glik', 'Gortat', 'Janusz', 'Koc', 'Kowalczyk', 'Kowalski', 'Lewandowski', 'Marczak', 'Mosiadz', 'Mysior', 'Nowak', 'Polak', 'Rybus', 'Salomon', 'Siwak', 'Sobolewski', 'Sokol', 'Tralka', 'Urbanowicz', 'Wolski', 'Zalewski', 'los','Ksiazka', 'Golabek']
nazwiska_listaK = ['Ambrzykowska','Augustyniak','Bartodziej', 'Bereszynska', 'Borowik', 'Boruc', 'Brodacka', 'Blaszczykowska', 'Cienciala', 'Czarniecka', 'Dzik', 'Glik', 'Gortat', 'Janusz', 'Koc', 'Kowalczyk', 'Kowalska', 'Lewandowska', 'Marczak', 'Mosiadz', 'Mysior', 'Nowak', 'Polak', 'Rybus', 'Salomon', 'Siwak', 'Sobolewska', 'Sokol', 'Tralka', 'Urbanowicz', 'Wolska', 'Zalewska', 'Dabek', 'loś','Ksiazka', 'Golabek']

#Tworze listę numerów dla kobiet i mężczyzn i ją wypełniam
wolne_numeryM = []
wolne_numeryK = []
for i in range(0,100):
    wolne_numeryM.append(i)
    wolne_numeryK.append(i)

#Tworzę listę na zajęte numery
numery_zajeteM = []
numery_zajeteK = []

#Funkcja dodaje numery nowych zawodników do zajętych i usuwa z wolnych, oraz zabiera najstarszy numer po, z zajętych i wstawia do wolnych
def numery(listaWN,listaZN,osoba):
    """Funkcja dodaje numery nowych zawodników do zajętych i usuwa z wolnych,
     oraz zabiera najstarszy numer po, z zajętych i wstawia do wolnych"""
    nr = osoba[2]
    listaZN.append(nr)
    listaWN.remove(nr)
    if len(listaZN) > 8:
        stary_nr = listaZN[0]
        listaWN.append(stary_nr)
        listaZN.remove(stary_nr)
        return listaWN,listaZN
    else:
        return listaWN,listaZN


def daty(data_początkowa,data_koncowa):
    """Wybiera datę w okresie między dwoma podanymi datami"""
    daty = [data_początkowa]
    while data_początkowa != data_koncowa: #Iteruje po wszystkich dniach w tym okresie i dodaje do listy
        data_początkowa += timedelta(days=1)
        daty.append(data_początkowa)
    data = choices(daty, k=1) #Wybieram z tej listy k=1 dat.
    return str(data[0])

def nowy_mezczyzna(year):
    """Tworzy krotkę, która zawiera informacje o płci, numerze koszulki, imieniu i nawisku oraz dacie dołączenia i odejścia z klubu, nowego mężczyzny"""
    plec = 2 #płeć to Enum w bazie danych
    numer_koszulki = int(np.random.choice(wolne_numeryM)) #wybiera z wolnych numerów
    imie = np.random.choice(imiona_listaM)
    nazwisko = np.random.choice(nazwiska_listaM) #wybiera losowy element z listy
    prawd = np.random.uniform() #wybiera losowy numer z przedziału (0,1)
    if prawd>0.7: #30 procent że ktoś nie spędzi pełnych 4 lat w klubie
        if year < 2018:
            data_dolaczenia = daty(date(year, 7, 1),date(year, 9, 30))
            data_odejscia = daty(date(year, 10, 1),date(year+4, 6, 30))
        else:
            data_dolaczenia = daty(date(year, 7, 1),date(year, 9, 30))
            data_odejscia = date(9999,12,30) #Dalej jest w klubie
    else:
        if year < 2018:
            data_dolaczenia = daty(date(year, 7, 1),date(year, 9, 30))
            data_odejscia = daty(date(year+4, 6, 1),date(year+4, 6, 30))
        else:
            data_dolaczenia = daty(date(year, 7, 1),date(year, 9, 30))
            data_odejscia = date(9999,12,30) #Dalej jest w klubie
    return str(imie), str(nazwisko), numer_koszulki, data_dolaczenia, data_odejscia, plec

def nowa_kobieta(year):
    """Tworzy krotkę, która zawiera informacje o płci, numerze koszulki, imieniu i nawisku oraz dacie dołączenia i odejścia z klubu, nowej kobiety w klubie"""
    plec = 1 #Płeć to Enum w bazie danych
    numer_koszulki = int(np.random.choice(wolne_numeryK))
    imie = np.random.choice(imiona_listaK)
    nazwisko = np.random.choice(nazwiska_listaK)
    prawd = np.random.uniform()
    if prawd>0.8:
        if year < 2018:
            data_dolaczenia = daty(date(year, 7, 1),date(year, 9, 30))
            data_odejscia = daty(date(year, 10, 1),date(year+4, 6, 30))
        else:
            data_dolaczenia = daty(date(year, 7, 1),date(year, 9, 30))
            data_odejscia = date(9999,12,30)
    else:
        if year < 2018:
            data_dolaczenia = daty(date(year, 7, 1),date(year, 9, 30))
            data_odejscia = daty(date(year+4, 6, 1),date(year+4, 6, 30))
        else:
            data_dolaczenia = daty(date(year, 7, 1),date(year, 9, 30))
            data_odejscia = date(9999,12,30) #Dalej jest w klubie
    return str(imie), str(nazwisko), numer_koszulki, data_dolaczenia, data_odejscia, plec

#łączę się z serwerem
mydb = mysql.connector.connect(
  host="giniewicz.it",
  user="team5",
  password="te@mSP@ss",
  database="team5"
)

mycursor = mydb.cursor()
# Próbny jeden zawodnik, czy zadziała
# sql = """INSERT INTO Zawodnicy (imie, nazwisko, numer_na_koszulce, data_dolaczenia, data_odejscia, plec) 
# VALUES (%s, %s, %s, %s, %s, %s);"""
# val = nowa_kobieta(year)
# wolne_numeryM,numery_zajeteM = numery(wolne_numeryM,numery_zajeteM,val)
# mycursor.execute(sql,val)

# mydb.commit()

#Definiuje rok, od którego mierzymy poczynania naszej drużyny
year = 1980

#Do tego roku
while year<2022:
    sql = """INSERT INTO Zawodnicy (imie, nazwisko, numer_na_koszulce, data_dolaczenia, data_odejscia, plec) 
    VALUES (%s, %s, %s, %s, %s, %s);""" #Query sqlowe, dodaje do kolumn o nazwach powyżej dane po funkcji VALUES
    val = nowy_mezczyzna(year) #nowy mężczyzna lub kobieta zwraca krotkę, rozdział na mężczyznę i kobietę był potrzebny przy podstawowych założeniach, jednak, zmieniliśmy je w póżniejszym czasie tworzenia projektu
    wolne_numeryM,numery_zajeteM = numery(wolne_numeryM,numery_zajeteM,val)
    mycursor.execute(sql, val) #biorę kod SQLowy ze zmiennej sql oraz zmienne z krotki val

    mydb.commit()

    sql = """INSERT INTO Zawodnicy (imie, nazwisko, numer_na_koszulce, data_dolaczenia, data_odejscia, plec) 
    VALUES (%s, %s, %s, %s, %s, %s);"""
    val = nowy_mezczyzna(year)
    wolne_numeryM,numery_zajeteM = numery(wolne_numeryM,numery_zajeteM,val)
    mycursor.execute(sql, val) 

    mydb.commit()

    sql = """INSERT INTO Zawodnicy (imie, nazwisko, numer_na_koszulce, data_dolaczenia, data_odejscia, plec)
     VALUES (%s, %s, %s, %s, %s, %s);"""
    val = nowa_kobieta(year)
    wolne_numeryK,numery_zajeteK = numery(wolne_numeryK,numery_zajeteK,val)
    mycursor.execute(sql, val)

    mydb.commit()

    sql = """INSERT INTO Zawodnicy (imie, nazwisko, numer_na_koszulce, data_dolaczenia, data_odejscia, plec)
    VALUES (%s, %s, %s, %s, %s, %s);"""
    val = nowa_kobieta(year)
    wolne_numeryK,numery_zajeteK = numery(wolne_numeryK,numery_zajeteK,val)
    mycursor.execute(sql, val)

    mydb.commit()
    year += 1

mydb.close() #zamykam połączenie z serverem