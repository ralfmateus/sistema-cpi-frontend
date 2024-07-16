from datetime import date
from flask import Blueprint, redirect, render_template, abort, request, url_for, session
import requests
from jinja2 import TemplateNotFound

from blueprints.artigo import ARTIGOS

consulta = Blueprint('consulta', __name__, url_prefix='/consulta')


@consulta.route('/consultar', methods=['GET', 'POST'])
def consultar():
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_id?id={session["usuario"]}')
    
    if not response:
        del session['usuario']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()
    
    usuarios = requests.get(f'http://127.0.0.1:8000/usuario/get_all').json()
    alunos = filter(lambda usuario: usuario['funcao'] == 'ALUNO' or usuario['funcao'] == 'JUSTICA', usuarios)
    chefes = filter(lambda usuarios: usuarios['funcao'] == 'CHEFE DE CURSO', usuarios)
    
    alunos = list(alunos)
    comunicantes = usuarios
    chefes = list(chefes)
    
    if request.method == 'GET':
        return render_template('consulta.html', alunos=alunos, comunicantes=comunicantes, chefes=chefes, usuario=usuario, itens=30)
    
    
    tipo = request.form.get('tipo')
    conduta = request.form.get('conduta')
    aluno = request.form.get('aluno')
    comunicante = request.form.get('comunicante')
    chefe_de_curso = request.form.get('chefe_de_curso')
    pelotao = request.form.get('pelotao')
    cia = request.form.get('cia')
    categoria_cp = request.form.get('categoria-cp')
    categoria_usuario = request.form.get('categoria-usuario')
    ordenar = request.form.get('ordenar')
    login = request.form.get('login')
    nome = request.form.get('nome')
    
    if tipo == 'cp':
        if categoria_cp == 'aluno':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_aluno?usuario_id={aluno}&conduta={conduta}')
        elif categoria_cp == 'chefe de curso':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_chefe_de_curso?usuario_id={chefe_de_curso}&conduta={conduta}')
        elif categoria_cp == 'comunicante':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_comunicante?usuario_id={comunicante}&conduta={conduta}')
        elif categoria_cp == 'pelotao':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_pelotao?pelotao={pelotao}&conduta={conduta}')
        elif categoria_cp == 'cia':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_cia?cia={cia}&conduta={conduta}')
        else:
            response = requests.get(f'http://127.0.0.1:8000/cpi/get_all?conduta={conduta}')
    elif tipo == 'usuario':
        if categoria_usuario == 'login':
            response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_login?login={login}')
        elif categoria_usuario == 'nome':
            response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_nome?nome={nome}')
        # elif categoria_usuario == 'pelotao':
            # response = requests.get(f'http://127.0.0.1:8000/usuario/consulta_pelotao?pelotao={pelotao}')
        # elif categoria_usuario == 'cia':
            # response = requests.get(f'http://127.0.0.1:8000/usuario/consulta_cia?cia={cia}')
        else:
            response = requests.get(f'http://127.0.0.1:8000/usuario/get_all')
        
    cpis = response.json()
    
    if ordenar == 'nota maior':
        ...
    elif ordenar == 'nota menor':
        ...
    else:
        ...
    
    
    
    
    
    return render_template('consulta.html', alunos=alunos, comunicantes=comunicantes, chefes=chefes, usuario=usuario, cpis=cpis, tipo=tipo, itens=30)