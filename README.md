# todoapp

Todo-sovelluksessa voi:
- luoda käyttäjätunnuksen ja kirjautua sisään
- lisätä, poistaa, muuttaa taskeja
- merkitä taskeja suoritetuksi
- lisätä taskille luonnissa tai editoinnissa halutessaan yhden tai useamman itse keksimänsä luokittelun
- suorittaa hakua taskeista otsikon mukaan
- filtteröidä oman todo-listansa taskien tilan perusteella
- seurata käyttäjäsivulta käyttäjien lisäämien taskien ja kommenttien lukumäärää
- kommentoida omia ja muiden taskeja


## Käyttöönotto

### Suorita seuraavat toiminnot alustaaksesi sovelluksen:
```bash
pip install flask

sqlite3 database.db < schema.sql
```

#### Luo config.py seuraavasti:

**Varmista olevasi sovelluksen juurikansiossa todoapp, luo config.py tiedosto komennolla:**
```bash
touch config.py
```
**Käynnistä python-konsoli komennolla:**

```bash
python3
```

**Kirjoita python-terminaaliin seuraavat komennot:**

```python
import secrets

secrets.token_hex(16)
```

**Kopioi terminaalin antama salainen avain muotoa '39e5b8dd1de7afdc786df2b0cdf7a8f1'**

**Poistu python terminaalista komennolla:**

```python
exit()
```

**Kirjoita config.py tiedostoon seuraava koodirivi, johon kopioit oman salaisen avaimesi - rivin kuuluisi näyttää tältä:**

```python
secret_key = '39e5b8dd1de7afdc786df2b0cdf7a8f1'
```

**Tallennettuasi tiedoston olet valmis käynnistämään sovelluksen.**

#### Sovellus käynnistyy komennolla:

```bash
flask run
```

**Tietokannan toimintaa voi halutessaan testata suurella tietomäärällä ajamalla tiedoston seed.py komennolla:**

```bash
python3 seed.py
```
