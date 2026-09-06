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
* Käyttäjä pystyy antamaan elokuvalle arvostelun, joka sisältää kommentin ja arvosanan (yhden arvostelun per elokuva). Elokuvasta näytetään arvostelut ja keskimääräinen arvosana.

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

Tiedosto `seed.py` luo tietokantaan suuren määrän testidataa: 1000 käyttäjää, 100000 elokuvaa ja 500000 arvostelua. Testidatan voi luoda näin:

```
$ rm -f database.db
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
$ python3 seed.py
```

Testasin sovelluksen toiminnan tällä tietomäärällä mittaamalla sivujen latausaikoja komennon `curl` avulla. Jokaisen tuloksen kolme lukua ovat kolmen mittauksen kestot sekunteina:

| Sivu | Latausaika |
|---|---|
| Etusivu (10 elokuvan sivu) | 0.003 / 0.003 / 0.003 |
| Elokuvan sivu | 0.003 / 0.002 / 0.002 |
| Hakusanahaku ("Elokuva 1") | 0.031 / 0.031 / 0.033 |
| Genrehaku | 0.030 / 0.025 / 0.034 |
| Käyttäjäsivu | 0.003 / 0.003 / 0.002 |

Kaikki sivut latautuvat nopeasti. Hakusana- ja genrehaku ovat hitaimpia, koska hakusana voi esiintyä myös elokuvan kuvauksessa, jolloin SQL-komennon on käytävä läpi kaikki 100000 elokuvaa. Haku on silti selvästi alle sekunnin.

Selvitin myös, mikä merkitys tietokantaan lisätyillä indekseillä on poistamalla indeksit väliaikaisesti ja toistamalla mittaukset:

| Sivu | Indeksit | Ilman indeksejä |
|---|---|---|
| Etusivu (10 elokuvan sivu) | 0.003 / 0.003 / 0.003 | 0.005 / 0.005 / 0.005 |
| Elokuvan sivu | 0.003 / 0.002 / 0.002 | 0.002 / 0.003 / 0.002 |
| Hakusanahaku ("Elokuva 1") | 0.031 / 0.031 / 0.033 | 0.029 / 0.028 / 0.037 |
| Genrehaku | 0.030 / 0.025 / 0.034 | 0.025 / 0.027 / 0.023 |
| Käyttäjäsivu | 0.003 / 0.003 / 0.002 | 0.030 / 0.027 / 0.023 |

Indeksit nopeuttavat käyttäjäsivua noin kymmenkertaisesti. Ilman indeksejä käyttäjän elokuvien haun on luettava kaikki 100000 elokuvaa ja käyttäjän arvostelujen määrän laskeminen kaikki 500000 arvostelua. Sen sijaan hakusana- ja genrehaku eivät hyödy indekseistä, koska haku käy joka tapauksessa läpi kaikki elokuvat. Etusivun ja elokuvan sivun arvostelujen haku toimii myös ilman erikseen luotuja indeksejä, koska arvostelu-taulun `UNIQUE`-ehto muodostaa tietokantaan automaattisen indeksin, joka kattaa saman haun. Kyselyt käyttävät indeksejä, kuten käy ilmi `EXPLAIN QUERY PLAN` -komennon tuloksista. Käyttäjäsivun kysely käyttää indeksejä `idx_movies_user_id`, `idx_reviews_movie_id` ja `idx_reviews_user_id`:

```
QUERY PLAN
|--SEARCH movies USING INDEX idx_movies_user_id (user_id=?)
`--SEARCH reviews USING INDEX idx_reviews_movie_id (movie_id=?) LEFT-JOIN
```

```
QUERY PLAN
`--SEARCH reviews USING COVERING INDEX idx_reviews_user_id (user_id=?)
```

Suuren tietomäärän käsittelyä helpottaa lisäksi sivutus: etusivu, hakutulokset ja käyttäjäsivun elokuvalista näyttävät kerralla vain 10 kohdetta, vaikka tietokannassa olisi satojatuhansia rivejä.
