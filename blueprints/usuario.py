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
        
        return render_template('adicionar_usuario.html')
    

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
    
    if response:
        cpis = response.json()
    else:
        cpis = []   
    
    
    return render_template('home.html', cpis=cpis)


@usuario.route('/cpis_comunicante', methods=['GET'])
def cpis_comunicante():
    if not session.get('usuario'):
        return redirect(url_for('usuario.login'))

    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_comunicante?usuario_id={session["usuario"]}')
    
    if response:
        cpis = response.json()
    else:
        cpis = []   
    
    
    return render_template('home.html', cpis=cpis)


@usuario.route('/cpis_chefe_de_curso', methods=['GET'])
def cpis_chefe_de_curso():
    if not session.get('usuario'):
        return redirect(url_for('usuario.login'))

    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_chefe_de_curso?usuario_id={session["usuario"]}')
    
    if response:
        cpis = response.json()
    else:
        cpis = []   
        
    
    return render_template('home.html', cpis=cpis)


@usuario.route('/cpis_comandante', methods=['GET'])
def cpis_comandante():
    if not session.get('usuario'):
        return redirect(url_for('usuario.login'))

    response = requests.get(f'http://127.0.0.1:8000/cpi/get_all_comandante?usuario_id={session["usuario"]}')
    
    if response:
        cpis = response.json()
    else:
        cpis = []   
        
    
    return render_template('home.html', cpis=cpis)
    
    
        
    