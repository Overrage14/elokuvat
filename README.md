# Elokuvat

Elokuvat on Flaskilla ja SQLitellä toteutettu web-sovellus, jossa käyttäjät
voivat jakaa tietoa elokuvista, luokitella niitä ja kirjoittaa arvosteluja.

## Sovelluksen toiminnot

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään elokuvia sekä muokkaamaan ja poistamaan niitä.
* Käyttäjä näkee sovellukseen lisätyt elokuvat.
* Käyttäjä pystyy etsimään elokuvia hakusanalla ja genren perusteella.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän
  lisäämät elokuvat.
* Käyttäjä pystyy valitsemaan elokuvalle yhden tai useamman luokittelun:
  * Genre: toiminta, animaatio, dokumentti, draama, kauhu, komedia,
    romanttinen, scifi, seikkailu tai trilleri
  * Ikäraja: S, 7, 12, 16 tai 18
* Käyttäjä pystyy antamaan elokuvalle arvostelun, joka sisältää kommentin ja
  arvosanan. Yksi käyttäjä voi antaa yhdelle elokuvalle yhden arvostelun.
  Elokuvasta näytetään arvostelut ja keskimääräinen arvosana.

Pääasiallinen tietokohde on elokuva ja toissijainen tietokohde on elokuvan
arvostelu.

## Tekniset tiedot

* Sovellus on toteutettu Pythonilla ja Flask-kirjastolla.
* Tietokantana on SQLite, ja sitä käytetään suoraan SQL-kyselyillä ilman ORMia.
* Käyttöliittymä muodostuu Flaskin sivupohjista, eikä sovellus käytä
  JavaScriptia.
* Ulkoasu on toteutettu itse tiedostossa `static/main.css` ilman ulkoisia
  CSS-kirjastoja.
* Salasanat tallennetaan tiivisteinä ja SQL-kyselyissä käytetään parametreja.
* Kaikissa lomakkeissa on CSRF-suojaus.
* Käyttöliittymässä on huomioitu saavutettavuutta muun muassa
  `label`-elementeillä, sivun kielellä ja semanttisella HTML-rakenteella.
* Suuren tietomäärän käsittelyä varten sovelluksessa on sivutus ja tietokannan
  indeksit.
* Koodi on jaettu selkeisiin moduuleihin, ja moduulit sekä funktiot on
  dokumentoitu docstring-kommenteilla.

## Projektin rakenne

| Tiedosto | Kuvaus |
|---|---|
| `app.py` | Flask-sovellus, reitit ja lomakkeiden käsittely |
| `config.py` | Sovelluksen salainen avain |
| `db.py` | Tietokantayhteydet ja SQL-kyselyjen suorittaminen |
| `movies.py` | Elokuviin ja luokitteluihin liittyvät tietokantaoperaatiot |
| `reviews.py` | Arvosteluihin liittyvät tietokantaoperaatiot |
| `users.py` | Käyttäjiin ja kirjautumiseen liittyvät tietokantaoperaatiot |
| `schema.sql` | Tietokannan taulut ja indeksit |
| `init.sql` | Genrejen ja ikärajojen alkutiedot |
| `seed.py` | Suuren testiaineiston luominen |
| `templates/` | HTML-sivupohjat |
| `static/main.css` | Sovelluksen tyylit |
| `pylint-report.md` | Pylint-työkalun raportti ja huomautusten selitykset |

## Asennus ja käynnistys

Asenna `flask`-kirjasto:

```
$ pip install flask
```

Luo tietokannan taulut ja lisää alkutiedot:

```
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
```

Käynnistä sovellus:

```
$ flask run
```

## Sovelluksen testaaminen

1. Luo tunnus ja kirjaudu sisään.
2. Lisää elokuva etusivun `Uusi elokuva` -linkin kautta. Valitse elokuvalle
   yksi tai useampi genre ja halutessasi ikäraja.
3. Avaa elokuvan sivu ja anna sille arvostelu.
4. Muokkaa ja poista lisäämäsi elokuva elokuvan sivun linkkien kautta.
5. Etsi elokuvia hakusanalla tai genrellä etusivun `Etsi elokuva` -linkin
   kautta.
6. Avaa käyttäjän sivu napsauttamalla käyttäjänimeä. Sivu näyttää käyttäjän
   tilastot ja lisäämät elokuvat.

## Suuri tietomäärä

### Testidatan luominen

Tiedosto `seed.py` luo tietokantaan suuren määrän testidataa: 1000 käyttäjää,
100000 elokuvaa ja 500000 arvostelua. Testidatan voi luoda näin:

```
$ rm -f database.db
$ sqlite3 database.db < schema.sql
$ sqlite3 database.db < init.sql
$ python3 seed.py
```

