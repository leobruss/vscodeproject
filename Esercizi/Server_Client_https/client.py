import requests
from requests.auth import HTTPBasicAuth
import urllib3


# Disabilita il warning per l'uso di HTTPS con certificati non verificati
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# URL base del server API
api_url_base = "https://127.0.0.1:8080"

# Funzione per inserire una nuova anagrafe (POST)
def post_anagrafe(auth):
    nome = input("Inserisci nome: ")
    cognome = input("Inserisci cognome: ")
    data_di_nascita = input("Inserisci la tua data di nascita (GG/MM/AAAA): ")
    cf = input("Inserisci il tuo codice fiscale: ")

    api_url = f"{api_url_base}/post_anagrafe"
    data = {
        "nome": nome,
        "cognome": cognome,
        "data_di_nascita": data_di_nascita,
        "cf": cf
    }

    # Richiesta HTTPS con disabilitazione verifica SSL per certificato autofirmato
    response = requests.post(api_url, json=data, auth=auth, verify=False)
    print(response.status_code)
    print(response.json())

# Funzione per ottenere tutte le anagrafe (GET)
def get_anagrafe(auth):
    api_url = f"{api_url_base}/get_anagrafe"
    response = requests.get(api_url, auth=auth, verify=False)
    
    print("Response Status Code:", response.status_code)  # Stampa il codice di stato
    print("Response Text:", response.text)  # Stampa il testo della risposta
    
    if response.status_code == 200:
        anagrafe = response.json()
        print("Anagrafe registrate:")
        for record in anagrafe:
            print(record)
    else:
        print("Errore durante il recupero dei dati. Status Code:", response.status_code)


# Funzione per aggiornare una anagrafe (PUT)
def put_anagrafe(auth):
    cf_to_update = input("Inserisci il cf dell'anagrafe da aggiornare: ")
    nome = input("Inserisci nuovo nome (lascia vuoto per non cambiare): ")
    cognome = input("Inserisci nuovo cognome (lascia vuoto per non cambiare): ")
    data_di_nascita = input("Inserisci nuova data di nascita (AAAA-MM-GG) (lascia vuoto per non cambiare): ")
    cf = input("Inserisci nuovo codice fiscale (lascia vuoto per non cambiare): ")

    api_url = f"{api_url_base}/put_anagrafe/{cf_to_update}"
    data = {}

    if nome:
        data["nome"] = nome
    if cognome:
        data["cognome"] = cognome
    if data_di_nascita:
        data["data_di_nascita"] = data_di_nascita
    if cf:
        data["cf"] = cf

    response = requests.put(api_url, json=data, auth=auth, verify=False)
    print(response.status_code)
    print(response.json())

# Funzione per cancellare una anagrafe (DELETE)
def delete_anagrafe(auth):
    cf_to_delete = input("Inserisci il cf dell'anagrafe da eliminare: ")
    api_url = f"{api_url_base}/delete_anagrafe/{cf_to_delete}"
    response = requests.delete(api_url, auth=auth, verify=False)
    print(response.status_code)
    print(response.json())

# Funzione per il menu delle operazioni
def menu():
    username = input("Inserisci username: ")
    password = input("Inserisci password: ")
    auth = HTTPBasicAuth(username, password)

    while True:
        print("\nMenu Operazioni Anagrafe:")
        print("1. Aggiungi una nuova anagrafe (POST)")
        print("2. Visualizza tutte le anagrafe (GET)")
        print("3. Aggiorna un'anagrafe esistente (PUT)")
        print("4. Elimina un'anagrafe (DELETE)")
        print("5. Esci")

        choice = input("Seleziona un'opzione (1-5): ")

        if choice == "1":
            post_anagrafe(auth)
        elif choice == "2":
            get_anagrafe(auth)
        elif choice == "3":
            put_anagrafe(auth)
        elif choice == "4":
            delete_anagrafe(auth)
        elif choice == "5":
            print("Uscita...")
            break
        else:
            print("Opzione non valida, riprova.")

# Avvia il menu
if __name__ == "__main__":
    menu()
