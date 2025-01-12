# Preču piegādes maršrutēšana
## Lietošanas instrukcijas operētājsistēmai Windows, izmantojot Visual Studio kodu

1. Izveidojiet mapi, kurā strādāsiet.
2. Izmantojot VScode: Atvērtiet mapi - ```Open Folder``` un atlasiet izveidoto mapi.
3.  Atveriet termināli iekšā VScode (Ctrl+`) un lokāli klonējiet repozitoriju:
    ```bash
    git clone https://github.com/Warlexfox/ProLab2024.git
4. Dodieties iekšā mapē, kurā atrodas repozitorijs: 
    ```bash
    cd ProLab2024
5. Izvietojiet un aktivizējiet virtuālo vidi:
    ```bash
    python -m venv venv
    venv\Scripts\activate
6. Ja rodas problēmas ar venv izvietošanu, ir jāatļauj skriptu izpilde pašreizējam lietotājam PowerShell neierobežotajā režīmā ar administratora tiesībām:
   ```bash
   Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
7. Instalējiet atkarības
   ```bash
   pip install -r requirements.txt
8. Ja "instace" cilnē ir database.db, ieteicams to izdzēst un pēc tam palaist skriptu (Tas noderēs, kad kaut ko mainīsiet, jo, ja algoritma loģika vai elementu savienošana ar datu bāzi izmaiņas, būs kļūdas):
   ```bash
   python init_db.py
10. Palaist tīmekļa lietojumprogrammu:
    ```flask run```
11. Tīmekļa lietojumprogrammu var atvērt adresē, kas tiks parādīta konsolē, parasti tā ir: ```http://127.0.0.1:5000```
12. Pēc darba pabeigšanas ļoti ieteicams atgriezties ierobežotajā režīmā, jo ```Unrestricted``` iestatījums ļauj palaist jebkurus skriptus bez autentifikācijas, kas palielina ļaunprātīga koda palaišanas risku:
    ```bash
    Set-ExecutionPolicy -ExecutionPolicy Restricted -Scope CurrentUser
    
## Tīmekļa lietojumprogramma tiek mitināta Azure platformā un izmanto Flask projektu, kura pamatā ir Werkzeug bibliotēka ar WSGI tīmekļa serveri.
#### Servera adrese:
* http://52.233.129.130:5000
#### Login testa dati:
* Email: 1@mail.com
* Parole: 1

## Dalībnieki 
 - Jānis Kārlis Zāģeris
 - Oleksandr Voznenko
 - Vlads Sokolovs
 - Lauris Keišs
 - Artjoms Šefanovskis
