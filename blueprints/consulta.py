from datetime import date
from operator import itemgetter
from flask import Blueprint, redirect, render_template, abort, request, url_for, session
import requests
from jinja2 import TemplateNotFound

from blueprints.artigo import ARTIGOS

consulta = Blueprint('consulta', __name__, url_prefix='/consulta')


@consulta.route('/consultar', methods=['GET', 'POST'])
def consultar():
    if not session.get('token'):
        return redirect(url_for('usuario.login'))
    
    headers = {'Authorization': f'Bearer {session["token"]}'}
    
    response = requests.get(f'http://127.0.0.1:8000/usuario/get_usuario', headers=headers)
    
    if not response:
        del session['token']
        return redirect(url_for('usuario.login', erro=1))
    
    usuario = response.json()['__data__']
    
    usuarios = requests.get(f'http://127.0.0.1:8000/usuario/get_all', headers=headers).json()
    alunos = filter(lambda usuario: usuario['funcao'] == 'ALUNO' or usuario['funcao'] == 'JUSTICA', usuarios)
    chefes = filter(lambda usuarios: usuarios['funcao'] == 'CHEFE DE CURSO', usuarios)
    
    alunos = list(alunos)
    comunicantes = usuarios
    chefes = list(chefes)
    
    if request.method == 'GET':
        return render_template('consulta.html', alunos=alunos, comunicantes=comunicantes, chefes=chefes, usuario=usuario, itens=30)
    
    
    tipo = request.form.get('tipo')
    conduta = request.form.get('conduta')
    aluno = request.form.get('aluno', type=int)
    comunicante = request.form.get('comunicante')
    chefe_de_curso = request.form.get('chefe_de_curso')
    pelotao = request.form.get('pelotao')
    cia = request.form.get('cia')
    categoria_cp = request.form.get('categoria-cp')
    categoria_usuario = request.form.get('categoria-usuario')
    ordenar = request.form.get('ordenar')
    login = request.form.get('login')
    nome = request.form.get('nome')
    curso = request.form.get('curso')
    ano = request.form.get('ano')
    status = request.form.get('status')
    ativo = request.form.get('ativo')
    
    if tipo == 'cp':
        if categoria_cp == 'aluno':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_aluno?usuario_id={aluno}&conduta={conduta}', headers=headers)
        elif categoria_cp == 'chefe de curso':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_chefe_de_curso?usuario_id={chefe_de_curso}&conduta={conduta}', headers=headers)
        elif categoria_cp == 'comunicante':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_comunicante?usuario_id={comunicante}&conduta={conduta}', headers=headers)
        elif categoria_cp == 'pelotao':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_pelotao?pelotao={pelotao}&conduta={conduta}', headers=headers)
        elif categoria_cp == 'cia':
            response = requests.get(f'http://127.0.0.1:8000/cpi/consulta_cia?cia={cia}&conduta={conduta}', headers=headers)
        else:
            response = requests.get(f'http://127.0.0.1:8000/cpi/get_all?conduta={conduta}', headers=headers)
    elif tipo == 'usuario':
        if categoria_usuario == 'nome':                   
            response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_nome?nome={nome}', headers=headers)
        # elif categoria_usuario == 'login':
        #     response = requests.get(f'http://127.0.0.1:8000/usuario/get_by_login?login={login}', headers=headers)
        elif categoria_usuario == 'pelotao':
            tipo = 'aluno'
            response = requests.get(f'http://127.0.0.1:8000/info/get_by_curso_ano_pelotao?curso={curso}&ano={ano}&pelotao={pelotao}', headers=headers)
        elif categoria_usuario == 'cia':
            tipo = 'aluno'
            response = requests.get(f'http://127.0.0.1:8000/info/get_by_cia?cia={cia}', headers=headers)
        else:
            response = requests.get(f'http://127.0.0.1:8000/usuario/get_all', headers=headers)
        
    if response.status_code == 500:
        return redirect(url_for('consulta.consultar'))
    
    dados = response.json()
    
    if (categoria_usuario == 'pelotao' or categoria_usuario == 'cia') and tipo == 'usuario':
        if ordenar == 'nota maior':
            dados = sorted(dados, key=itemgetter('nota_conduta'))
        elif ordenar == 'nota menor':
            dados = sorted(dados, key=itemgetter('nota_conduta'), reverse=True)
        else:
            ...
    
    if tipo == 'usuario':
        if ativo == '-':
            ...
        elif ativo == 'True':
            usuarios = list()
            for usuario in dados:
                if usuario['ativo'] == True:
                    usuarios.append(usuario)
            dados = usuarios
        elif ativo == 'False':
            usuarios = list()
            for usuario in dados:
                if usuario['ativo'] == False:
                    usuarios.append(usuario)
            dados = usuarios
    
    if tipo == 'aluno':
        if ativo == '-':
            ...
        elif ativo == 'True':
            usuarios = list()
            for usuario in dados:
                if usuario['aluno']['ativo'] == True:
                    usuarios.append(usuario)
            dados = usuarios
        elif ativo == 'False':
            usuarios = list()
            for usuario in dados:
                if usuario['aluno']['ativo'] == False:
                    usuarios.append(usuario)
            dados = usuarios
    
    if tipo == 'cp':
        cpis = list()
        if status != '-':
            for cpi in dados:
                if status != None:
                    if cpi['status'] == int(status):
                        cpis.append(cpi)
                else:
                    cpis.append(cpi)    
            dados = cpis
        
        if ativo == '-':
            ...
        elif ativo == 'True':
            cpis = list()
            for cpi in dados:
                if cpi['aluno']['ativo'] == True:
                    cpis.append(cpi)
            dados = cpis
        elif ativo == 'False':
            cpis = list()
            for cpi in dados:
                if cpi['aluno']['ativo'] == False:
                    cpis.append(cpi)
            dados = cpis
                
    
    return render_template('consulta.html', alunos=alunos, comunicantes=comunicantes, chefes=chefes, usuario=usuario, dados=dados, tipo=tipo, itens=30)