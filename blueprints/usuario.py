from datetime import date
from flask import Blueprint, redirect, render_template, abort, request, url_for, session
import requests
from jinja2 import TemplateNotFound

from blueprints.artigo import ARTIGOS

usuario = Blueprint('usuario', __name__, url_prefix='/usuario')


@usuario.route('/adicionar', methods=['GET', 'POST'])
def adicionar_usuario():
    # if not session.get('token'):
    #     return redirect(url_for('usuario.login'))
    
    # headers = {'Authorization': f'Bearer {session["token"]}'}
    
    # response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    # if not response:
    #     del session['token']
    #     return redirect(url_for('usuario.login', erro=1))
    
    # usuario = response.json()['__data__']
    
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
        
        # response = requests.post('http://127.0.0.1:8000/usuario/create', json=usuario, headers=headers)
        response = requests.post('http://127.0.0.1:8000/usuario/create', json=usuario)
        
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
                # response = requests.post('http://127.0.0.1:8000/info/create', json=info, headers=headers)
                response = requests.post('http://127.0.0.1:8000/info/create', json=info)
                
            elif usuario['funcao'] ==  'CHEFE DE CURSO':
                info = {
                    "curso": request.form.get('curso'),
                    "ano": request.form.get('ano'),
                    "pelotao": request.form.get('pelotao'),
                    "usuario": usuario['id']
                }
                
                # response = requests.post('http://127.0.0.1:8000/info/create', json=info, headers=headers)
                response = requests.post('http://127.0.0.1:8000/info/create', json=info)
                
            elif usuario['funcao'] == 'COMANDANTE DE CIA':
                info = {
                    "curso": request.form.get('curso'),
                    "ano": request.form.get('ano'),
                    "cia": request.form.get('cia'),
                    "pelotao": request.form.get('pelotao'),
                    "usuario": usuario['id']
                }
            
                # response = requests.post('http://127.0.0.1:8000/info/create', json=info, headers=headers)
                response = requests.post('http://127.0.0.1:8000/info/create', json=info)
            
            return redirect(url_for('usuario.adicionar_usuario'))
        
        return redirect(url_for('usuario.adicionar_usuario', erro=1))


@usuario.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('token'):
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
                        
                    response = requests.get(f'http://127.0.0.1:8000/parecer/get_by_cpi', params={'cpi_id': cpi['id']}, headers=headers)
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
        
    if not ciente:
        json = {
            'id': id,
            'justificativa': justificativa,
            'ass_comunicante': True,
            'status': 10,
        }
    else:
        json = {
            'id': id,
            'ass_comunicante': True,
            'status': 1
        }
            
    response = requests.put(f'http://127.0.0.1:8000/cpi/update_cpi', json=json, headers=headers)
    return redirect(url_for('usuario.home'))


@usuario.route('/parecer', methods=['POST'])
def parecer():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
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
        'chefe_de_curso': int(usuario['id']),
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
        'cmd_cia': int(usuario['id']),
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
        'enquadramento': enquadramento.upper(),
        'data': data,
        'comandante': int(usuario['id']),
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
    
    current_user = response.json()['__data__']
    
    id = request.args.get('id', type=int)
    
    if not id:
        return redirect(url_for('consulta.consultar'))
    
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_id?id={id}', headers=headers)
    
    if not response:
        return redirect(url_for('consulta.consultar'))
    
    usuario = response.json()
    
    
    if usuario['funcao'] == 'JUSTICA' or usuario['funcao'] == 'ALUNO':
        response = requests.get(f'http://127.0.0.1:8000/info/get_by_usuario?id={id}', headers=headers)
        
        if not response:
            return redirect(url_for('consulta.consultar'))
                
        info = response.json()
        
        response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_all_aluno?usuario_id={info["usuario"]["id"]}', headers=headers)
        
        if not response:
            return redirect(url_for('consulta.consultar'))
        
        cpis = response.json()
        
        response = {
            'info': info,
            'cpis': cpis,
            'aluno': True
        }
    
    else:
        if usuario['funcao'] == 'CHEFE DE CURSO' or usuario['funcao'] == 'COMANDANTE DE CIA':
            response = requests.get(f'http://127.0.0.1:8000/info/get_by_usuario?id={id}', headers=headers)
        
            if not response:
                return redirect(url_for('consulta.consultar'))
                    
            info = response.json()
            
        else:
            info = False
        
        response = {
            'usuario': usuario,
            'info': info,
            'aluno': False
        }
        
    return render_template('perfil_consulta.html', dados=response)


