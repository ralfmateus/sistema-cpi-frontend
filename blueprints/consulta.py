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
    categoria = request.form.get('categoria')
    ordenar = request.form.get('ordenar')
    
    if tipo == 'cp':
        if categoria == 'aluno':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_aluno?usuario_id={aluno}')
        elif categoria == 'chefe de curso':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_chefe_de_curso?usuario_id={chefe_de_curso}')
        elif categoria == 'comunicante':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_comunicante?usuario_id={comunicante}')
        elif categoria == 'pelotao':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_pelotao?pelotao={pelotao}')
        elif categoria == 'cia':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_cia?cia={cia}')
        else:
            response = requests.get(f'http://127.0.0.1:8000/cpi/get_all')
        
    cpis = response.json()
    
    if ordenar == 'nota maior':
        ...
    elif ordenar == 'nota menor':
        ...
    else:
        ...
    
    
    
    
    
    return render_template('consulta.html', alunos=alunos, comunicantes=comunicantes, chefes=chefes, usuario=usuario, cpis=cpis, itens=30)