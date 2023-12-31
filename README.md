# PORTAMENTO 
> THE PROJECT IS NOT YET UTILIZABLE WITHOUT MODIFYING THE CODE: THERE ARE SOME STATIC PATHS THAT CAN ONLY WORK ON MY COMPUTERS. 
>> These are present in the GameManager Class and in the Python scripts.


*Portamento: Machine Learning for music cataloguing and a three-dimensional interface to highlight its inherent nuances.*
Read the thesis (in italian): [thesis](https://github.com/nicoloddo/PORTAMENTO/blob/master/THESIS.pdf)


Portamento is a music cataloguing software that uses a selfmade mod of the BIRCH algorithm to cluster a database of tracks. The parameters of each song are withdrawn from Spotify's audio analysis databases. The interface is done using the Unity Engine with an approach similar to videogames that obtains an interactive exploration of the clustering tree hierarchy.
The backend is written in Python, while the frontend is written in C#.

[![Watch the video](https://i.imgur.com/wOLEDrZ.jpg)](https://youtu.be/aSUIdFPvFPQ)
This video shows the functioning of the Beta version.

Database references:
1. **[Spotify](https://developer.spotify.com/documentation/web-api/reference/)**, from which I get the tracks' metadata and analysis.
2. **[MusicBrainz](https://musicbrainz.org/)**, additional informations about the tracks (*to be implemented in future developments*).


### Frontend
Written in C# on the **Unity Engine**, the interface plays a very big role in the project as it follows one of the main ideas behind it by trying to highlight the actual impossibility to reduce music to a discreet number of clusters inferior to the number of the songs. It provides in fact a way to interactively explore a tree structure of clusters in which the root consist of the entire database, while the leaves are actually every sample (in that case song) of the database. This is as image of the idea that, at the highest level of detail, every song constitute a genre by itself. Moreover, the clustering parameters and weights are highly tweakable by the user to satisfy every user-specific need of categorization.

The user will be able to move inside a 3D space in which every cluster is located at specific 3 coordinates chosen from all its parameters. These 3 parameters are in fact the meaning given to the 3 axis of the space and can be modified by the user itself. It is also possible to go inside a cluster, thus going down in the tree hierarchy. By entering a cluster the user will see a totally similar scene but with the clusters that belongs to the new node of the hierarchy in which the user is now located.

### Backend
The heart of the software consists in the scripts written in Python, runned from the interface. These provide the data retrieval methods Spotify's API and the actual clusterization of the database.

![Software structure](https://i.imgur.com/JtsOI7Pl.png)


## Wanted functioning of the future 1.0 version
...




******************************************************************************************************************

## Funzionamento voluto per la versione 1.0 (in italiano)
All'avvio del programma, vi sarà una schermata di inizio in cui scegliere se cambiare **impostazioni** o se iniziare un **viaggio**.

### Impostazioni
Al selezionamento di "**Impostazioni**", sarà mostrata una schermata da cui:
-  Si potranno cambiare gli **assi** predefiniti per il viaggio scegliendo tra una lista di pacchetti di assi, oppure si potrà creare un nuovo pacchetto da eventualmente impostare come predefinito.
	> **Nota bene:** gli assi scelti non cambiano in alcun modo i parametri scelti per la clusterizzazione. Per cambiare questi ultimi bisogna cambiare il pacchetto dei pesi.
- Si potranno cambiare le impostazioni di clusterizzazione del dataset, ossia il **pacchetto dei pesi** (set dei pesi per ogni feature della clusterizzazione) e eventualmente lo **script di clusterizzazione**. 
- Vi sarà inoltre la possibilità di cambiare il **dataset** su cui si basa l'interfaccia.
Tutte le impostazioni sopra citate saranno attuate tramite il salvataggio dell'ID del pacchetto di assi, pacchetto di pesi o dataset; l'attributo ID sarà definito durante la creazione di un qualunque preset di quel tipo.
Per fare ciò serve fornire un nuovo dataset da clusterizzare attraverso l'inserimento di una lista di link a canzoni o playlist di Spotify. Alla creazione bisognerà selezionare il pacchetto di pesi da utilizzare e avviare la clusterizzazione. Finchè il nuovo dataset non sarà stato clusterizzato, non potrà essere utilizzato. I viaggi salvati che utilizzano questo dataset si riferiranno ad esso con il suo ID. La condivisione dei dataset avverrà attraverso la condivisione del modello già clusterizzato: se si volesse condividere il dataset non clusterizzato basterebbe passarsi il file di testo con i link e il pacchetto di pesi, dunque trovo inutile pensarlo in altro modo.

In particolare, per i **pacchetti dei pesi**, sarà possibile scegliere tra alcuni set già definiti, che avranno anche una loro precisa descrizione semantica riguardante che obbiettivo di raggruppamento ottiene. Anche in questo caso sarà possibile crearne di nuovi, salvarli, importarli o condividerli.

### Viaggi
Al selezionamento di "**Viaggi**" verrà esposta all'utente una lista di viaggi predefiniti, la possibilità di importare un viaggio che gli è stato condiviso e la possibilità di creare un viaggio nuovo.
Avere dei viaggi predefiniti permette all'utente di avviare il software e buttarsi dentro a un viaggio immediatamente senza dover inserire alcun input. 
> **Esempio:** *"Esplora la musica sarda dal Rock and Roll al Trip Hop"*

Ogni viaggio salvato sarà definito dai seguenti campi:
- Descrittivi:
	- Titolo.
	- Descrizione.
	- Immagine.
- Di impostazione:
	- Set di assi di movimento.
	- Set di pesi delle features.
	- Codice dataset da utilizzare.
	- Set di tracce radar
	- Filtri inseriti.
Saranno dunque semplici oggetti importabili e condivisibili tra utenti

#### Creazione di un viaggio
Alla crazione di un viaggio, l'utente dovrà inserire una playlist di Spotify. 

Subito dopo, gli verrà chiesto di selezionare una specifica *canzone di partenza* dalla lista: questa costituirà appunto la posizione di partenza all'interno dell'interfaccia. 
Tutte le canzoni della lista saranno sempre presenti nell'interfaccia all'interno di una mappa per eseguire la funzione di orientamento: indicheranno infatti il cluster a cui apparterrebbero tra quelli presenti nella scena.
Non più di 10 canzoni saranno accettate per la costituzione di tale funzione *"radar"*.

Sarà infine data l'opzione di filtrare le canzoni tramite vari parametri come ad esempio l'anno, la lingua o la città di provenienza.

Se il viaggio è nuovo, gli assi, il dataset e i pesi, attribuiti al viaggio saranno quelli predefiniti (cambiabili nelle impostazioni).
Prima di avviare l'interfaccia 3D, verrà mostrata una schermata di riassunto delle impostazioni del viaggio con:
- La lista delle canzoni che saranno presenti nella mappa.
- Il filtro.
- Gli assi scelti, con la possibilità di cambiarli da qui solo per questo viaggio.
- Il dataset scelto, anch'esso cambiabile come impostazione temporanea esclusivamente per questo viaggio.
- I pesi scelti per le features di clusterizzazione, cambiabili solo con pacchetti di pesi già processati. 
Nella stessa schermata vi sarà la possibilità di modificare il viaggio o di salvare e eventualmente condividere il viaggio.

#### Avvio di un viaggio già creato
Al selezionamento di un viaggio già creato, verrà avviata direttamente la schermata di riassunto del suddetto viaggio.

### Avvio
Un pulsante nella schermata di riassunto permetterà all'utente di catapultarsi nell'universo clusterizzato con la possibilità immediata di avere suggerimenti e di navigare verso altri generi musicali.
La mappa sarà un grosso aiutante in questo viaggio: segnerà i punti in cui son presenti le canzoni preventivamente scelte e indicherà i punti in cui son presenti i cluster e la canzone più rilevante del cluster. 
> **Nota bene:** se le canzoni scelte per lo *spawn* e per la mappa fossero state filtrate, queste non saranno presenti nell'interfaccia e nei cluster, **ma** verranno comunque usate per i loro scopi: il viaggio inizierà in ogni caso dalla canzone iniziale e la mappa segnerà comunque in che punto sarebbero quelle canzoni. 
Il motivo di ciò è che lo scopo di queste canzoni consiste esclusivamente nell'orientamento all'interno dell'universo, come dei punti cardinali: il loro scopo primario deve essere mantenuto anche se non saranno effettivamente presenti.

## I filtri
- Dati da MusicBrainz:
	- Filtro demografico per la città di nascita degli artisti: basato sul selezionamento di uno o più punti con un corrispettivo raggio all'interno di una cartina geografica. In futuro può essere migliorato tramite nuove modalità di selezione.
	- Lingua della canzone.
	> *Nonostante il database di MusicBrainz sia molto grande, non tutte le canzoni possiedono queste informazioni; per questo, se uno di questi filtri dovesse essere attivo, saranno filtrate fuori le canzoni che non forniscono un dato nel campo utile al filtro*.
- Presenti nei metadati di Spotify:
	- Intervallo di anni di uscita dell'album (non sempre accurato, dipende da che anno è segnalato da Spotify).
	- Artista.
- Altri tipi di filtri:
	- Lista di link a canzoni o playlist di Spotify: l'uso principale è da whitelist, ma si può usare anche in modalità blacklist. 
	Utilizzandolo come whitelist permetterebbe ad esempio di organizzare una grande playlist multigenere mantenendo la clusterizzazione del dataset generale originario (senza dover clusterizzare altri dataset).