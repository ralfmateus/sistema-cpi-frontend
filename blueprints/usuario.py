from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

usuario = Blueprint('usuario', __name__, url_prefix='/usuario')


@usuario.route('/adicionar')
def adicionar_usuario():
    try:
        return render_template('adicionar_usuario.html')
    except TemplateNotFound:
        abort(404)