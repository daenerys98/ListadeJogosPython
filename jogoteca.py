from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Hack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
lista = [jogo1, jogo2, jogo3]

class Usuario: 
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario('Hermione', 'Mione', 'alohomora')
usuario2 = Usuario('Harry', 'Zoin', 'raio')
usuario3 = Usuario('Rony', 'Ruivo', 'perebas')

usuarios = {usuario1.nickname : usuario1, #dicionario
            usuario2.nickname :usuario2,
            usuario3.nickname :usuario3}

app = Flask(__name__)
app.secret_key = 'alura' # app.secret_key é uma configuração no Flask usada para assinar dados de sessão. A assinatura é feita com uma chave secreta, que é importante para a segurança das sessões. Garante que os dados da sessão não sejam alterados por terceiros. Exemplo: app.secret_key = 'alura'.

@app.route('/')
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request. form['nome']
    categoria = request. form['categoria']
    console = request. form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect (url_for('index')) # redirecionamento para a rota

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima) #enviando as informações para o html

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.') # O flash é útil quando você deseja exibir mensagens de uma solicitação para a próxima, mas não precisa armazenar essas mensagens a longo prazo. 
        return redirect(url_for('login')) # se não volta para login

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout concluido com sucesso!')
    return redirect (url_for('index'))

app.run(debug=True)