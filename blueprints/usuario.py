from datetime import date
from flask import Blueprint, redirect, render_template, abort, request, url_for, session
import requests
from jinja2 import TemplateNotFound

usuario = Blueprint('usuario', __name__, url_prefix='/usuario')


@usuario.route('/adicionar', methods=['GET', 'POST'])
def adicionar_usuario():
    if request.method == 'GET':
        return render_template('adicionar_usuario.html')
    else:
        usuario = {
            "login": request.form.get('login'),
            "senha": request.form.get('senha'),
            "funcao": request.form.get('funcao'),
            "nome": request.form.get('nome'),
            "grau_hierarquico": request.form.get('hierarquia')
        }
        
        response = requests.post('http://127.0.0.1:8000/usuario/create', json=usuario)
        
        
        if response.status_code == 200:
            usuario = response.json()
            
        
            info = {
                "curso": request.form.get('curso'),
                "pelotao": request.form.get('pelotao'),
                "numero": request.form.get('numero'),
                "nota_conduta": 10,
                "usuario": usuario['id']
            }
            
            response = requests.post('http://127.0.0.1:8000/info/create', json=info)
        
        return render_template('adicionar.html')
    

@usuario.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('usuario'):
            return redirect(url_for('usuario.cpis_aluno'))
        return render_template('login.html')
    else:
        data = {
            "login": request.form.get('login'),
            "senha": request.form.get('senha'),
        }
        
        response = requests.post('http://127.0.0.1:8000/usuario/login', json=data)

        if response.status_code == 200:
            usuario = response.json()
            session['usuario'] = usuario['id']
            
            return redirect(url_for('usuario.cpis_aluno'))
        
        return render_template('login.html')
    

@usuario.route('/logout', methods=['GET'])
def logout():
    del session['usuario']
    return redirect(url_for('login'))


@usuario.route('/cpis_aluno', methods=['GET'])
def cpis_aluno():
    if not session.get('usuario'):
        return redirect(url_for('usuario.login'))

    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_aluno?usuario_id={session["usuario"]}')
    
    protocolo = request.args.get('protocolo')
    if not protocolo:
        if response:
            cpis = response.json()
        else:
            cpis = []   
        
        return render_template('cpis_aluno.html', cpis=cpis)
    
    else:
        if response:
            cpis = response.json()
            for cpi in cpis:
                if cpi['id'] == int(protocolo):
                    return render_template('defesa.html', cpi=cpi)
                
            return render_template('cpis_aluno.html', cpis=cpis)
            
        else:
            cpis = []
            return render_template('cpis_aluno.html', cpis=cpis)


@usuario.route('/cpis_comunicante', methods=['GET'])
def cpis_comunicante():
    if not session.get('usuario'):
        return redirect(url_for('usuario.login'))

    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_comunicante?usuario_id={session["usuario"]}')
    
    protocolo = request.args.get('protocolo')
    if not protocolo:
        if response:
            cpis = response.json()
        else:
            cpis = []   
        
        return render_template('cpis_comunicante.html', cpis=cpis)
    
    else:
        if response:
            cpis = response.json()
            for cpi in cpis:
                if cpi['id'] == int(protocolo):
                    return render_template('comunicante.html', cpi=cpi)
                
            return render_template('cpis_comunicante.html', cpis=cpis)
            
        else:
            cpis = []
            return render_template('cpis_comunicante.html', cpi=cpi)


