from datetime import date
from flask import Blueprint, redirect, render_template, abort, request, url_for, session
import requests
from jinja2 import TemplateNotFound

from blueprints.artigo import ARTIGOS

cpi = Blueprint('cpi', __name__, url_prefix='/cpi')


@cpi.route('/adicionar', methods=['GET', 'POST'])
def adicionar_cpi():
    response = requests.get('http://127.0.0.1:8000/usuario/get_all')
    comunicantes = response.json()
    
    if request.method == 'GET':
        data = date.today()
        
        return render_template('adicionar_cpi.html', artigos=ARTIGOS, comunicantes=comunicantes, data=data)
    else:
        comunicante = int(request.form.get('comunicante'))
        temp = request.form.get('data')
        temp = temp.split('-')
        data = f'{temp[2]}/{temp[1]}/{temp[0]}'
        numero = int(request.form.get('numero'))
        
        curso = request.form.get('curso')
        
        params = {
            'numero': numero,
            'curso': curso
        }
    
        response = requests.get('http://127.0.0.1:8000/info/get_by_numero_curso', params=params)
        
        info = response.json()
        
        
        cpi = {
            "aluno": info[0]['usuario']['id'],
            "conduta": request.form.get('conduta'),
            "data": data,
            "hora": request.form.get('hora'),
            "local": request.form.get('local'),
            "artigo": request.form.get('artigo'),
            "testemunhas": request.form.get('testemunhas'),
            "comunicante": comunicante,
            "observacoes": request.form.get('observacoes'),
        }
                
        response = requests.post('http://127.0.0.1:8000/cpi/create', json=cpi)
        
        return render_template('adicionar_cpi.html', comunicantes=comunicantes, artigos=ARTIGOS)