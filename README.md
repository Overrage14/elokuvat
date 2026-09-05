# Elokuvat

## Sovelluksen toiminnot

* Sovelluksessa käyttäjät pystyvät jakamaan tietoa elokuvista ja arvostelemaan niitä.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään elokuvia sekä muokkaamaan ja poistamaan niitä.
* Käyttäjä näkee sovellukseen lisätyt elokuvat.
* Käyttäjä pystyy etsimään elokuvia hakusanalla ja genren perusteella.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät elokuvat.
* Käyttäjä pystyy valitsemaan elokuvalle yhden tai useamman luokittelun:
  - Genre: toiminta, animaatio, dokumentti, draama, kauhu, komedia, romanttinen, scifi, seikkailu tai trilleri
  - Ikäraja: S, 7, 12, 16 tai 18
* Käyttäjä pystyy antamaan elokuvalle arvostelun, joka sisältää kommentin ja arvosanan. Elokuvasta näytetään arvostelut ja keskimääräinen arvosana.

Tässä pääasiallinen tietokohde on elokuva ja toissijainen tietokohde on elokuvan arvostelu.

## Sovelluksen asennus

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Voit käynnistää sovelluksen näin:

```
$ flask run
```

Sovelluksen testaaminen on helpointa luomalla ensin tunnus ja kirjautumalla sisään. Uuden elokuvan voi lisätä etusivun linkin kautta. Elokuvan sivulla voi antaa arvostelun, ja omalle elokuvalle näkyy linkit muokkaamiseen ja poistamiseen. Hakusana- ja genrehaun voi tehdä etusivun linkin kautta.

## Sovelluksen testaus suurella tietomäärällä

Tiedosto `seed.py` luo tietokantaan suuren määrän testidataa: 1000 käyttäjää, 10000 elokuvaa ja 50000 arvostelua. Testidatan voi luoda näin:

```
$ rm -f database.db
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
$ python3 seed.py
```

Testasin sovelluksen toiminnan tällä tietomäärällä mittaamalla sivujen latausaikoja komennon `curl` avulla. Jokaisen tuloksen kolme lukua ovat kolmen mittauksen kestot sekunteina:

| Sivu | Latausaika |
|---|---|
| Etusivu (10 elokuvan sivu) | 0.003 / 0.003 / 0.010 |
| Elokuvan sivu | 0.002 / 0.002 / 0.006 |
| Hakusana­haku ("Elokuva 1") | 0.011 / 0.012 / 0.014 |
| Genrehaku | 0.012 / 0.013 / 0.016 |
| Käyttäjäsivu | 0.007 / 0.007 / 0.008 |

Kaikki sivut latautuvat nopeasti. Selvitin myös, mikä merkitys tietokantaan lisätyillä indekseillä on poistamalla indeksit `idx_reviews_movie_id` ja `idx_movie_genres_movie_id` väliaikaisesti ja toistamalla mittaukset:

| Sivu | Latausaika ilman indeksejä |
|---|---|
| Etusivu (10 elokuvan sivu) | 0.024 / 0.028 / 0.029 |
| Elokuvan sivu | 0.009 / 0.009 / 0.020 |
| Genrehaku | 0.012 / 0.016 / 0.021 |
| Käyttäjäsivu | 0.027 / 0.030 / 0.033 |

Indeksit nopeuttavat etusivua ja käyttäjäsivua noin viidestä kymmeneen kertaan, koska arvostelujen keskiarvon laskeminen perustuu hakuun arvosteluista elokuvan id:n perusteella. Hakusana­haun tapauksessa hakusana voi esiintyä myös elokuvan kuvauksessa, jolloin SQL-komennon on käytävä läpi kaikki elokuvat; tällöin indeksi elokuvan nimellä ei voi nopeuttaa hakua. Joka tapauksessa haku on nopea 10000 elokuvan tietomäärällä.

Suuren tietomäärän käsittelyä helpottaa lisäksi etusivun sivutus, joka hakee kerralla vain 10 elokuvaa.
