import requests
import subprocess
import base64
import json

# Variabili globali
base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key="
sGoogleApiKey = "AIzaSyChlPrxdzMFAbO9N33aOXDexlBdL6-MysA"
api_url = base_url + sGoogleApiKey

def ComponiJsonPerImmagine(sImagePath):
    subprocess.run(["rm", "./image.jpg"])
    subprocess.run(["rm", "./request.json"])
    subprocess.run(["cp", sImagePath, "./image.jpg"])
    subprocess.run(["bash", "./creajsonpersf.sh"])

def question_gemini(question, image=None):
    # Se è presente un'immagine, compila il JSON per l'immagine
    if image:
        file = base64.b64encode(image.read()).decode("utf-8")
        dJsonRequest: dict = {"contents": [{"parts": [{"text": question}, {"inline_data": {"mime_type": "image/jpeg", "data": file}}]}]}
        # Invia la richiesta all'API di Gemini
        response = requests.post(api_url, json=dJsonRequest, verify=False)

    else:
        # Se non c'è un'immagine, invia solo la domanda
        jsonDataRequest = {"contents": [{"parts": [{"text": question}]}]}
        response = requests.post(api_url, json=jsonDataRequest, verify=False)

    # Gestisci la risposta
    if response.status_code == 200:
        dResponse = response.json()
        dListaContenuti = dResponse['candidates'][0]
        return dListaContenuti['content']['parts'][0]['text']
    else:
        return "Errore: " + response.json().get("error", {}).get("message", "Errore sconosciuto")