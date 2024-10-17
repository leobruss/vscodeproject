from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth

# Lista in cui memorizzare i dati dell'anagrafe
anagrafe = []

# Creazione dell'istanza dell'app Flask e dell'autenticazione
api = Flask(__name__)
auth = HTTPBasicAuth()

# Dati di esempio per l'autenticazione
users = {
    "lettura": {"password": "password_lettura", "role": "r"},
    "scrittura": {"password": "password_scrittura", "role": "w"},
}


def verify_password(username, password):
    if username in users and users[username]['password'] == password:
        return username  # Ritorna l'username se l'autenticazione ha successo
    return None

def get_user_role(username):
    return users[username]["role"]

# Metodo POST per inserire una nuova anagrafe
@api.route('/post_anagrafe', methods=['POST'])
def post_anagrafe():
    username = auth.current_user()
    if get_user_role(username) != "w":
        return jsonify({"Errore": "Non hai permessi per scrivere dati"}), 403  # Forbidden
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json_data = request.json
        anagrafe.append(json_data)  # Aggiunge il dato alla lista
        response = {"Esito": "ok", "Msg": "Dato inserito"}
        return jsonify(response), 201  # Created
    else:
        return 'Content-Type not supported!', 400

# Metodo GET per ottenere tutti i dati dell'anagrafe
@api.route('/get_anagrafe', methods=['GET'])
def get_anagrafe():
    username = auth.current_user()
    if get_user_role(username) == "r" or get_user_role(username) == "w":
        return jsonify({"Errore": "Non hai permessi per leggere dati"}), 403  # Forbidden
    try:
        return jsonify(anagrafe), 200  # Status code 200 (OK)
    except Exception as e:
        return jsonify({"Esito": "errore", "Msg": str(e)}), 500  # Status code 500 (Internal Server Error)

# Metodo PUT per aggiornare un record nell'anagrafe (per esempio in base all'cf)
@api.route('/put_anagrafe/<cf>', methods=['PUT'])
def update_anagrafe(cf):
    username = auth.current_user()
    if get_user_role(username) != "w":
        return jsonify({"Errore": "Non hai permessi per modificare dati"}), 403  # Forbidden
    
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json_data = request.json
        for record in anagrafe:
            if record.get("cf") == cf:
                record.update(json_data)
                response = {"Esito": "ok", "Msg": "Dato aggiornato"}
                return jsonify(response), 200  # Status code 200 (OK)
        return jsonify({"Esito": "errore", "Msg": "cf non trovato"}), 404  # Status code 404 (Not Found)
    else:
        return 'Content-Type not supported!', 400

# Metodo DELETE per cancellare un record dall'anagrafe (per esempio in base all'cf)
@api.route('/delete_anagrafe/<cf>', methods=['DELETE'])
def delete_anagrafe(cf):
    username = auth.current_user()
    if get_user_role(username) != "w":
        return jsonify({"Errore": "Non hai permessi per eliminare dati"}), 403  # Forbidden
    for record in anagrafe:
        if record.get("cf") == cf:
            anagrafe.remove(record)
            response = {"Esito": "ok", "Msg": "Dato eliminato"}
            return jsonify(response), 200
    return jsonify({"Esito": "errore", "Msg": "cf non trovato"}), 404

if __name__ == "__main__":
    api.run(host="127.0.0.1", port=8080, ssl_context='adhoc')
