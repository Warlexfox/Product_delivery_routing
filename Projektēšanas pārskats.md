# Ievads
### Problēmas nostādne
> Paaugstinoties traporta daudzumam, pieaugusi arī preču piegādes efektivitātes problēma. Laika palielināšana un papildu izmaksas sastrēgumos ceļā, kā arī optimālā laika plānošana manuāli atkarībā no pašreizējās situācijas tas viss negatīvi ietekmē piegādes kvalitāti un arī preču piegādes iespējas pasliktināšanos plānotajā laikā.
### Darba un novērtēšanas mērķis
> Izstrādāt piegādes maršrutēšanas sistēmu, kas ļaus efektīvāk plānot produkcijas piegādes maršrutus, samazināt piegādes termiņus, izmaksas un ceļā pavadīto laiku, tādējādi optimizējot loģistiku. Sistēmai būs automātiski jāaprēķina optimālais maršruts un izvērtēt piegādes efektivitāti atkarībā no lietotāja uzstādītajiem parametriem.

# Līdzīgo risinājumu pārskats
### Līdzīgi tehniskie risinājumi
* [Routific](https://www.routific.com) 
> Maksas piegādes maršrutu optimizācijas serviss, kas palīdz uzņēmumiem plānot un vadīt kurjeru, transportlīdzekļu maršrutus. Tas tiek izmantots loģistikā, lai uzlabotu preču piegādes efektivitāti, samazinātu laiku ceļā un uzlabotu klientu apkalpošanu. Serviss automātiski būvē maršrutus, ņemot vērā kurjeru skaitu, piegādes punktus, un ceļa apstākļus, tāpat prot reālā laikā atjaunināt maršrutus, izmantot kompānijas analītiku un atskaites, izmantojot transportlīdzekļu maršrutēšanas uzdevuma (VRP) risinājuma algoritmus ar mākslīgā intelekta apvienošanu. Tas var integrēties citos servisos caur API, piemēram, e-komercijas platformām vai noliktavu vadības sistēmām. Servisam ir ērta saskarne, kā arī mobilā aplikācija.
* [Route4me](https://www.route4me.com/)
>  Maršrutu plānošanas un optimizācijas programmatūra, ko izmanto loģistikas, piegādes pakalpojumu, lauka servisa pārvaldības un transporta nozarēs. Tā ļauj lietotājiem ātri izveidot optimizētus maršrutus ar vairākiem galamērķiem. Galvenās iespējas ietver reāllaika maršrutu optimizāciju, GPS izsekošanu, mobilo lietotņu integrāciju un analītiku. Route4Me izceļas tirgū ar lietošanas ērtumu, mērogojamību dažāda lieluma uzņēmumiem un tiek apgalvots, ka viņi izmanto progresīvus optimizācijas algoritmus, kas spēj efektīvi apstrādāt sarežģītas maršrutu plānošanas vajadzības.
* [Google Distance Matrix API](https://developers.google.com/maps/documentation/distance-matrix/overview)
> Google Distance Matrix API ir rīks, kas ļauj lietotājiem iegūt attālumus un ceļošanas laikus starp vairākiem sākuma un galamērķiem. Tas tiek izmantots vairākās nozarēs, sākot no loģistikas un piegādes plānošanas līdz maršrutu optimizācijai un pakalpojumu vietas noteikšanai. API aprēķina attālumus, ņemot vērā dažādus transporta veidus, piemēram, auto transportu, velosipēdu, staigāšanu un sabiedrisko transportu. Google Distance Matrix izmanto transportlīdzekļu maršrutēšanas problēmu (VRP) principus, un, balstoties uz reāllaika datiem, piedāvā maršrutu optimizāciju. Šis palīdz maršrutam pielāgoties uz pašreizējiem ceļa apstākļiem, piemēram, remontdarbiem un esošajai satiksmei.
* [OptimoRoute](https://optimoroute.com/)
> OptimoRoute ir mākoņpakalpojums, kas palīdz plānot un optimizēt piegādes maršrutus un grafikus, nodrošinot efektīvāku darbību. Tas piedāvā automatizētu plānošanu un vadītāju mobilo lietotni, kas sniedz detalizētus maršrutus un klientu informāciju. Tiešraides izsekošana ļauj redzēt vadītāju atrašanās vietu un sniedz aptuveno ierašanās laiku. Klienti saņem paziņojumus par piegādes statusu, un piegādes var apstiprināt ar parakstiem un fotogrāfijām. OptimoRoute nodrošina integrāciju ar citām sistēmām, piemēram, e-komercijas platformām, lai automatizētu pasūtījumu izpildi. Analītikas rīki palīdz uzlabot veiktspēju un identificēt problēmas, nodrošinot augstas kvalitātes pakalpojumu. OptimoRoute izmanto transportlīdzekļu maršrutēšanas problēmas (VRP) algoritmus, lai atrastu optimālus risinājumus sarežģītās loģistikas situācijās.
* [Onfleet](https://onfleet.com/)
> Onfleet ir platforma, kas palīdz uzņēmumiem labāk pārvaldīt savas piegādes. Tā piedāvā rīkus, kas ļauj vieglāk plānot maršrutus, sekot līdzi piegādēm reāllaikā un organizēt kurjeru darbu. Piemēram, uzņēmumu vadītāji var redzēt, kur tieši atrodas viņu piegādes, piešķirt kurjeriem uzdevumus un sūtīt automātiskus atgādinājumus klientiem. Platforma ir vienkārša un viegli lietojama gan uzņēmumu vadītājiem, gan kurjeriem, un tā palīdz arī analizēt un uzlabot piegāžu efektivitāti.
### Apkopoti novērojumi
|     Tehniskā risinājuma nosaukums     |     Funkcionalitāte     |     Izmantotais algoritms     |     Izmaksas      |
|---------------------------------------|-------------------------|-------------------------------|-------------------|
|Routific                               |- būvē maršrutus, ņemot vērā kurjeru skaitu, piegādes punktus, un ceļa apstākļus <br>- prot reāllaikā atjaunināt maršrutus, izmantot uzņēmuma analīzi un pārskatus|Transportlīdzekļu maršrutēšanas uzdevuma (VRP) risinājuma algoritmi|Maksas tehniskais risinājums abonementa veidā no $39 līdz $93 atkarībā no abonēšanas formas|
|Route4me                               |- Reāllaika maršrutu pielāgošana un GPS izsekošana <br> - Mobilās lietotnes Android un iOS ierīcēm <br> - Integrācija ar citām sistēmām caur API <br> - Analītika un atskaites par maršrutu efektivitāti <br> - Klientu paziņojumi un ETA (paredzamā ierašanās laika) informācija| - Algorithms for solving the Vehicle Routing Problem (VRP) <br> - Algorithms for solving the Traveling Salesman Problem (TSP) |Risinājums tiek tirgots abonamenta formā un tā cena sākas no $200 mēnesī|
|Google Distance Matrix API             |- Aprēķina divu punktu attālumu un laiku. <br>- Izmanto reāllaika satiksmes datus, ļaujot veikt maršrutu koriģēšanu. <br>- Atbalsta vairākus sākuma un galamērķa punktus. <br>- Daudzveidīgs transporta veidu atbalsts. <br>- Ceļu apstākļu optimizācija, kas ļauj aprēķināt optimālos maršrutus, pamatojoties uz dažādiem parametriem, kā minimālais laiks, īsākais attālums utl.|- Ceļojošās komivojažiera problēmu uzdevuma risināšanas algoritmi (TSP) <br> - Transportlīdzekļu maršrutēšanas problēmu risinājuma algoritmi (VRP)|Nosacīti maksas tehniskais risinājums. Līdz 1000 pieprasījumiem bez maksas, tālāk peldošā cena atkarībā no pieprasījumu skaita. Lai noskaidrotu cenu par vairāk elementiem mēnesī ir jāsazinās ar google pārdevējiem.|
|OptimoRoute                            |- Efektīvu piegādes un lauka darbu maršrutu plānošana un optimizācija  <br> - Reāllaika maršrutu pielāgošana, ņemot vērā izmaiņas pasūtījumos vai apstākļos <br> - Integrācija ar citām sistēmām (e-komercija, ERP, API) <br> - Detalizēta analītika un pārskati par maršrutu efektivitāti|   Transportlīdzekļu maršrutēšanas uzdevuma (VRP) risinājuma algoritmi                            |Maksas tehniskais risinājums, cenas sākas no $19 līdz $39 par transportlīdzekli/mēnesī atkarībā no plāna                   |
|Onfleet                                |- Dispečerim ir lieliska iespēja uzreiz pārredzēt optimizēt un pārvaldīt pasūtījumus reāllaikā, pievienojot un mainot noteikto maršrutu <br> - Piegādes ceļa optimizācija ir lielisks veids, kā samazināt izmaksas <br> - Reāllaika čats ar piegādātāju un iespēju to pārvaldīt <br> - Datu apkopojums un viegla to pārredzamība|- Ceļojošās komivojažiera problēmu uzdevuma risināšanas algoritmi (TSP) <br> - Transportlīdzekļu maršrutēšanas problēmu risinājuma algoritmi (VRP) <br> - Reāllaika maršrutu korekcijas algoritmi, kas ļauj izmantot dinamisko maršruta plānošanu <br> - Uzdevumu piešķiršanas algoritmi, kuri ļauj automātiski piešķirt piegādes produktu kurjeriem <br> - Datu analīzes un prognozēšanas algoritmi, kuri ietver sevī mašīnmācīšanās algoritmus, kuri ļauj analīzēt iepriekšējos piegāžu datus un prognozēt turpmākos pieprasījumus un iespējamās problēmas|Maksas tehniskais risinājums, kuram ir 3 abonementa tipi, kas sākas no 550 $mēnesī līdz individuālajai cenai kurā ietilpst tehniskais atbalsts, kā arī dažādi papildu instrumenti un risinājumi|
### Līdzīgu tehnisko risinājumu intelektuālais algoritms
> Visi līdzīgie tehniskie risinājumi izmanto transportlīdzekļu maršrutēšanas uzdevuma (VRP) risinājuma algoritmus, kas ir apkopots no ceļojošā komivojažiera uzdevuma (TSP), kuras uzdevums ir optimizēt maršrutus vairākiem transportlīdzekļiem, izejot cauri visām pilsētām, kurām nepieciešams veikt minimālu attālumu un laiku. Šādu uzdevumu risināšanas algoritms ir pietiekami daudz, kas savukārt padara neiespējamu to definēt komerciālos projektos. Tomēr ir daudz atvērtu freimvorku šādu uzdevumu risināšanai, piemēram, Google OR-Tools, OptaPlanner, VROOM, Jsprit.
# Tehniskais risinājums
### Prasības
|     Nr.     |     Lietotāju stāsts     |     Prioritāte, <br> MoSCoW metode    |
|-------------|--------------------------|---------------------------------------|
|      1.     | Klienti vēlas interneta pakalpojumu, kurā var grafiski apskatīt piegādes maršrutus un zināt kad un cikos atnāks viņa sūtījums, jo tas ļaus ērti izsekot vispārīgai informācijai par maršrutiem un arī pārliecināties, vai visi maršruti ir pareizi.| M                  |
|      2.     | Menedžeris vēlas, lai lietotne efektīvi sastādītu maršrutu, balstoties uz piegādes punktiem un piegādes laiku, jo vēlas pēc iespējas vairāk samazinātu braukšanas laiku.| M              |
|      3.     | Menedžeris vēlas veikt CRUD operācijas ar katru esošo maršrutu un tā galamērķi, jo vēlas ātri un viegli izmainīt informāciju, ja viņš nokļūdījās informācijas ievades laikā vai arī ir notikušas izmaiņas.| M              |
|      4.    | Menedžeris vēlas uzturēt atsevišķus, savā starpā nesaistītus, maršrutus un piegāžu maršrutu vēsturi, jo tas nodrošina caurspīdīgumu un izsekojamību.| M        |
|      5.    | Menedžeris vēlas, lai pēc iespējas mazāk vadītāju būtu iesaistīti, jo tas samazina izmaksās dažādiem vadītājiem.| M                    |
|      6.     | Menedžeris vēlas iespēju iedot lietotnei failu ar galamērķu sarakstu, jo nevēlas patstāvīgi pārkopēt informāciju.| S                  |
|      7.     | Autovadītājs vēlas redzēt tikai savus piegādes maršrutus, jo tas palīdzēs koncentrēties savam darbam.| S                    |
|      8.     | Menedžeris vēlas vākt statistiku par piegādēm: dažāda statistika par nobraukto attālumu, par paku piegādi, jo tas nodrošina analīzi un ērtu piekļuvi datiem.| C                    |
|      9.     | Autovadītāji vēlas, lai slodze būtu sadalīta vienlīdzīgi, jo tas samazinās darba apjomu.| C                    |
|      10.    | Autovadītājs vēlas saņemt aktuālus datus par satiksmes apstākļiem, jo tas palīdz izvairīties no sastrēgumiem un samazināt piegādes kavējumus.| C                   |

### Algoritms

Izstrādātais algoritms ir piegādes maršrutu optimizācijas risinājums, kas izmanto pielāgotu loģiku transportlīdzekļu maršrutēšanas problēmas (VRP) risināšanai. Tas ņem vērā šādus faktorus: vadītāju prioritātes, piegādes laika logus un ceļa attālumus, lai minimizētu braukšanas laiku. Tehniskajā izpildē tiek izmantoti Python moduļi kā datetime un googlemaps, lai veiktu attālumu aprēķinus un laika logu analīzi. Algoritma mērķis ir nodrošināt optimālu maršruta plānošanu loģistikas uzdevumiem, kas arī vienlaicīgi samazina manuālas plānošanas nepieciešamību.


Galvenās funkcijas:

1. Maršrutu plānošana: Algoritms izvērtē pieejamos vadītājus un piegādes punktus, aprēķina attālumus un braukšanas laikus, un izvēlas optimālo piegādes secību.
2. Laika logu ievērošana: Katrs piegādes punkts tiek plānots tā, lai ievērotu noteiktos piegādes laika logus, vienlaikus maksimāli samazinot kavējumus.
3. Vadītāju noslodzes balansēšana: Algoritms nodrošina, ka neviena vadītāja darba laiks nepārsniedz 8 stundas dienā.
4. Neizpildāmo piegāžu identificēšana: Situācijās, kad visas piegādes nevar izpildīt pieejamo vadītāju ierobežojumu dēļ, šīs piegādes tiek atzīmētas kā "neizpildāmas".
5. Adrešu grupēšana pēc vadītājiem: Piegādes tiek grupētas atsevišķās sekvencēs katram vadītājam ar secības numuriem, kas atspoguļo izpildes kārtību.

### Konceptu modelis
![Konceptu modelis](https://github.com/user-attachments/assets/bfbe1728-58e8-409c-95d5-f01c99c65932)

### Tehnoloģiju steks
* Frontend
> - HTML <br>
> - JavaScript <br>
> - CSS <br>
* Backend
> - Satvars: Flask <br>
> - Programmēšanas valoda: Python <br>
> - OS: Ubuntu Server <br>
> - Tīmekļa serveris: Ngrok <br>
> - Datu bāze: SQLite <br>

### Programmatūras apraksts
Projekta rezultātā tika izveidota tīmekļvietne, kurā var iegūt optimizētus piegādes maršrutus ievadot pieejamos autovadītājus un nepieciešamos galapunktus. 
Tīmeķlvietnē ir īstenotas sekojošas lietas:
> - Autorizēšanās
> - Autovadītāju pievienošana un dzēšana
> - Vairāku neatkarīgu maršrutu izveidi un dzēšanu.
> - Iespēju maršrutam importēt sarakstu ar galapunktiem, kā arī manuāli ievadīt galapunktu datus un dzēst maršrutam galapunktus. Veicot pievienošanu vai dzēšanu, optimizētais maršruts tiek pārrēķināts.
> - Iespēju eksportēt optimizēto maršrutu
> - Optimizēto maršrutu grafiska pārskatīšana uz kartes ar vizuāli atšķiramiem dažādu vadītāju piegādes maršrutiem.

# Novērtējums

### Novērtēšanas plāns

#### Mērķis

Novērtējuma mērķis ir pārbaudīt, vai maršrutu optimizācijas algoritms spēj nodrošināt efektīvu maršrutu plānošanu, samazinot vadītāju darba slodzi un laika patēriņu, kā arī identificēt situācijas, kurās piegādes nav iespējamas, ņemot vērā laika logus un resursu pieejamību.

#### Ieejas mainīgie

> - Vadītāju saraksts ar sākotnējo atrašanās vietu un prioritāti.
> - Piegādes vietas ar laika logiem un koordinātēm.
> - Algoritma iestatījumi (maksimālais autovadītāja darba laiks, vidējais ātrums).

#### Novērtēšanas mēri

> - Vai algoritms ir respektējis autovadītāju darba laikus
> - Vai piegādēm netiek pārsniegti laika logi
> - Cik daudz piegāžu tiek novērtēti, kā nepiegādājami

### Novērtēšanas rezultāti

# Secinājumi

