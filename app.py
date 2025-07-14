from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from utils import carregar_dados, salvar_dados

app = Flask(__name__)
app.secret_key = 'chave_secreta_segura'

# Carregamento de dados salvos em arquivos JSON
usuarios = carregar_dados('usuarios.json')
posts = carregar_dados('posts.json')


# ========================
# ROTA DE LOGIN
# ========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        if usuario == 'admin' and senha == '123':
            session['logado'] = True
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha inválidos')
            return redirect(url_for('login'))
    return render_template('login.html')


# ========================
# ROTA DE LOGOUT
# ========================
@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('login'))


# ========================
# PÁGINA PRINCIPAL (DASHBOARD)
# ========================
@app.route('/')
def home():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('index.html', usuarios=usuarios, posts=posts)


# ========================
# LISTAGEM DE USUÁRIOS
# ========================
@app.route('/usuarios')
def listar_usuarios():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('usuarios.html', usuarios=usuarios)


# ========================
# FORMULÁRIO PARA NOVO USUÁRIO
# ========================
@app.route('/novo-usuario', methods=['GET', 'POST'])
def novo_usuario():
    if not session.get('logado'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        usuarios.append({'nome': nome, 'email': email})
        salvar_dados('usuarios.json', usuarios)
        return redirect(url_for('listar_usuarios'))
    return render_template('usuario_form.html')


# ========================
# LISTAGEM DE POSTAGENS
# ========================
@app.route('/posts')
def listar_posts():
    if not session.get('logado'):
        return redirect(url_for('login'))
    return render_template('posts.html', posts=posts)


# ========================
# FORMULÁRIO PARA NOVA POSTAGEM
# ========================
@app.route('/novo-post', methods=['GET', 'POST'])
def novo_post():
    if not session.get('logado'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        titulo = request.form['titulo']
        conteudo = request.form['conteudo']
        data_criacao = datetime.now().strftime('%d/%m/%Y %H:%M')
        posts.append({
            'titulo': titulo,
            'conteudo': conteudo,
            'data_criacao': data_criacao
        })
        salvar_dados('posts.json', posts)
        return redirect(url_for('listar_posts'))
    return render_template('postagem_form.html')


# ========================
# EXECUÇÃO
# ========================
if __name__ == '__main__':
    app.run(debug=True, port=5002)
