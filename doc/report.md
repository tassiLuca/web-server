<div style="text-align: center">
    <h1>Web Server</h1>
    <h2>Relazione di progetto di 'Programmazione di reti'</h2>
    <p>Tassinari Luca &bull; Matr. 921373</p>
</div>

## Analisi dei requisiti
Si vuole realizzare un _web server_ per un'agenzia di viaggi. 
Di seguito sono elencati per punti i requisiti del sistema.
- il _web server_ deve consentire l'accesso a più utenti in contemporanea;
- la _home page_ del sito deve permettere la visualizzazione della lista di servizi erogati dall'agenzia viaggi (con relativo _link_ ad una pagina dedicata);
- devono esserci la possibilità di inserire _link_ per il _download_ di documenti pdf;
- si richiede la possibilità di autenticare gli utenti;
- l'interruzione da tastiera dell'esecuzione del _web server_ deve essere opportunamente gestita in modo da liberare la risorsa _socket_.

## Design 
L'architettura del sistema è molto semplice ed è presenta qui di seguito.

![Architettura del sistema](./out/arch.svg)

- `WebServerAgent` è il componente attivo che si occupa dell'istanziazione e configurazione del server web. 
- `AppRequestHandler` è la classe che si occupa della gestione delle richieste HTTP che arrivano al server web dai vari _client_. Si noti che questa classe estende [`BaseHTTPRequestHandler`](https://docs.python.org/3/library/http.server.html#http.server.BaseHTTPRequestHandler), definita all'interno del modulo `http.server`, implementando la logica delle risposte all'interno dei due metodi `do_GET()` e `do_POST()`. 
- `LoginAuthenticator`: classe che si occupa dell'autenticazione all'area riservata del sito web.

### Design dettagliato
Per permettere al server di gestire più client in contemporanea è necessario fare uso di più _thread_, uno per ciascun _client_ che si connette: in particolare, per ogni _client_ che si connette al _web server_, il _server_ crea un nuovo _thread_ il cui compito è quello di rispondere al _client_; una volta esaurito il suo compito, termina. 

![Threads](out/threads.svg)