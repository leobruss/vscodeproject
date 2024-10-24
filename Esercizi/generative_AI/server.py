from flask import Flask, render_template, request
from utility_gemini import question_gemini
import os

api = Flask(__name__)

@api.route('/', methods=['GET'])
def index():
    return render_template('sendfile.html')

@api.route('/mansendfile', methods=['POST'])
def mansendfile():
    # Recupera la domanda inviata tramite il form
    question = request.form.get('question')
    
    # Verifica se è presente un file immagine
    image = request.files.get("image")

    if not image:
        risposta = question_gemini(question)
        return render_template("sendfile.html", answer=risposta)

    # Put here some other checks (security, file length etc...)S
    else:

        file = request.files.get("image")
        risposta = question_gemini(question, image=file,)
        question = ""
        image = ""
        return render_template("sendfile.html", answer=risposta)
    



api.run(host="0.0.0.0",port=8085)
