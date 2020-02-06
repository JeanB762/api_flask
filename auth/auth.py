import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from db.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        visualizacao = request.form['visualizacao']
        
        db = get_db()
        error = None

        if not nome:
            error = 'Nome is required.'
        elif not telefone:
            error = 'Telefone is required.'
        elif db.execute(
            'SELECT id FROM client WHERE nome = ?', (nome,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(nome)

        if error is None:
            db.execute(
                'INSERT INTO client (nome, telefone, visualizacao) VALUES (?, ?, ?)',
            )
            db.commit()
            return 'salvo no db'

        flash(error)

    return 'cadastro realizado'