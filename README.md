# todoapp

Tarkoituksena on luoda todo-sovellus, jossa voi:
- luoda käyttäjätunnuksen ja kirjautua sisään
- lisätä, poistaa, muuttaa taskeja
- merkitä taskeja suoritetuksi
- suorittaa hakua taskeista statuksen ja/tai otsikon mukaan
- seurata käyttäjäsivulta käyttäjien lisäämien taskien lukumäärää ja statusta


## käyttöönotto

Seuraa kurssin ohjeita tiedoston config.py ja salaisen avaimen luomista varten.
Suorita seuraavat komennot alustaaksesi sovelluksen:
pip install flask
sqlite3 database.db < schema.sql

Sovellus käynnistyy komennolla:
flask run