from flask import Flask, redirect, url_for
from blueprints import consulta, usuario, cpi
from blueprints.usuario import home



app = Flask(__name__)



URL_BASE = 'http://127.0.0.1:8000/'
SECRET = 'secret'

app.secret_key = SECRET


app.register_blueprint(usuario.usuario)
app.register_blueprint(cpi.cpi)
app.register_blueprint(consulta.consulta)

@app.route('/')
def index():
    return redirect(url_for('usuario.login'))

@app.errorhandler(404)
def erro_not_found(error):
    return redirect(url_for('usuario.login'))