@usuario.route('/perfil_atual')
def perfil_atual():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    current_user = response.json()['__data__']
    
    id = current_user['id']
    
    if not id:
        return redirect(request.referrer)
    
    
    if current_user['funcao'] == 'JUSTICA' or current_user['funcao'] == 'ALUNO':
        response = requests.get(f'http://127.0.0.1:8000/info/get_by_usuario?id={id}', headers=headers)
        
        if not response:
            return redirect(request.referrer)
                
        info = response.json()
        
        response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_all_aluno?usuario_id={info["usuario"]["id"]}', headers=headers)
        
        if not response:
            return redirect(url_for('consulta.consultar'))
        
        cpis = response.json()
        
        cpis = False

        response = {
            'info': info,
            'cpis': cpis,
            'aluno': True
        }
    
    else:
        if current_user['funcao'] == 'CHEFE DE CURSO' or current_user['funcao'] == 'COMANDANTE DE CIA':
            response = requests.get(f'http://127.0.0.1:8000/info/get_by_usuario?id={id}', headers=headers)
        
            if not response:
                return redirect(url_for('usuario.home'))
                    
            info = response.json()
            
        else:
            info = False
        
        response = {
            'usuario': current_user,
            'info': info,
            'aluno': False
        }

    return render_template('perfil_atual.html', dados=response)


@usuario.route('/trocar_senha', methods=['GET', 'POST'])
def trocar_senha():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    current_user = response.json()['__data__']
    
    if request.method == 'GET':
        return render_template('trocar_senha.html')
    
    login = request.form.get('login')
    senha_atual = request.form.get('senha_atual')
    nova_senha1 = request.form.get('nova_senha1')
    nova_senha2 = request.form.get('nova_senha2')
    
    
    data = {
            "username": login,
            "password": senha_atual,
        }
        
    response = requests.post('http://127.0.0.1:8000/usuario/token', data=data, headers=headers)
    
    
    if response.status_code == 200:        
        if not nova_senha1 == nova_senha2:
            return redirect(url_for('usuario.trocar_senha', erro=1))
                
        # **************************    EFETIVAMENTE TROCAR A SENHA     *********************************
        
        data = {
            'login': login,
            'senha': nova_senha1,
        }
        
        response = requests.put('http://127.0.0.1:8000/usuario/trocar_senha', json=data, headers=headers)
                
        if response.status_code == 200:
            return redirect(url_for('usuario.home'))
        else:
            return redirect(url_for('usuario.trocar_senha', id=current_user['id'], erro=2))
        
    else:
        return redirect(url_for('usuario.trocar_senha', id=current_user['id'], erro=3))    
        
        
