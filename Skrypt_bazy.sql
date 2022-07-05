
  
        
CREATE TABLE Finanse
(
  id           INT(10)        NOT NULL AUTO_INCREMENT,
  data         DATE           NOT NULL,
  kwota        DECIMAL(13, 2) NOT NULL,
  typ_podmiotu VARCHAR(40)    NOT NULL,
  ID_podmiotu  INT(10)        NULL    ,
  uwagi        VARCHAR(200)   NULL    ,
  ilosc        TINYINT(4)     NULL    ,
  PRIMARY KEY (id)
);

CREATE TABLE Mecze
(
  id                       INT(10)     NOT NULL,
  rezultat                 VARCHAR(40) NOT NULL,
  Wynik_naszej_druzyny     INT(10)     NOT NULL,
  Wynik_druzyny_przeciwnej INT(10)     NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Pracownicy
(
  id                INT(10)     NOT NULL AUTO_INCREMENT,
  imie              VARCHAR(40) NOT NULL,
  nazwisko          VARCHAR(40) NOT NULL,
  stanowisko        VARCHAR(40) NOT NULL,
  data_zatrudnienia DATE        NOT NULL,
  data_odejscia     DATE        NOT NULL,
  pensja            INT(4)      NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Sprzet
(
  id                                    INT(10)     NOT NULL AUTO_INCREMENT,
  typ_sprzetu                           VARCHAR(40) NOT NULL,
  ilosc                                 INT(10)     NOT NULL,
  ilosc_uszkodzonych_lub_zutylizowanych INT(10)     NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Terminarz
(
  id                       INT(10)     NOT NULL AUTO_INCREMENT,
  data                     DATE         NOT NULL,
  przeciwnik               VARCHAR(40) NOT NULL,
  Miejsce_rozegrania_meczu VARCHAR(40) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Zawodnicy
(
  id                INT(10)     NOT NULL AUTO_INCREMENT,
  imie              VARCHAR(40) NOT NULL,
  nazwisko          VARCHAR(40) NOT NULL,
  numer_na_koszulce INT(10)     NOT NULL,
  data_dolaczenia   DATE        NOT NULL,
  data_odejscia     DATE        NOT NULL,
  plec              VARCHAR(40) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE Zawodnicy_Mecze
(
  ilosc_punktow INT(10) NOT NULL,
  id_meczu      INT(10) NOT NULL,
  id_zawodnika  INT(10) NOT NULL,
  PRIMARY KEY (id_meczu, id_zawodnika)
);

ALTER TABLE Mecze
  ADD CONSTRAINT FK_Terminarz_TO_Mecze
    FOREIGN KEY (id)
    REFERENCES Terminarz (id);

ALTER TABLE Zawodnicy_Mecze
  ADD CONSTRAINT FK_Zawodnicy_TO_Zawodnicy_Mecze
    FOREIGN KEY (id_zawodnika)
    REFERENCES Zawodnicy (id);

ALTER TABLE Zawodnicy_Mecze
  ADD CONSTRAINT FK_Mecze_TO_Zawodnicy_Mecze
    FOREIGN KEY (id_meczu)
    REFERENCES Mecze (id);

        
      