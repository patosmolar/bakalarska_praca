# iŽalúzie - Použivateľská príručka

# # Pridanie užívateľa do databázy

Po úspešnej inštalácií a aktivovanom virtal enviromente ([Installation Manual](README.md)) spustiť príkazom > python.  
\>\>\>from bakalarka import db  
\>\>\>from bakalarka.models import User  
\>\>\>from flask_bcrypt import Bcrypt  
\>\>\>b = Bcrypt()  
\>\>\>pw = b.generate_password_hash('heslo')  
\>\>\>user = User(username='username',email='email@email.com&#8203;',password=pw,calendarID='-1')  
\>\>\>db.session.add(user)  
\>\>\>db.session.commit()  

# # Používanie

1. Po úspešnej inštalácií a aktivovanom virtal enviromente ([Installation Manual](README.md)) spustiť príkazom > run.py&#8203;.
2. V programe Google Chrome prejdeme na adresu http://127.0.0.1:5000.
3. Na stránke prihlásenia zadať požadovaný email a heslo.('test@test.com&#8203;','password')
4. Aplikácia vás vyzve o prihlásenie pomocou konta Google.(neskoršie plánovanie pomocou kalendára)
5. Po prihlásení je zobrazená hlavná stránka HOME.
6. Ľubovoĺná zmena posuvníkov je reprezentovaná graficky.
7. Po stlačení tlačidla 'Nastavit' sledujeme výpis v konzole.
8. Po prejdení na stránku plánovača aplikácia presmeruje na Accout.
9. V zozname kalendárov si vyberiete požadovaný kalendár a potvrdíme tlačidlom (Optimálne si vytvoriť nový kalendár iba pre účely plánovača nech sa váš hlavný nezahltí [Návod](https://support.google.com/calendar/answer/37095?hl=sk)).
10. Po úspešnom výbere prejdeme na stránku plánovača.
11. Pre pridanie udalosti  vypíšeme potrebné údaje a potvrdíme tlačidlom 'Submit'.
12. Pre odstránenie udalosti vyberieme udalosť zo zoznamu a potvrdíme tlačidlom 'Submit'.
13. Obe akcie vidíme zpísané v kalendári, a po prejdení na stránku Account sledujeme výpis zoznamu úloh v CMD konzole.
14. Odhlásenie prebieha pomocou navigačného panela (Logout).

