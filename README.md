# iŽalúzie - Bakalárska práca

INTERNETOVÁ APLIKÁCIA NA OVLÁDANIE EXTERIÉROVÝCH ŽALÚZIÍ.

Kompletná Programová dokumentácia : https://patosmolar.github.io/bakalarska_praca/
Užívateľsá príručka : [a relative link](userManual.md)



# # Inštalačná príručka
V tejto časti sú obsiahnuté všetky potrebné kroky k spránvej inštalácií.
Inštalácia pre Win10 a Google Chrome
### Predpoklady pre inštaláciu
Python 3.0+ 
```
Pyhton 3.X
[https://www.python.org/downloads/]
```
Google Chrome
```
[https://www.google.com/chrome/]
```

Nastavenie virtual enviroment
```
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
$ py -3 -m venv venv
```
Aktivácia virtual enviromentu
```
> venv\Scripts\activate
 ```
Stiahnutie modulu Flask
 ```
$ pip install Flask
 ```
### Inštalácia
Naklonovať/stiahnúť repozitár do priečinku, s prednastaveným virtualenv (viď. predpoklady pre inštaláciu)
 ```
> git clone https://github.com/patosmolar/bakalarska_praca.git
 ```
 Nainštalovať potrebné moduly
  ```
> pip install requirements.txt 
 ```
 Spustiť hlavný modul
 ```
> run.py 
 ```
 V programe Google Chrome prístupiť k loaklite localhost
 ```
[http://127.0.0.1:5000/]
 ```
 
