from flask import Flask, render_template, request

utenti = [["l.brussani@gmail.com","BRSLRD04L24H501N","leonardo04"],
          ["mariorossi@gmail.com","ROELAM03L25H501N","Rossi03"],
          ["asiadelbuono@gmail.com","ASIDBN97A19H501N","Asietta97"]]

api = Flask("__name__")

@api.route('/', methods = ['GET'])
def index():
    return render_template("index.html")

@api.route('/registration', methods =['POST'])
def registration():
    email = request.form["email"]
    cf = request.form["cf"]
    password = request.form["psw"]

    input_user = [email, cf, password]

    if input_user in utenti:
        return render_template("reg_ok.html")
    else:
        return render_template("reg_ko.html")
    
api.run(host = "0.0.0.0", port = 8085)
