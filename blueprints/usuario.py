from datetime import date
from flask import Blueprint, redirect, render_template, abort, request, url_for, session
import requests
from jinja2 import TemplateNotFound

from blueprints.artigo import ARTIGOS

usuario = Blueprint('usuario', __name__, url_prefix='/usuario')


@usuario.route('/adicionar', methods=['GET', 'POST'])
def adicionar_usuario():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    if request.method == 'GET':
        return render_template('adicionar_usuario.html')
    else:
        usuario = {
            "login": request.form.get('login'),
            "senha": request.form.get('senha'),
            "funcao": request.form.get('funcao'),
            "nome": request.form.get('nome'),
            "nome_de_guerra": request.form.get('nome_de_guerra'),
            "grau_hierarquico": request.form.get('grau_hierarquico')
        }
        
        response = requests.post('http://127.0.0.1:8000/usuario/create', json=usuario, headers=headers)
        
        
        if response.status_code == 200:
            usuario = response.json()
            
            if usuario['funcao'] == 'ALUNO' or usuario['funcao'] == 'JUSTICA':
                info = {
                    "curso": request.form.get('curso'),
                    "ano": request.form.get('ano'),
                    "cia": request.form.get('cia'),
                    "pelotao": request.form.get('pelotao'),
                    "numero": request.form.get('numero'),
                    "nota_conduta": 10,
                    "usuario": usuario['id']
                }
                response = requests.post('http://127.0.0.1:8000/info/create', json=info, headers=headers)
                
            elif usuario['funcao'] ==  'CHEFE DE CURSO':
                info = {
                    "curso": request.form.get('curso'),
                    "ano": request.form.get('ano'),
                    "pelotao": request.form.get('pelotao'),
                    "numero": request.form.get('numero'),
                    "usuario": usuario['id']
                }
                
                response = requests.post('http://127.0.0.1:8000/info/create', json=info, headers=headers)
                
            elif usuario['funcao'] == 'COMANDANTE DE CIA':
                info = {
                    "curso": request.form.get('curso'),
                    "ano": request.form.get('ano'),
                    "cia": request.form.get('cia'),
                    "pelotao": request.form.get('pelotao'),
                    "usuario": usuario['id']
                }
            
                response = requests.post('http://127.0.0.1:8000/info/create', json=info, headers=headers)
            
            return redirect(url_for('usuario.adicionar_usuario'))
        
        return redirect(url_for('usuario.adicionar_usuario', erro=1))


@usuario.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('usuario'):
            return redirect(url_for('usuario.home'))
        return render_template('login.html')
    else:
        data = {
            "username": request.form.get('login'),
            "password": request.form.get('senha'),
        }
        
        response = requests.post('http://127.0.0.1:8000/usuario/token', data=data)

        if response.status_code == 200:
            token = response.json()['access_token']
            session['token'] = token
            
            return redirect(url_for('usuario.home'))
        
        return redirect(url_for('usuario.login'))
    

@usuario.route('/home')
def home():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    if usuario['funcao'] == 'ALUNO':
        return redirect(url_for('usuario.cpis_aluno'))
    elif usuario['funcao'] == 'CHEFE DE CURSO':
        return redirect(url_for('usuario.cpis_chefe_de_curso'))
    elif usuario['funcao'] == 'COMANDANTE DE CIA':
        return redirect(url_for('usuario.cpis_cmd_cia'))
    elif usuario['funcao'] == 'COMANDANTE DA ESFAP':
        return redirect(url_for('usuario.cpis_comandante'))
    elif usuario['funcao'] == 'COMANDANTE DA ESFO':
        return redirect(url_for('usuario.cpis_comandante'))
    elif usuario['funcao'] == 'COMUNICANTE':
        return redirect(url_for('usuario.cpis_comunicante'))
    elif usuario['funcao'] == 'JUSTICA':
        return redirect(url_for('usuario.cpis_aluno'))
    
    

@usuario.route('/logout', methods=['GET'])
def logout():
    del session['token']
    return redirect(url_for('usuario.login'))


@usuario.route('/cpis_aluno', methods=['GET'])
def cpis_aluno():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    response = requests.get(f'http://127.0.0.1:8000/info/get_by_usuario?id={usuario["id"]}', headers=headers)
    if not response:
        return redirect(url_for('usuario.home', erro=1))
    
    info = response.json()
    

    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_aluno?usuario_id={usuario["id"]}', headers=headers)
    
    protocolo = request.args.get('protocolo')
    if not protocolo:
        if response:
            cpis = response.json()
        else:
            cpis = []   
        
        return render_template('home_aluno.html', cpis=cpis, usuario=usuario, info=info)
    
    else:
        if response:
            cpis = response.json()
            for cpi in cpis:
                if cpi['id'] == int(protocolo):
                    return render_template('defesa.html', cpi=cpi)
                
            return render_template('home_aluno.html', cpis=cpis, usuario=usuario, info=info)
            
        else:
            cpis = []
            return render_template('home_aluno.html', cpis=cpis, usuario=usuario, info=info)


