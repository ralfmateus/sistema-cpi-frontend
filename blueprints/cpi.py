from datetime import date
from flask import Blueprint, redirect, render_template, abort, request, url_for, session
import requests
from jinja2 import TemplateNotFound

from blueprints.artigo import ARTIGOS
# from blueprints.usuario import verificar_funcao

cpi = Blueprint('cpi', __name__, url_prefix='/cpi')


@cpi.route('/adicionar', methods=['GET', 'POST'])
def adicionar_cpi():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_id?id={usuario["id"]}', headers=headers)
    
    if not response:
        del session['usuario']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()
    
    
    response = requests.get('http://127.0.0.1:8000/usuario/get_all', headers=headers)
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
    
        response = requests.get('http://127.0.0.1:8000/info/get_by_numero_curso_ano', params=params, headers=headers)
        
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
                
        response = requests.post('http://127.0.0.1:8000/cpi/create', json=cpi, headers=headers)
        
        
        if request.form.get('submit') == 'novo':
            return redirect(url_for('cpi.adicionar_cpi'))
        return redirect(url_for('usuario.home'))


@cpi.route('/perfil_cpi', methods=['GET'])
def perfil_cpi():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    
    protocolo = request.args.get('protocolo', type=int)
    if not protocolo:
        return redirect(url_for('consulta.consultar'))
    
    response = requests.get(f'http://127.0.0.1:8000/cpi/get_by_cpi_id?id={protocolo}', headers=headers)
    
    if not response:
        return redirect(url_for('consulta.consultar', erro=1))
    else:
        cpi = response.json()
        
        response = requests.get(f'http://127.0.0.1:8000/defesa/get_by_cpi', params={'cpi_id': cpi['id']}, headers=headers)
        if response:
            defesa = response.json()
        else:
            defesa = None
                                
        response = requests.get(f'http://127.0.0.1:8000/parecer_cmd_cia/get_by_cpi', params={'cpi_id': cpi['id']}, headers=headers)
        if response:
            parecer_cmd_cia = response.json()
        else:
            parecer_cmd_cia = None
                                
        response = requests.get(f'http://127.0.0.1:8000/parecer/get_by_cpi', params={'cpi_id': cpi['id']}, headers=headers)
        if response:
            parecer = response.json()
        else:
            parecer = None
        
                        
        response = requests.get(f'http://127.0.0.1:8000/decisao/get_by_cpi', params={'cpi_id': cpi['id']}, headers=headers)
        if response:
            decisao = response.json()
        else:
            decisao = None
                        
        return render_template('cpi.html', cpi=cpi, defesa=defesa, parecer=parecer, parecer_cmd_cia=parecer_cmd_cia, decisao=decisao)
    
    
@cpi.route('/gerar_caderno', methods=['GET', 'POST'])
def gerar_caderno():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    if request.method == 'GET':
        return render_template('gerar_caderno.html', cadernos=None, usuario=usuario)
    
    temp = request.form.get('data_inicial')
    temp = temp.split('-')
    data_inicial = f'{temp[2]}/{temp[1]}/{temp[0]}'
    
    temp = request.form.get('data_final')  
    temp = temp.split('-')
    data_final = f'{temp[2]}/{temp[1]}/{temp[0]}'
      
    pelotoes = request.form.get('pelotoes', type=int)  
    
    response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_data?data_inicial={data_inicial}&data_final={data_final}', headers=headers)
    
    if not response:
        return redirect(url_for('cpi.gerar_caderno', erro=1))
        
    cadernos = response.json()
    
    return render_template('gerar_caderno.html', cadernos=cadernos, usuario=usuario, pelotoes=pelotoes)