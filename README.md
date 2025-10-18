# todoapp

Todo-sovelluksessa voi:
- luoda käyttäjätunnuksen ja kirjautua sisään
- lisätä, poistaa, muuttaa taskeja
- merkitä taskeja suoritetuksi
- suorittaa hakua taskeista otsikon mukaan
- filtteröidä oman todo-listansa taskien tilan perusteella
- seurata käyttäjäsivulta käyttäjien lisäämien taskien ja kommenttien lukumäärää
- kommentoida omia ja muiden taskeja


## käyttöönotto

Seuraa kurssin ohjeita tiedoston config.py ja salaisen avaimen luomista varten.
Suorita seuraavat komennot alustaaksesi sovelluksen:

pip install flask

sqlite3 database.db < schema.sql

Sovellus käynnistyy komennolla:

flask run

Tietokannan toimintaa voi halutessaan testata suurella tietomäärällä ajamalla tiedoston seed.py komennolla:

python3 seed.py
