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

Suorita seuraavat toiminnot alustaaksesi sovelluksen:

pip install flask

sqlite3 database.db < schema.sql

Luo config.py seuraavasti:

Varmista olevasi sovelluksen juurikansiossa todoapp, luo config.py tiedosto komennolla:

touch config.py

Käynnistä python-konsoli komennolla:

python3

Kirjoita python-terminaaliin seuraavat komennot:

import secrets
secrets.token_hex(16)

Kopioi terminaalin antama salainen avain muotoa '39e5b8dd1de7afdc786df2b0cdf7a8f1'

poistu python terminaalista komennolla:

exit()

Kirjoita config.py tiedostoon seuraava koodirivi, johon kopioit oman salaisen avaimesi - rivin kuuluisi näyttää tältä:

secret_key = '39e5b8dd1de7afdc786df2b0cdf7a8f1'

Tallennettuasi tiedoston olet valmis käynnistämään sovelluksen.

Sovellus käynnistyy komennolla:

flask run

Tietokannan toimintaa voi halutessaan testata suurella tietomäärällä ajamalla tiedoston seed.py komennolla:

python3 seed.py
