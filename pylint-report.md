# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksen lopullisesta versiosta (koodi on
tarkastettu komennolla `pylint *.py` sovelluksen hakemistossa):

```
************* Module app
app.py:22:0: C0103: Constant name "page_size" doesn't conform to UPPER_CASE naming style (invalid-name)
app.py:334:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:489:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
************* Module config
config.py:3:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:8:0: C0103: Constant name "time_queries" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module movies
movies.py:42:0: R0913: Too many arguments (6/5) (too-many-arguments)
movies.py:42:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
movies.py:61:0: R0913: Too many arguments (6/5) (too-many-arguments)
movies.py:61:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
************* Module seed
seed.py:8:0: C0103: Constant name "user_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:9:0: C0103: Constant name "movie_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:10:0: C0103: Constant name "review_count" doesn't conform to UPPER_CASE naming style (invalid-name)

Your code has been rated at 9.80/10
```

Seuraavassa käyn läpi raportin ilmoitukset. Moni ilmoitus koskee samaa asiaa,
joten käsittelemme samanlaiset ilmoitukset yhteisesti.

## Vakioiden nimet

Raportissa on seuraavat ilmoitukset liittyen vakionimiin:

```
app.py:22:0: C0103: Constant name "page_size" doesn't conform to UPPER_CASE naming style (invalid-name)
config.py:3:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
db.py:8:0: C0103: Constant name "time_queries" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:8:0: C0103: Constant name "user_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:9:0: C0103: Constant name "movie_count" doesn't conform to UPPER_CASE naming style (invalid-name)
seed.py:10:0: C0103: Constant name "review_count" doesn't conform to UPPER_CASE naming style (invalid-name)
```

Nämä ilmoitukset koskevat koodin päätasolla määriteltyjä muuttujia, jotka
Pylint tulkitsee vakioiksi ja joiden nimien tulisi olla suuraakkosin
kirjoitettuja. Kurssimateriaalin esimerkkisovelluksen tapaan päätason
muuttujien nimet on kuitenkin kirjoitettu pienillä kirjaimilla, mikä näyttää
tässä yhteydessä selkeämmältä. Muuttujaa `secret_key` käytetään koodissa näin:

```python
app.secret_key = config.secret_key
```

## Palautusarvojen epäjohdonmukaisuus

Raportissa on seuraavat ilmoitukset:

```
app.py:334:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:489:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```

Ensimmäinen ilmoitus koskee funktiota `remove_movie`:

```python
@app.route("/remove_movie/<int:movie_id>", methods=["GET", "POST"])
def remove_movie(movie_id):
    """Show the removal confirmation or remove a movie."""
    ...
    if request.method == "GET":
        return render_template("remove_movie.html", movie=movie)

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            movies.remove_movie(movie_id)
            flash("Elokuvan poistaminen onnistui", "success")
            return redirect("/")
        return redirect("/movie/" + str(movie_id))
```

Funktio palauttaa arvon, kun `request.method` on `GET` tai `POST`, mutta
periaatteessa voisi tulla tilanne, jossa metodi on jotain muuta eikä koodi
palauttaisi arvoa. Käytännössä tällaista tilannetta ei voi tulla, koska
funktion dekoraattori rajaa sallitut metodit `GET`- ja `POST`-metodeihin.
Toinen ilmoitus koskee vastaavalla tavalla funktiota `login`, jonka
dekoraattorissa on sama rajoitus. Koodin selkeyden vuoksi erillistä
loppupalautusta ei ole lisätty.

## Liian monta parametria

Raportissa on seuraavat ilmoitukset:

```
movies.py:42:0: R0913: Too many arguments (6/5) (too-many-arguments)
movies.py:42:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
movies.py:61:0: R0913: Too many arguments (6/5) (too-many-arguments)
movies.py:61:0: R0917: Too many positional arguments (6/5) (too-many-positional-arguments)
```

Ensimmäinen ilmoitusten pari koskee funktiota `add_movie`:

```python
def add_movie(title, year, description, user_id, genre_ids, age_rating_id):
    """Add a movie and its classifications, and return its ID."""
```

Funktion parametrit vastaavat suoraan elokuvaan tallennettavia tietoja:
elokuvan nimi, vuosi, kuvaus, lisääjä, genret ja ikäraja. Parametrien määrää
voisi pienentää yhdistämällä useita parametreja yhdeksi tietorakenteeksi,
mutta tässä se heikentäisi koodin selkeyttä, koska jokainen parametri kuvaa
omaa, selkeästi nimettyä asiaa. Toinen ilmoitusten pari koskee vastaavasti
funktiota `update_movie`, jolla on samat parametrit paitsi että
`user_id`-parametrin tilalla on `movie_id`-parametri.
