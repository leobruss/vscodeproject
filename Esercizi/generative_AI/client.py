import requests, json, sys
import subprocess
from myjson import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key="

sGoogleApiKey: str = "AIzaSyChlPrxdzMFAbO9N33aOXDexlBdL6-MysA"


def ComponiJsonPerImmagine(sImagePath):
  subprocess.run(["rm", "./image.jpg"])
  subprocess.run(["rm", "./request.json"])
  subprocess.run(["cp", sImagePath,"./image.jpg"])
  subprocess.run(["bash", "./creajsonpersf.sh"])

print("Benvenuti nella mia Generativa")
api_url = base_url + sGoogleApiKey

iFlag = 0
while iFlag == 0:
    print("\nOperazioni disponibili:")
    print("1. Crea una favola")
    print("2. Rispondi ad una domanda")
    print("3. Rispondere ad una domanda su un file img")
    print("4. Esci")


    try:
        iOper = int(input("Cosa vuoi fare? "))
    except ValueError:
        print("Inserisci un numero valido!")
        continue


    if iOper == 1:
        sArgomento = input("Inserisci l'argomento della favola: ")
        sArgomento2 ="Crea una storia su" + sArgomento + "in lingua italiana"
        
        jsonDataRequest = {"contents": [{"parts": [{"text": sArgomento2}]}]}
        #j sonDataRequest ["contents"] [0] ["'parts"] [0] ["text"]=sArgomento
        #EseguiOperazione(1, api_url, jsonDataRequest)
        response = requests.post(api_url, json = jsonDataRequest, verify = False)

        if response.status_code == 200:
            dResponse = response.json()
            dListaContenuti = dResponse['candidates'][0]
            sTestoprimaRisposta = dListaContenuti ['content']['parts'][0]['text']
            print(sTestoprimaRisposta)
        else:
            print("\nerror: " + response.json()["error"]["message"])

    elif iOper == 2:
        sArgomento = input(" Rispondi ad una domanda: ")
        
        jsonDataRequest = {"contents": [{"parts": [{"text": sArgomento}]}]}
        response = requests.post(api_url, json = jsonDataRequest, verify = False)

        if response.status_code == 200:
            print(response.json())
        else:
            print("\nerror: " + response.json()["error"]["message"])
   
   
    elif iOper == 3:
        sFile = input("Inserisci il path completo del file che vuoi analizzare: ")
        sDomanda = input("Inserisci la domanda: ")

        ComponiJsonPerImmagine(sFile)
        dJsonRequest = JsonDeserialize("request.json")
        response = requests.post(api_url, json=dJsonRequest, verify=False)
        if response.status_code == 200:
            dResponse = response.json()
            dJsonRequest ["contents"] [0] ["parts"] [0]["text"]=sDomanda
            dListaContenuti = dResponse['candidates'][0]
            sTestoprimaRisposta = dListaContenuti ['content']['parts'][0]['text']
            print(sTestoprimaRisposta)
        else:
            print("\nerror: " + response.json()["error"]["message"])


    elif iOper == 4:
        print("Buona giornata!")
        iFlag = 1

    else:
        print("Operazione non disponibile, riprova.")