@usuario.route('/cpis_comunicante', methods=['GET'])
def cpis_comunicante():    
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']

    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_comunicante?usuario_id={usuario["id"]}', headers=headers)
    
    protocolo = request.args.get('protocolo')
    if not protocolo:
        if response:
            cpis = response.json()
        else:
            cpis = []   
        
        return render_template('cpis_comunicante.html', cpis=cpis, usuario=usuario)
    
    else:
        if response:
            cpis = response.json()
            for cpi in cpis:
                if cpi['id'] == int(protocolo):
                    return render_template('comunicante.html', cpi=cpi)
                
            return render_template('cpis_comunicante.html', cpis=cpis, usuario=usuario)
            
        else:
            cpis = []
            return render_template('cpis_comunicante.html', cpi=cpi, usuario=usuario)


@usuario.route('/cpis_chefe_de_curso', methods=['GET'])
def cpis_chefe_de_curso():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    usuario = response.json()

    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_chefe_de_curso?usuario_id={usuario["id"]}', headers=headers)
    
    protocolo = request.args.get('protocolo')
    if not protocolo:
        if response:
            cpis = response.json()
        else:
            cpis = []   
        
        return render_template('cpis_chefe_de_curso.html', cpis=cpis, usuario=usuario)
    
    else:
        if response:
            cpis = response.json()  
            for cpi in cpis:
                if cpi['id'] == int(protocolo):
                    params = {
                        'cpi_id': cpi['id']
                    }
                    
                    response = requests.get(f'http://127.0.0.1:8000/defesa/get_by_cpi', params=params, headers=headers)
                    if response:
                        defesa = response.json()
                        return render_template('parecer.html', cpi=cpi, defesa=defesa)
                    else:
                        return render_template('cpis_chefe_de_curso.html', cpis=cpis, usuario=usuario)   
                    
                
            return render_template('cpis_chefe_de_curso.html', cpis=cpis, usuario=usuario)
            
        else:
            cpis = []
            return render_template('cpis_chefe_de_curso.html', cpis=cpis, usuario=usuario)


@usuario.route('/cpis_cmd_cia', methods=['GET'])
def cpis_cmd_cia():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']

    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_cmd_cia?usuario_id={usuario["id"]}', headers=headers)
    
    protocolo = request.args.get('protocolo')
    if not protocolo:
        if response:
            cpis = response.json()
        else:
            cpis = []   
        
        return render_template('cpis_cmd_cia.html', cpis=cpis, usuario=usuario)
    
    else:
        if response:
            cpis = response.json()  
            for cpi in cpis:
                if cpi['id'] == int(protocolo):
                    params = {
                        'cpi_id': cpi['id']
                    }
                    
                    response = requests.get(f'http://127.0.0.1:8000/defesa/get_by_cpi', params=params, headers=headers)
                    if response:
                        defesa = response.json()
                        return render_template('parecer_cmd_cia.html', cpi=cpi, defesa=defesa)
                    else:
                        return render_template('parecer_cmd_cia.html', cpi=cpi, defesa=False)
                         
                    
                
            return render_template('cpis_cmd_cia.html', cpis=cpis, usuario=usuario)
            
        else:
            cpis = []
            return render_template('cpis_cmd_cia.html', cpis=cpis, usuario=usuario)


@usuario.route('/cpis_comandante', methods=['GET'])
def cpis_comandante():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_comandante?usuario_id={usuario["id"]}', headers=headers)
    
    protocolo = request.args.get('protocolo')
    if not protocolo:
        if response:
            cpis = response.json()
        else:
            cpis = []   
        
        return render_template('cpis_comandante.html', cpis=cpis, usuario=usuario)
    
    else:
        if response:
            cpis = response.json()
            for cpi in cpis:
                if cpi['id'] == int(protocolo):
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
                        
                    response = requests.get(f'http://127.0.0.1:8000/parecer/get_by_cpi', params={'cpi_id': cpi['id']})
                    if response:
                        parecer = response.json()
                    else:
                        parecer = None
                        
                    return render_template('decisao.html', cpi=cpi, artigos=ARTIGOS, defesa=defesa, parecer=parecer, parecer_cmd_cia=parecer_cmd_cia)
                
            return redirect(url_for('usuario.cpis_comandante'))
            
        else:
            cpis = []
            return redirect(url_for('usuario.cpis_comandante'))
    

