from flask import Flask, request, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Para mensagens de flash

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

class CartaoCredito(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    numero_cartao = db.Column(db.String(20), nullable=False)
    validade = db.Column(db.String(5), nullable=False)
    codigo_seguranca = db.Column(db.String(3), nullable=False)

def create_tables():
    with app.app_context():  # Cria um contexto de aplicação
        db.create_all()
        if Usuario.query.count() == 0:
            db.session.add(Usuario(login='admin', senha='123456'))
            db.session.add(Usuario(login='user1', senha='password'))
            db.session.add(Usuario(login='user2', senha='senha123'))
            db.session.commit()

        if CartaoCredito.query.count() == 0:
            db.session.add(CartaoCredito(nome='John Doe', numero_cartao='1234 5678 9012 3456', validade='12/25', codigo_seguranca='123'))
            db.session.add(CartaoCredito(nome='Jane Doe', numero_cartao='9876 5432 1098 7654', validade='10/24', codigo_seguranca='456'))
            db.session.commit()

# Rota de login
@app.route('/attack', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Consulta segura usando Flask-SQLAlchemy
        user = Usuario.query.filter_by(login=username, senha=password).first()
        if user:
            flash('Autenticação bem-sucedida!')
             #return redirect(url_for('cartoes'))  # Redireciona para a página de cartões
        else:
            flash('Usuário ou senha incorretos.')

    return render_template('attack.html')

# Página para exibir cartões de crédito
# @app.route('/cartoes')
#def cartoes():
 #   cartoes = CartaoCredito.query.all()  # Recupera todos os cartões de crédito
  #  return render_template('cartoes.html', cartoes=cartoes)

# Página de login
@app.route('/')
def login_page():
    return redirect(url_for('login'))

if __name__ == '__main__':
    create_tables()  
    app.run(debug=True)
