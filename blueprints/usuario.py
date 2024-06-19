from flask import Blueprint, render_template, abort, request
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
            print(response.json())
        
        return render_template('adicionar_usuario.html')