@usuario.route('/defesa', methods=['POST'])
def defesa():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    response = requests.get(f'http://127.0.0.1:8000/info/get_by_usuario?id={usuario["id"]}', headers=headers)
    if not response:
        return redirect(url_for('usuario.home', erro=1))
    
    info = response.json()
    
    ciente = request.form.get('ciente')
    ciente = True if ciente == 'True' else False
    justificativa = request.form.get('justificativa') if request.form.get('justificativa') else ''
    protocolo = int(request.args.get('protocolo'))
    
    params = {
        'cpi_id': protocolo
    }
    
    response = requests.get(f'http://127.0.0.1:8000/defesa/get_by_cpi', params=params, headers=headers)
    
    id = response.json()['id']
    
    data_justificada = date.today().strftime('%d/%m/%Y')
    
    if ciente:
        json = {
            'id': id,
            'ciente': ciente,
            'data_justificada': data_justificada,
            'ass_aluno': True,
            'status': 12,
        }
    else:
        json = {
            'id': id,
            'ciente': ciente,
            'defesa': justificativa,
            'data_justificada': data_justificada,
            'ass_aluno': True,
            'status': 2,

        }
    
    response = requests.put(f'http://127.0.0.1:8000/defesa/update_defesa', json=json, headers=headers)
    
    return redirect(url_for('usuario.home'))


@usuario.route('/ciente_comunicante', methods=['POST'])
def ciente_comunicante():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    ciente = request.form.get('ciente')
    ciente = True if ciente == 'True' else False
    justificativa = request.form.get('justificativa') if request.form.get('justificativa') else ''
    id = int(request.args.get('protocolo'))
        
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
            
    response = requests.put(f'http://127.0.0.1:8000/cpi/update_cpi', json=json, headers=headers)
    return redirect(url_for('usuario.home'))


@usuario.route('/parecer', methods=['POST'])
def parecer():
    if not session.get('usuario'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    sugestao = request.form.get('sugestao')
    justificativa = request.form.get('justificativa') if request.form.get('justificativa') else ''
    id = int(request.args.get('protocolo'))
    
    data = date.today().strftime('%d/%m/%Y')
    
    json = {
        'cpi': int(id),
        'parecer': sugestao,
        'observacoes': justificativa,
        'data': data,
        'chefe_de_curso': int(session.get('usuario')),
        'ass': True,
    }
    
    response = requests.post(f'http://127.0.0.1:8000/parecer/create', json=json, headers=headers)
    return redirect(url_for('usuario.home'))


@usuario.route('/parecer_cmd_cia', methods=['POST'])
def parecer_cmd_cia():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    sugestao = request.form.get('sugestao')
    justificativa = request.form.get('justificativa') if request.form.get('justificativa') else ''
    id = int(request.args.get('protocolo'))
    
    data = date.today().strftime('%d/%m/%Y')
    
    json = {
        'parecer': sugestao,
        'observacoes': justificativa,
        'data': data,
        'cmd_cia': int(session.get('usuario')),
        'ass': True,
        'cpi': int(id),
    }
    
    
    response = requests.post(f'http://127.0.0.1:8000/parecer_cmd_cia/create', json=json, headers=headers)
    return redirect(url_for('usuario.home'))


@usuario.route('/decisao', methods=['POST'])
def decisao():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    decisao = request.form.get('decisao')
    justificativa = request.form.get('justificativa') if request.form.get('justificativa') else ''
    enquadramento = request.form.get('enquadramento')
    if request.args.get('protocolo'):
        id = int(request.args.get('protocolo'))
    else:
        ...
    
    data = date.today().strftime('%d/%m/%Y')
    
    json = {
        'decisao': decisao,
        'observacoes': justificativa,
        'enquadramento': enquadramento,
        'data': data,
        'comandante': int(session.get('usuario')),
        'ass': True,
        'cpi': id,
    }
    
    response = requests.post(f'http://127.0.0.1:8000/decisao/create', json=json, headers=headers)
    return redirect(url_for('usuario.home'))
    
    
@usuario.route('/perfil')
def perfil():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    id = request.args.get('usuario', type=int)
    response = requests.get(f'http://127.0.0.1:8000/info/get_by_usuario?id={id}', headers=headers)
    
    if not response:
        return redirect(url_for('consulta.consultar'))
            
    info = response.json()
    
    response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_all_aluno?usuario_id={id}', headers=headers)
    cpis = response.json()

    infos = [info, cpis]
    
    return infos


