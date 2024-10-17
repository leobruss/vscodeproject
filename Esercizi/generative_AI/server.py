from flask import Flask, render_template, request

api = Flask("__name__")

@api.route('/', methods = ['GET'])
def index():
    return render_template("sendfile.html")

@api.route('/mansendfile', methods = ['POST'])
def index():
    return render_template("sendfile.html")
    
api.run(host = "127.0.0.1", port = 8085, ssl_context="adhoc")
