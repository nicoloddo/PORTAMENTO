# PORTAMENTO 
Portamento parte da una riscrittura del progetto "**SpotiWorld**" per la catalogazione di musica tramite analisi della traccia.
Il cuore del software è scritto in Python, l'interfaccia invece è scritta in C# e sfrutta l'editor Unity e il suo 3D Engine.

## Interfaccia
L'interfaccia è parte costituente della filosofia del software, che punta a evidenziare l'effettiva impossibilità di ridurre la musica a un numero discreto di cluster e le sfumature che derivano da qualunque catalogazione: al livello più basso di specializzazione infatti, ogni cluster è effettivamente una sola canzone. 

L'utente si può spostare in un mondo 3D in cui ogni punto è un cluster. Può inoltre entrare dentro a un cluster per scendere di livello di specializzazione, entrando dunque in un nuovo mondo di nuovi clusters. 
Il movimento è attuato su 3 assi definiti dall'utente tra tutti i parametri di dedscrizione della traccia.

## Funzionamento
All'avvio del programma, verrà richiesto all'utente di inserire una lista di link a canzoni su Spotify oppure un unico link a una playlist. 
Subito dopo, gli verrà chiesto di selezionare una specifica canzone di partenza dalla lista: questa costituirà la posizione di partenza all'interno dell'interfaccia. Le altre canzoni saranno invece indicate nell'interfaccia all'interno di una mappa o radar.
Sarà in seguito data l'opzione di filtrare le canzoni tramite vari parametri come ad esempio l'anno, la lingua o la città di provenienza.

Appena completati questi primi semplici step, l'utente verrà subito teletrasportato all'interno dell'universo 3D con la possibilità immediata di avere suggerimenti e di navigare verso altri generi musicali.
