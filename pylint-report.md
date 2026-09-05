# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksen lopullisesta versiosta (koodi on tarkastettu komennolla `pylint *.py` sovelluksen hakemistossa):

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:17:0: C0103: Constant name "page_size" doesn't conform to UPPER_CASE naming style (invalid-name)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:23:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:30:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:47:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:57:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:67:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:81:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:92:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:108:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:121:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:128:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:141:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:160:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:180:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:180:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:200:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:220:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:224:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:245:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:245:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:263:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module movies
movies.py:1:0: C0114: Missing module docstring (missing-module-docstring)
movies.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
movies.py:7:0: C0116: Missing function or method docstring (missing-function-docstring)
movies.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
movies.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
movies.py:27:0: C0116: Missing function or method docstring (missing-function-docstring)
movies.py:35:0: C0116: Missing function or method docstring (missing-function-docstring)
movies.py:35:0: R0913: Too many arguments (6/5) (too-many-arguments)
movies.py:35:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
movies.py:53:0: C0116: Missing function or method docstring (missing-function-docstring)
movies.py:53:0: R0913: Too many arguments (6/5) (too-many-arguments)
movies.py:53:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
movies.py:73:0: C0116: Missing function or method docstring (missing-function-docstring)
movies.py:83:0: C0116: Missing function or method docstring (missing-function-docstring)
movies.py:104:0: C0116: Missing function or method docstring (missing-function-docstring)
movies.py:108:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module reviews
reviews.py:1:0: C0114: Missing module docstring (missing-module-docstring)
reviews.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:11:0: C0116: Missing function or method docstring (missing-function-docstring)
reviews.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module seed
seed.py:1:0: C0114: Missing module docstring (missing-module-docstring)
seed.py:6:0: C0103: Constant name "user_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:7:0: C0103: Constant name "movie_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:8:0: C0103: Constant name "review_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:10:0: R0914: Too many local variables (17/15) (too-many-locals)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:5:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:25:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.29/10
```

Seuraavassa käyn läpi raportin ilmoitukset. Moni ilmoitus koskee samaa asiaa, joten käsittelemme samanlaiset ilmoitukset yhteisesti.

## Docstring-kommentit

Suurin osa raportin ilmoituksista koskee puuttuvia docstring-kommentteja:

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
...
```

Ilmoitus C0114 koskee tiedoston alussa olevan kommentin (docstring) puuttumista ja ilmoitus C0116 funktion alussa olevan kommentin puuttumista. Kurssimateriaalin mukaisesti sovelluksen funktiot on nimetty kuvaavasti, jolloin koodin on helppo lukea ilman docstring-kommentteja, eikä kurssilla ole vaatimuksena kirjoittaa niitä. Siksi en lisännyt docstring-kommentteja koodiin.

## Vakioiden nimet

Raportissa on seuraavat ilmoitukset liittyen vakionimiin:

```
app.py:17:0: C0103: Constant name "page_size" doesn't conform to UPPER_CASE naming style (invalid-name)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:6:0: C0103: Constant name "user_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:7:0: C0103: Constant name "movie_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:8:0: C0103: Constant name "review_count" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Nämä ilmoitukset koskevat koodin päätasolla määriteltyjä muuttujia, jotka Pylint tulkitsee vakioiksi ja joiden nimien tulisi olla suuraakkosin kirjoitettuja. Kuitenkin esimerkkisovelluksen tapaan tässä sovelluksessa päätason muuttujien nimet on kirjoitettu pienillä kirjaimilla, mikä näyttää tässä tilanteessa paremmalta. Muuttujaa `secret_key` käytetään koodissa näin:

```python
app.secret_key = config.secret_key
```

## Vaarallinen oletusarvo

Raportissa on seuraavat ilmoitukset liittyen vaaralliseen oletusarvoon:

```
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

Ilmoitukset koskevat esimerkiksi seuraavaa funktiota:

```python
def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
```

Parametrin oletusarvo `[]` on tyhjä lista. Ongelmaksi voisi tulla, että sama oletusarvona oleva listaolio on jaettu kaikkien funktion kutsujen kesken, ja jos jossain kutsussa listan sisältöä muutettaisiin, muutos näkyisi myös muissa kutsuissa. Käytännössä tämä ei kuitenkaan haittaa, koska koodi ei koskaan muuta listaoliota, vaan funktiolle annetaan joko parametrina uusi lista tai käytetään tyhjää listaa sellaisenaan.

## Palautusarvojen epäjohdonmukaisuus

Raportissa on seuraavat ilmoitukset:

```
app.py:180:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:245:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```

Ensimmäinen ilmoitus koskee seuraavaa funktiota:

```python
@app.route("/remove_movie/<int:movie_id>", methods=["GET", "POST"])
def remove_movie(movie_id):
    ...
    if request.method == "GET":
        return render_template("remove_movie.html", movie=movie)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            movies.remove_movie(movie_id)
            return redirect("/")
        return redirect("/movie/" + str(movie_id))
```

Tässä funktio palauttaa arvon, kun `request.method` on `GET` tai `POST`, mutta periaatteessa voisi tulla tilanne, jossa `request.method` on jotain muuta eikä koodi palauttaisi arvoa. Käytännössä tällainen tilanne ei ole kuitenkaan mahdollinen, koska funktion dekoraattorissa on vaatimus, että metodin tulee olla `GET` tai `POST`. Niinpä tässä tapauksessa ei ole riskiä, että funktio ei jossain tilanteessa palauttaisi arvoa. Toinen ilmoitus koskee vastaavalla tavalla funktiota `login`, jonka dekoraattorissa on sama vaatimus.

## Liian monta parametria

Raportissa on seuraavat ilmoitukset:

```
movies.py:35:0: R0913: Too many arguments (6/5) (too-many-arguments)
movies.py:35:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
movies.py:53:0: R0913: Too many arguments (6/5) (too-many-arguments)
movies.py:53:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
```

Ensimmäinen ilmoitusten pari koskee seuraavaa funktiota:

```python
def add_movie(title, year, description, user_id, genre_ids, age_rating_id):
```

Funktion parametrit vastaavat suoraan elokuvaan tallennettavia tietoja: elokuvan nimi, vuosi, kuvaus, lisääjä, genret ja ikäraja. Parametrien määrää voisi pienentää yhdistämällä useita parametreja yhdeksi tietorakenteeksi, mutta tässä se heikentäisi koodin selkeyttä, koska jokainen parametri kuvaa omaa, selkeästi nimettyä asiaa. Toinen ilmoitusten pari koskee vastaavasti funktiota `update_movie`, jolla on samat parametrit paitsi että `user_id`-parametrin tilalla on `movie_id`-parametri.

## Liian monta paikallista muuttujaa

Raportissa on seuraava ilmoitus:

```
seed.py:10:0: R0914: Too many local variables (17/15) (too-many-locals)
```

Ilmoitus koskee tiedoston `seed.py` funktiota `main`, joka luo tietokantaan suuren määrän testidataa. Funktiossa on paikallisia muuttujia esimerkiksi lisättävien käyttäjien, elokuvien ja arvostelujen tietorakenteille. Funktion voisi jakaa useampaan funktion, mutta koska kyseessä on vain testidatan luomiseen tarkoitettu apuskripti, en nähnyt tätä tarpeellisena.