@usuario.route('/editar_perfil_aluno', methods=['GET', 'POST'])
def editar_perfil_aluno():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    current_user = response.json()['__data__']

    if request.method == 'GET':
        id = request.args.get('id', type=int)
        
        if not id:
            return redirect(url_for('consulta.consultar'))
        
        # EDITAR PERFIL COMPLETO EXCETO DADOS SENCIVEIS COMO SENHA, LOGIN E NOTA DE CONDUTA
        response = requests.get(f'http://127.0.0.1:8000/info/get_by_usuario?id={id}', headers=headers)
        
        if not response:
            return redirect(url_for('consulta.consultar'))
        
        info = response.json()
    
        return render_template('editar_perfil_aluno.html', info=info)
    
    # **********************************    EFETIVAMENTE EDITAR PERFIL    *********************************
    
    ativo = True if request.form.get('ativo') == 'True' else False
    
    usuario = {
            "id": request.form.get('id'),
            "funcao": request.form.get('funcao'),
            "nome": request.form.get('nome'),
            "nome_de_guerra": request.form.get('nome_de_guerra'),
            "grau_hierarquico": request.form.get('grau_hierarquico'),
            "ativo": ativo
        }
    
    info = {
            "curso": request.form.get('curso'),
            "ano": request.form.get('ano'),
            "cia": request.form.get('cia'),
            "pelotao": request.form.get('pelotao'),
            "numero": request.form.get('numero'),
            "usuario": usuario['id']
        }
    
    response = requests.put('http://127.0.0.1:8000/usuario/update_usuario', json=usuario, headers=headers)
    if response.status_code == 200:
        response = requests.put('http://127.0.0.1:8000/info/update_info', json=info, headers=headers)
        if response.status_code == 200:
            return redirect(url_for('usuario.perfil', id=usuario['id']))
        else:
            return redirect(url_for('usuario.editar_perfil_aluno', id=usuario['id'], erro=1))
    else:
        return redirect(url_for('usuario.editar_perfil_aluno', id=usuario['id'], erro=2))
    
        
@usuario.route('/editar_perfil_usuario', methods=['GET', 'POST'])
def editar_perfil_usuario():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    current_user = response.json()['__data__']

    if request.method == 'GET':
        id = request.args.get('id', type=int)
        
        if not id:
            return redirect(url_for('consulta.consultar'))
        
        # EDITAR PERFIL COMPLETO EXCETO DADOS SENCIVEIS COMO SENHA, LOGIN E NOTA DE CONDUTA
        response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_id?id={id}', headers=headers)
        
        if not response:
            redirect(url_for('consulta.consultar'))
        
        usuario = response.json()
    
        if usuario['funcao'] == 'CHEFE DE CURSO' or usuario['funcao'] == 'COMANDANTE DE CIA':
            response = requests.get(f'http://127.0.0.1:8000/info/get_by_usuario?id={id}', headers=headers)
        
            if not response:
                redirect(url_for('consulta.consultar'))
            
            info = response.json()
            
        else:
            info = False
        
        return render_template('editar_perfil_usuario.html', usuario=usuario, info=info)
        
    # **********************************    EFETIVAMENTE EDITAR PERFIL    *********************************
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_id?id={request.form.get("id")}', headers=headers)
        
    if not response:
        redirect(url_for('consulta.consultar'))
    
    user = response.json()
    
    ativo = True if request.form.get('ativo') == 'True' else False
    usuario = {
            "id": request.form.get('id'),
            "funcao": request.form.get('funcao'),
            "nome": request.form.get('nome'),
            "nome_de_guerra": request.form.get('nome_de_guerra'),
            "grau_hierarquico": request.form.get('grau_hierarquico'),
            "ativo": ativo
        }
    
    if user['funcao'] == 'CHEFE DE CURSO' or user['funcao'] == 'COMANDANTE DE CIA':
        if request.form.get('cia'):
            info = {
                    "curso": request.form.get('curso'),
                    "ano": request.form.get('ano'),
                    "cia": request.form.get('cia'),
                    "pelotao": request.form.get('pelotao'),
                    "usuario": usuario['id']
                }
        else:
            info = {
                    "curso": request.form.get('curso'),
                    "ano": request.form.get('ano'),
                    "cia": '',
                    "pelotao": request.form.get('pelotao'),
                    "usuario": usuario['id']
                }
    else:
        info = False
            
    response = requests.put('http://127.0.0.1:8000/usuario/update_usuario', json=usuario, headers=headers) 
    if response.status_code == 200:
        if info:
            response = requests.put('http://127.0.0.1:8000/info/update_info', json=info, headers=headers)
            print(response.json())
            if response.status_code == 200:
                return redirect(url_for('usuario.perfil', id=usuario['id']))
            else:
                return redirect(url_for('usuario.editar_perfil_usuario', id=usuario['id'], erro=1))
        else:
            return redirect(url_for('usuario.perfil', id=usuario['id']))
    else:
        return redirect(url_for('usuario.editar_perfil_usuario', id=usuario['id'], erro=2))