Testidatan käyttäjätunnukset ovat `kayttaja1`, `kayttaja2`, ...,
`kayttaja1000`, ja kaikkien salasana on `salasana`.

### Mittaukset

Sovelluksen voi käynnistää niin, että se tulostaa jokaisen
tietokantaoperaation keston:

```
$ python3 app.py --time-db
```

Tällöin jokaisen sivun latauksen yhteydessä tulostuu esimerkiksi seuraava rivi:

```
0.4 ms  SELECT movies.id, movies.title, movies.year, users.id user_id, users.username, AVG(reviews.rating) avg_rating, COUNT(reviews.id) review_count FROM movies JOIN users ON movies.user_id = users.id LEFT JOIN reviews ON movies.id = reviews.movie_id GROUP BY movies.id ORDER BY movies.id DESC LIMIT ? OFFSET ?
```

Testasin sovelluksen toiminnan tällä tietomäärällä mittaamalla sivujen
latausaikoja komennon `curl` avulla. Jokaisen tuloksen kolme lukua ovat kolmen
mittauksen kestot sekunteina:

| Sivu | Latausaika |
|---|---|
| Etusivu (10 elokuvan sivu) | 0.003 / 0.003 / 0.003 |
| Elokuvan sivu | 0.003 / 0.002 / 0.002 |
| Hakusanahaku ("Elokuva 1") | 0.031 / 0.031 / 0.033 |
| Genrehaku | 0.030 / 0.025 / 0.034 |
| Käyttäjäsivu | 0.003 / 0.003 / 0.002 |

Kaikki sivut latautuvat nopeasti. Hakusana- ja genrehaku ovat hitaimpia, koska
hakusana voi esiintyä myös elokuvan kuvauksessa, jolloin SQL-komennon on
käytävä läpi kaikki 100000 elokuvaa. Haku on silti selvästi alle sekunnin.

### Indeksien vaikutus

Selvitin myös, mikä merkitys tietokantaan lisätyillä indekseillä on poistamalla
indeksit väliaikaisesti ja toistamalla mittaukset:

| Sivu | Indeksit | Ilman indeksejä |
|---|---|---|
| Etusivu (10 elokuvan sivu) | 0.003 / 0.003 / 0.003 | 0.005 / 0.005 / 0.005 |
| Elokuvan sivu | 0.003 / 0.002 / 0.002 | 0.002 / 0.003 / 0.002 |
| Hakusanahaku ("Elokuva 1") | 0.031 / 0.031 / 0.033 | 0.029 / 0.028 / 0.037 |
| Genrehaku | 0.030 / 0.025 / 0.034 | 0.025 / 0.027 / 0.023 |
| Käyttäjäsivu | 0.003 / 0.003 / 0.002 | 0.030 / 0.027 / 0.023 |

Indeksit nopeuttavat käyttäjäsivua noin kymmenkertaisesti. Ilman indeksejä
käyttäjän elokuvien haun on luettava kaikki 100000 elokuvaa ja käyttäjän
arvostelujen määrän laskeminen kaikki 500000 arvostelua. Sen sijaan hakusana- ja
genrehaku eivät hyödy indekseistä, koska haku käy joka tapauksessa läpi kaikki
elokuvat. Etusivun ja elokuvan sivun arvostelujen haku toimii myös ilman
erikseen luotuja indeksejä, koska arvostelu-taulun `UNIQUE`-ehto muodostaa
tietokantaan automaattisen indeksin, joka kattaa saman haun. Kyselyt käyttävät
indeksejä, kuten käy ilmi `EXPLAIN QUERY PLAN` -komennon tuloksista.
Käyttäjäsivun kysely käyttää indeksejä `idx_movies_user_id`,
`idx_reviews_movie_id` ja `idx_reviews_user_id`:

```
QUERY PLAN
|--SEARCH movies USING INDEX idx_movies_user_id (user_id=?)
`--SEARCH reviews USING INDEX idx_reviews_movie_id (movie_id=?) LEFT-JOIN
```

```
QUERY PLAN
`--SEARCH reviews USING COVERING INDEX idx_reviews_user_id (user_id=?)
```

Suuren tietomäärän käsittelyä helpottaa lisäksi sivutus: etusivu,
hakutulokset ja käyttäjäsivun elokuvalista näyttävät kerralla vain 10 kohdetta,
vaikka tietokannassa olisi satojatuhansia rivejä.

## Koodin laatu

Sovelluksen Python-koodi on tarkastettu Pylint-työkalulla. Raportti ja
jäljellä olevien huomautusten selitykset löytyvät tiedostosta
`pylint-report.md`.
