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
>
* [OptimoRoute](https://optimoroute.com/)
> OptimoRoute ir mākoņpakalpojums, kas palīdz plānot un optimizēt piegādes maršrutus un grafikus, nodrošinot efektīvāku darbību. Tas piedāvā automatizētu plānošanu un vadītāju mobilo lietotni, kas sniedz detalizētus maršrutus un klientu informāciju. Tiešraides izsekošana ļauj redzēt vadītāju atrašanās vietu un sniedz aptuveno ierašanās laiku. Klienti saņem paziņojumus par piegādes statusu, un piegādes var apstiprināt ar parakstiem un fotogrāfijām. OptimoRoute nodrošina integrāciju ar citām sistēmām, piemēram, e-komercijas platformām, lai automatizētu pasūtījumu izpildi. Analītikas rīki palīdz uzlabot veiktspēju un identificēt problēmas, nodrošinot augstas kvalitātes pakalpojumu
### Apkopoti novērojumi
|     Tehniskā risinājuma nosaukums     |     Funkcionalitāte     |     Izmantotais algoritms     |     Izmaksas      |
|---------------------------------------|-------------------------|-------------------------------|-------------------|
|Routific                               |- būvē maršrutus, ņemot vērā kurjeru skaitu, piegādes punktus, un ceļa apstākļus <br>- prot reāllaikā atjaunināt maršrutus, izmantot uzņēmuma analīzi un pārskatus|transportlīdzekļu maršrutēšanas uzdevuma (VRP) risinājuma algoritmi|Maksas tehniskais risinājums abonementa veidā no 39$ līdz 93$ atkarībā no abonēšanas formas|
|Route4me                               |- Reāllaika maršrutu pielāgošana un GPS izsekošana <br> - Mobilās lietotnes Android un iOS ierīcēm <br> - Integrācija ar citām sistēmām caur API <br> - Analītika un atskaites par maršrutu efektivitāti <br> - Klientu paziņojumi un ETA (paredzamā ierašanās laika) informācija| - Algorithms for solving the Vehicle Routing Problem (VRP) <br> - Algorithms for solving the Traveling Salesman Problem (TSP) |Risinājums tiek tirgots abonamenta formā un tā cena sākas no 200$ mēnesī|
|                                       |                         |                               |                   |
|                                       |                         |                               |                   |
|                                       |                         |                               |                   |
### Līdzīgu tehnisko risinājumu intelektuālais algoritms
> Visi līdzīgie tehniskie risinājumi izmanto transportlīdzekļu maršrutēšanas uzdevuma (VRP) risinājuma algoritmus, kas ir apkopots no ceļojošā komivojažiera uzdevuma (TSP), kuras uzdevums ir optimizēt maršrutus vairākiem transportlīdzekļiem, izejot cauri visām pilsētām, kurām nepieciešams veikt minimālu attālumu un laiku. Šādu uzdevumu risināšanas algoritms ir pietiekami daudz, kas savukārt padara neiespējamu to definēt komerciālos projektos. Tomēr ir daudz atvērtu freimvorku šādu uzdevumu risināšanai, piemēram, Google OR-Tools, OptaPlanner, VROOM, Jsprit.
# Tehniskais risinājums
### Prasības
### Konceptu modelis
