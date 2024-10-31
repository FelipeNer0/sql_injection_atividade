from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para inicializar o banco de dados e adicionar usuários e cartões de crédito
def inicializa_banco():
    con = sqlite3.connect('usuarios.db')
    cursor = con.cursor()

    # Cria a tabela 'usuarios' se ela não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        senha TEXT NOT NULL
    )
    ''')

    # Cria a tabela 'cartoes_credito' se ela não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cartoes_credito (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        numero_cartao TEXT NOT NULL,
        validade TEXT NOT NULL,
        codigo_seguranca TEXT NOT NULL
    )
    ''')

    # Insere dados de teste se a tabela 'usuarios' estiver vazia
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
        INSERT INTO usuarios (login, senha) VALUES (?, ?)
        ''', [
            ('admin', '123456'),
            ('user1', 'password'),
            ('user2', 'senha123'),
        ])

    # Insere dados de teste na tabela 'cartoes_credito'
    cursor.execute("SELECT COUNT(*) FROM cartoes_credito")
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
        INSERT INTO cartoes_credito (nome, numero_cartao, validade, codigo_seguranca) VALUES (?, ?, ?, ?)
        ''', [
            ('John Doe', '1234 5678 9012 3456', '12/25', '123'),
            ('Jane Doe', '9876 5432 1098 7654', '10/24', '456'),
        ])

    con.commit()
    con.close()

# Rota de login vulnerável a SQL Injection
@app.route('/login', methods=['GET', 'POST'])
def login_vulneravel():
    resultado = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Consulta SQL vulnerável a SQL Injection
        query = f"SELECT login, senha, 'placeholder' FROM usuarios WHERE login = '{username}' AND senha = '{password}'"

        con = sqlite3.connect('usuarios.db')
        cursor = con.cursor()

        try:
            cursor.execute(query)
            resultado = cursor.fetchall()

            # Se houver resultado, mostre os cartões de crédito
            if resultado:
                resultado = "Usuário autenticado."
                #return redirect(url_for('cartoes'))  # Redireciona para a página de cartões
            else:
                resultado = "Usuário ou senha incorretos."
        except Exception as e:
            resultado = f"Erro na consulta: {e}"
        finally:
            con.close()

    return render_template('login.html', resultado=resultado)

# Página para exibir cartões de crédito
@app.route('/cartoes')
def cartoes():
    con = sqlite3.connect('usuarios.db')
    cursor = con.cursor()
    cursor.execute("SELECT nome, numero_cartao, validade, codigo_seguranca FROM cartoes_credito")
    cartoes = cursor.fetchall()  # Recupera todos os cartões de crédito
    con.close()
    return render_template('cartoes.html', cartoes=cartoes)

# Página de login
@app.route('/')
def login_page():
    return render_template('login.html')

# Inicializa o banco de dados e roda o servidor Flask
if __name__ == '__main__':
    inicializa_banco()  # Inicializa o banco de dados com usuários e cartões de crédito
    app.run(debug=True)
