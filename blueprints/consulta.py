from datetime import date
from flask import Blueprint, redirect, render_template, abort, request, url_for, session
import requests
from jinja2 import TemplateNotFound

from blueprints.artigo import ARTIGOS

consulta = Blueprint('consulta', __name__, url_prefix='/consulta')


@consulta.route('/')
def index():
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_id?id={session["usuario"]}')
    
    if not response:
        del session['usuario']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()
    
    return render_template('consulta.html', usuario=usuario)

@consulta.route('/consultar', methods=['POST'])
def consultar():
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_id?id={session["usuario"]}')
    
    if not response:
        del session['usuario']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()
    
    return render_template('consulta.html', usuario=usuario)