@usuario.route('/cpis_chefe_de_curso', methods=['GET'])
def cpis_chefe_de_curso():
    if not session.get('usuario'):
        return redirect(url_for('usuario.login'))

    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_chefe_de_curso?usuario_id={session["usuario"]}')
    
    protocolo = request.args.get('protocolo')
    if not protocolo:
        if response:
            cpis = response.json()
        else:
            cpis = []   
        
        return render_template('cpis_chefe_de_curso.html', cpis=cpis)
    
    else:
        if response:
            cpis = response.json()          
            for cpi in cpis:
                if cpi['id'] == int(protocolo):
                    params = {
                        'cpi_id': cpi['id']
                    }
                    
                    response = requests.get(f'http://127.0.0.1:8000/defesa/get_by_cpi', params=params)
                    if response:
                        defesa = response.json()
                        return render_template('parecer.html', cpi=cpi, defesa=defesa)
                    else:
                        return render_template('cpis_chefe_de_curso.html', cpis=cpis)   
                    
                
            return render_template('cpis_chefe_de_curso.html', cpis=cpis)
            
        else:
            cpis = []
            return render_template('cpis_chefe_de_curso.html', cpis=cpis)


@usuario.route('/cpis_comandante', methods=['GET'])
def cpis_comandante():
    if not session.get('usuario'):
        return redirect(url_for('usuario.login'))
    
    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_comandante?usuario_id={session["usuario"]}')
    
    protocolo: int = request.args.get('protocolo')
    if not protocolo:
        if response:
            cpis = response.json()
        else:
            cpis = []   
        
        return render_template('cpis_comandante.html', cpis=cpis)
    
    else:
        if response:
            cpis = response.json()
            for cpi in cpis:
                if cpi['id'] == protocolo:
                    return render_template('decisao.html', cpi=cpi)
                
            return render_template('decisao.html', cpis=cpis)
            
        else:
            cpis = []
            return render_template('decisao.html', cpi=cpi)
    

@usuario.route('/defesa', methods=['POST'])
def defesa():
    if not session.get('usuario'):
        return redirect(url_for('usuario.login'))
    
    ciente = request.form.get('ciente')
    ciente = True if ciente == 'True' else False
    justificativa = request.form.get('justificativa')
    id = request.args.get('protocolo')
    
    data_justificada = date.today().strftime('%d/%m/%Y')
    
    if ciente:
        json = {
            'id': int(id),
            'ciente': ciente,
            'data_justificada': data_justificada,
            'ass_aluno': True,
            'status': 4,
        }
    else:
        json = {
            'id': int(id),
            'ciente': ciente,
            'defesa': justificativa,
            'data_justificada': data_justificada,
            'ass_aluno': True,
            'status': 2,

        }
    
    response = requests.put(f'http://127.0.0.1:8000/defesa/update_defesa', json=json)
    return redirect(url_for('usuario.cpis_aluno'))


@usuario.route('/ciente_comunicante', methods=['POST'])
def ciente_comunicante():
    if not session.get('usuario'):
        return redirect(url_for('usuario.login'))
    
    ciente = request.form.get('ciente')
    ciente = True if ciente == 'True' else False
    justificativa = request.form.get('justificativa')
    id = request.args.get('protocolo')
        
    if ciente:
        json = {
            'id': id,
            'ass_comunicante': True,
            'status': 1
        }
    else:
        json = {
            'id': id,
            'justificativa': justificativa,
            'ass_comunicante': True,
            'status': 10,
        }
    
    response = requests.put(f'http://127.0.0.1:8000/cpi/update_cpi', json=json)
    return redirect(url_for('usuario.cpis_comunicante'))


@usuario.route('/parecer', methods=['POST'])
def parecer():
    if not session.get('usuario'):
        return redirect(url_for('usuario.login'))
    
    sugestao = request.form.get('sugestao')
    justificativa = request.form.get('justificativa')
    id = request.args.get('protocolo')
    
    data = date.today().strftime('%d/%m/%Y')
    
    json = {
        'id': int(id),
        'parecer': sugestao,
        'observacoes': justificativa,
        'data': data,
        'chefe_de_curso': int(session.get('usuario')),
        'ass_cefe_de_curso': True,
    }
    
    response = requests.put(f'http://127.0.0.1:8000/parecer/update_parecer', json=json)
    return redirect(url_for('usuario.cpis_chefe_de_curso'))
    

    
    
    
        
    