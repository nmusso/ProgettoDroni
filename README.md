# ProgettoDroni

## Guida Utente
È **raccomandato** l’utilizzo di _Spyder_ per un’esecuzione ottimale.

Come prima cosa è necessario avviare il _Gateway_
Se non si usa Spyder, da terminale:  
  ```python3  gateway.py```   

In seguito si possono avviare in qualsiasi ordine:

* _Client_ con:
  * Se non si usa Spyder, da terminale:  
    ```python3  client.py```
  
* _DroneX_ (sostituire X con 1, 2, 3) con: 
  * Se non si usa Spyder, da terminale:  
   ```python3  droneX.py```

I comandi utili per testare il tutto sono quelli lanciabili dalla console del Client e sono fruibili con il comando _**/help**_ direttamente da essa.

## Esempi 
Utilizzo funzioni principali da console del Client:

Richiesta droni disponibili
```
Insert command: /drones 
D1 (192.168.1.101) Available
D2 (192.168.1.102) Not available
```

Richiesta di spedizione da parte di un drone ad un certo indirizzo
```
Insert command: /ship 192.168.1.101 Via delle Forche 12
``` 
oppure 
```
Insert command: /ship D1 Via delle Forche 12
```


