# PORTAMENTO 
Portamento parte da una riscrittura del progetto "**SpotiWorld**" per la catalogazione di musica tramite analisi della traccia.
Il cuore del software è scritto in Python, l'interfaccia invece è scritta in C# e sfrutta l'editor Unity e il suo 3D Engine.

I database utilizzati per questo progetto sono:
1. **[Spotify](https://developer.spotify.com/documentation/web-api/reference/)**, da cui prelevo metadati delle canzoni, ma anche l'analisi musicale delle tracce.
2. **[MusicBrainz](https://musicbrainz.org/)**, da cui prelevo informazioni aggiuntive come la lingua della canzone o la città d'origine.

## Interfaccia
L'interfaccia è parte costituente della filosofia del software, che punta a evidenziare l'effettiva impossibilità di ridurre la musica a un numero discreto di cluster e le sfumature che derivano da qualunque catalogazione: al livello più basso di specializzazione infatti, ogni cluster è effettivamente una sola canzone. 

L'utente si può spostare in un mondo 3D in cui ogni punto è un cluster. Può inoltre entrare dentro a un cluster per scendere di livello di specializzazione, entrando dunque in un nuovo mondo di nuovi clusters. 
Il movimento è attuato su 3 assi definiti dall'utente tra tutti i parametri di dedscrizione della traccia.

## Funzionamento
All'avvio del programma, vi sarà una schermata di inizio in cui scegliere se cambiare **impostazioni** o se iniziare un **viaggio**.

### Impostazioni
Al selezionamento di "**Impostazioni**", sarà mostrata una schermata da cui:
-  Si potranno cambiare gli **assi** predefiniti per il viaggio scegliendo tra una lista di pacchetti di assi, oppure si potrà creare un nuovo pacchetto da eventualmente impostare come predefinito.
- Si potranno cambiare le impostazioni di clusterizzazione del database, ossia il **pacchetto dei pesi** (set dei pesi per ogni feature della clusterizzazione) e eventualmente lo **script di clusterizzazione**. 
- Vi sarà inoltre la possibilità di cambiare il **database** su cui si basa l'interfaccia: se non lo si ha già fatto, serve creare un nuovo database da clusterizzare fornendo una playlist o una lista di link a canzoni di Spotify. Alla creazione bisognerà selezionare il pacchetto di pesi e avviare la clusterizzazione prima di poter usare quel database nell'interfaccia. Sarà inoltre associato al database un codice alfanumerico a cui si riferiranno i viaggi salvati basati su questo database.

In particolare, per i **pacchetti dei pesi**, sarà possibile scegliere tra qualche pacchetto già processato che avrà anche una sua descrizione semantica riguardante che obbiettivo di raggruppamento ottiene, ma vi sarà anche la possibilità di crearne di nuovi, salvarli, importarli o condividerli.

### Viaggi
Al selezionamento di "**Viaggi**" verrà esposta all'utente una lista di viaggi predefiniti, la possibilità di importare un viaggio che gli è stato condiviso e la possibilità di creare un viaggio nuovo.

#### Creazione di un viaggio
Alla crazione di un viaggio, l'utente dovrà inserire una lista di link a canzoni su Spotify, oppure un unico link a una playlist. 

Subito dopo, gli verrà chiesto di selezionare una specifica *canzone di partenza* dalla lista: questa costituirà appunto la posizione di partenza all'interno dell'interfaccia. Le altre canzoni saranno invece indicate nell'interfaccia all'interno di una mappa o radar.

Sarà infine data l'opzione di filtrare le canzoni tramite vari parametri come ad esempio l'anno, la lingua o la città di provenienza.

Se il viaggio è nuovo, gli assi, il database e i pesi, attribuiti al viaggio saranno quelli predefiniti (cambiabili nelle impostazioni).
Prima di avviare l'interfaccia 3D, verrà mostrata una schermata di riassunto delle impostazioni del viaggio con la lista delle canzoni che saranno presenti nel radar, il filtro, gli assi scelti (con la possibilità di cambiarli da qui solo per questo viaggio), il database scelto (anch'esso cambiabile come impostazione temporanea esclusivamente per questo viaggio) e i pesi scelti per le features di clusterizzazione (cambiabili solo con pacchetti di pesi già processati). Nella stessa schermata vi sarà la possibilità di modificare il viaggio o di salvare e eventualmente condividere il viaggio.

#### Avvio di un viaggio già creato
Al selezionamento di un viaggio già creato, verrà avviata direttamente la schermata di riassunto del suddetto viaggio.

### Avvio
Un pulsante nella schermata di riassunto permetterà all'utente di catapultarsi nell'universo clusterizzato con la possibilità immediata di avere suggerimenti e di navigare verso altri generi musicali.
Aiutanti in questo viaggio saranno il radar e la mappa, basati sulle impostazioni del viaggio. 


## I filtri
- Dati da MusicBrainz 
> *Non tutte le canzoni possiedono queste informazioni; per questo, se uno di questi filtri dovesse essere attivo, saranno filtrate fuori le canzoni che non forniscono un dato nel campo utile al filtro*:
	- Filtro demografico per la città di nascita degli artisti: basato sul selezionamento di uno o più punti con un corrispettivo raggio all'interno di una cartina geografica. In futuro può essere migliorato tramite nuove modalità di selezione.
	- Lingua della canzone.
- Presenti nei metadati di Spotify:
	- Intervallo di anni di uscita dell'album (non sempre accurato, dipende da che anno è segnalato da Spotify).
	- Artista.
- Altri tipi di filtri:
	- Lista di link a canzoni di Spotify o link a una playlist di Spotify: può essere impostato come blacklist o come whitelist. Questo permetterebbe di organizzare una playlist mantenendo la clusterizzazione del database generale originario (senza dover clusterizzare altri database).