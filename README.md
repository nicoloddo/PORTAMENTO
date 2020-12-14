# PORTAMENTO 
Portamento parte da una riscrittura del progetto "**SpotiWorld**" per la catalogazione di musica tramite analisi della traccia.
Il cuore del software è scritto in Python, l'interfaccia invece è scritta in C# e sfrutta l'editor Unity e il suo 3D Engine.

I database utilizzati per questo progetto sono:
1. **[Spotify](https://developer.spotify.com/documentation/web-api/reference/)**, da cui prelevo metadati delle canzoni, ma anche l'analisi musicale delle tracce.
2. **[MusicBrainz](https://musicbrainz.org/)**, da cui prelevo informazioni aggiuntive come la lingua della canzone o la città d'origine.

### Cenni riguardanti l'interfaccia
L'interfaccia è parte costituente della filosofia del software, che punta a evidenziare l'effettiva impossibilità di ridurre la musica a un numero discreto di cluster e le sfumature che derivano da qualunque tipo di catalogazione musicale: nessun cluster ha una definizione oggettiva, ma gli si può dare un nome soggettivo; inoltre, al livello più basso di specializzazione, ogni cluster è effettivamente una sola canzone, a immagine del fatto che in realtà, alla base, ogni canzone definisce un suo genere unico. 

L'utente si può spostare in un mondo 3D in cui ogni punto è un cluster. Può inoltre entrare dentro a un cluster per scendere di livello di specializzazione, entrando dunque in un nuovo mondo di nuovi clusters. 
Il movimento è attuato su 3 assi definiti dall'utente tra tutti i parametri di descrizione della traccia.

## Funzionamento
All'avvio del programma, vi sarà una schermata di inizio in cui scegliere se cambiare **impostazioni** o se iniziare un **viaggio**.

### Impostazioni
Al selezionamento di "**Impostazioni**", sarà mostrata una schermata da cui:
-  Si potranno cambiare gli **assi** predefiniti per il viaggio scegliendo tra una lista di pacchetti di assi, oppure si potrà creare un nuovo pacchetto da eventualmente impostare come predefinito.
	> Nota bene: gli assi scelti non cambiano in alcun modo i parametri scelti per la clusterizzazione. Per cambiare questi ultimi bisogna cambiare il pacchetto dei pesi.
- Si potranno cambiare le impostazioni di clusterizzazione del database, ossia il **pacchetto dei pesi** (set dei pesi per ogni feature della clusterizzazione) e eventualmente lo **script di clusterizzazione**. 
- Vi sarà inoltre la possibilità di cambiare il **database** su cui si basa l'interfaccia.
Per fare ciò serve fornire un nuovo database da clusterizzare attraverso l'inserimento di una lista di link a canzoni o playlist di Spotify. Alla creazione bisognerà selezionare il pacchetto di pesi da utilizzare e avviare la clusterizzazione. Finchè il nuovo database non sarà stato clusterizzato, non potrà essere utilizzato. Sarà inoltre associato al database un codice alfanumerico a cui si riferiranno i viaggi salvati che utilizzano questo database.

In particolare, per i **pacchetti dei pesi**, sarà possibile scegliere tra alcuni set già definiti, che avranno anche una loro precisa descrizione semantica riguardante che obbiettivo di raggruppamento ottiene. Anche in questo caso sarà possibile crearne di nuovi, salvarli, importarli o condividerli.

### Viaggi
Al selezionamento di "**Viaggi**" verrà esposta all'utente una lista di viaggi predefiniti, la possibilità di importare un viaggio che gli è stato condiviso e la possibilità di creare un viaggio nuovo.
Avere dei viaggi predefiniti permette all'utente di avviare il software e buttarsi dentro a un viaggio immediatamente senza dover inserire alcun input. 
> Esempio: **"Esplora la musica sarda dal Rock and Roll al Trip Hop"**

Ogni viaggio salvato sarà definito dai seguenti campi:
- Descrittivi:
	- Titolo.
	- Descrizione.
	- Immagine.
- Di impostazione:
	- Set di assi di movimento.
	- Set di pesi delle features.
	- Codice database da utilizzare.
	- Filtri inseriti.
Saranno dunque semplici oggetti importabili e condivisibili tra utenti

#### Creazione di un viaggio
Alla crazione di un viaggio, l'utente dovrà inserire una lista di link a canzoni o playlist di Spotify. 

Subito dopo, gli verrà chiesto di selezionare una specifica *canzone di partenza* dalla lista: questa costituirà appunto la posizione di partenza all'interno dell'interfaccia. Le altre canzoni saranno invece indicate nell'interfaccia all'interno di una mappa o radar.

Sarà infine data l'opzione di filtrare le canzoni tramite vari parametri come ad esempio l'anno, la lingua o la città di provenienza.

Se il viaggio è nuovo, gli assi, il database e i pesi, attribuiti al viaggio saranno quelli predefiniti (cambiabili nelle impostazioni).
Prima di avviare l'interfaccia 3D, verrà mostrata una schermata di riassunto delle impostazioni del viaggio con la lista delle canzoni che saranno presenti nel radar, il filtro, gli assi scelti (con la possibilità di cambiarli da qui solo per questo viaggio), il database scelto (anch'esso cambiabile come impostazione temporanea esclusivamente per questo viaggio) e i pesi scelti per le features di clusterizzazione (cambiabili solo con pacchetti di pesi già processati). Nella stessa schermata vi sarà la possibilità di modificare il viaggio o di salvare e eventualmente condividere il viaggio.

#### Avvio di un viaggio già creato
Al selezionamento di un viaggio già creato, verrà avviata direttamente la schermata di riassunto del suddetto viaggio.

### Avvio
Un pulsante nella schermata di riassunto permetterà all'utente di catapultarsi nell'universo clusterizzato con la possibilità immediata di avere suggerimenti e di navigare verso altri generi musicali.
Aiutanti in questo viaggio saranno il radar e la mappa, basati sulle impostazioni del viaggio: segneranno i punti in cui son presenti le canzoni preventivamente scelte, ma indicheranno anche i punti in cui son presenti i cluster e la canzone più rilevante del cluster. 
> Nota bene: se le canzoni scelte per lo *spawn* e per il radar/mappa fossero state filtrate, queste non saranno presenti nell'interfaccia e nei cluster, **ma** verranno comunque usate per i loro scopi: il viaggio inizierà in ogni caso dalla canzone iniziale e la mappa segnerà comunque in che punto sarebbero quelle canzoni. 
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
	Utilizzandolo come whitelist permetterebbe ad esempio di organizzare una grande playlist multigenere mantenendo la clusterizzazione del database generale originario (senza dover clusterizzare altri database).