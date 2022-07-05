from multiprocessing import connection
import mysql.connector
import numpy as np

mydb = mysql.connector.connect(
  host="giniewicz.it",
  user="team5",
  password="te@mSP@ss",
  database="team5"
)

def scores(n):
    s=[]
    for i in range(3):
        if n!=0:
            a=np.random.randint(0,n)
            s.append(a)
            n=n-a
        else:
            s.append(0)
    s.append(n)
    return s
def assign_players():
    mycursor = mydb.cursor()

    mycursor.execute("SELECT Mecze.id, data,Wynik_naszej_druzyny FROM Mecze LEFT JOIN Terminarz ON Mecze.id = Terminarz.id")
    matches = np.fromiter(mycursor.fetchall(), count=-1 , dtype=('i4,M8[D],i4'))
        
    mycursor.execute("SELECT id, data_dolaczenia, data_odejscia FROM Zawodnicy")

    players = np.fromiter(mycursor.fetchall(), count=-1 , dtype=('i4,M8[D],M8[D]'))
    players_2d = np.array([[player[0], player[1], player[2]] for player in players])

    for match in matches:
        candidate_players_bool = (players_2d[:,1] < match[1]) & (match[1] < players_2d[:, 2])
        candidate_players = players_2d[candidate_players_bool,:]

        players_for_match = np.random.choice(candidate_players[:,0], 4, replace=False)
        s=scores(match[2])
        i=0
        for player in players_for_match:
            mycursor.execute(
                     """INSERT INTO Zawodnicy_Mecze (id_meczu, id_zawodnika,ilosc_punktow) 
                    VALUES (%s, %s,%s)""", (int(match[0]), int(player),int(s[i])))
            i=i+1

    mydb.commit()

assign_players()
mydb.close()
