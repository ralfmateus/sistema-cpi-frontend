from datetime import date
from flask import Blueprint, redirect, render_template, abort, request, url_for, session
import requests
from jinja2 import TemplateNotFound

from blueprints.artigo import ARTIGOS
# from blueprints.usuario import verificar_funcao

cpi = Blueprint('cpi', __name__, url_prefix='/cpi')


@cpi.route('/adicionar', methods=['GET', 'POST'])
def adicionar_cpi():
    # if not verificar_funcao('JUSTICA') and not verificar_funcao('COMANDANTE DA ESFAP') and not verificar_funcao('COMANDANTE DA ESFO'):
    #     return redirect(url_for('usuario.home'))
    # if not verificar_funcao('-'):
    #     return redirect(url_for('usuario.home'))
    
    # response = requests.get(f'http://127.0.0.1:8000/info/get_by_usuario?id={session["usuario"]}')
    # if not response:
    #     return redirect(url_for('usuario.home', erro=1))
    
    # info = response.json()
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_id?id={session["usuario"]}')
    
    if not response:
        del session['usuario']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()
    
    
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
        ano = request.form.get('ano')
        
        params = {
            'numero': numero,
            'curso': curso,
            'ano': ano,
        }
    
        response = requests.get('http://127.0.0.1:8000/info/get_by_numero_curso_ano', params=params)
        
        info = response.json()
        
        
        cpi = {
            "aluno": info[0]['usuario']['id'],
            "conduta": request.form.get('conduta'),
            "data": data,
            "hora": request.form.get('hora'),
            "local": request.form.get('local'),
            "artigo": request.form.get('enquadramento'),
            "testemunhas": request.form.get('testemunha'),
            "comunicante": comunicante,
            "observacoes": request.form.get('observacoes'),
        }
                
        response = requests.post('http://127.0.0.1:8000/cpi/create', json=cpi)
        
        
        if request.form.get('submit') == 'novo':
            return redirect(url_for('cpi.adicionar_cpi'))
        return redirect(url_for('usuario.home'))
