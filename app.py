#Importa as funções e classes do flask
from flask import Flask, redirect, render_template, request, session

#Inicializa o objeto Flask, instanciando a classe Flask
app = Flask(__name__)

#Define a chave secreta para a aplicação Flask
app.secret_key = 'MINHA CHAVE SECRETA'

#Define a rota raiz da aplicação
@app.get('/')
def paginaInicial():
    if 'nomeUsuarioLogado' in session:
        return render_template('pagina_usuario_logado.html', nomeUsuario=session['nomeUsuarioLogado'])
    else:
        return redirect("/login")

#Define a rota para exibir a página de login
@app.get('/login')
def exibirPaginaLogin():
    return render_template('login.html', msgErro='')

#Define a rota para processar o login
@app.post('/login')
def realizarLogin():
    usuarios = [
        {'email': 'teste@teste.com', 'password': '123456', 'nome': 'Teste'},
        {'email': 'camila@teste.com', 'password': 'abcdef', 'nome': 'Camila'},
        {'email': 'joao@teste.com', 'password': 'qwerty', 'nome': 'João'}
    ]

    email = request.form.get('email')
    password = request.form.get('password')

    nomeUsuarioEncontrado = None

    for u in usuarios:
        if u['email'] == email and u['password'] == password:
            nomeUsuarioEncontrado = u['nome']
            break

    if nomeUsuarioEncontrado is not None:
        session['nomeUsuarioLogado'] = nomeUsuarioEncontrado
        return render_template('pagina_usuario_logado.html', nomeUsuario=nomeUsuarioEncontrado)
    else:
        return render_template('login.html', msgErro='Usuário ou senha inválidos. Tente novamente.')

#Define a rota para processar o logout
@app.get('/logout')
def realizarLogout():
    session.pop('nomeUsuarioLogado', None)
    return "Logout realizado com sucesso!"

#Função para validar se o usuário está autenticado
def validarAutenticacaoUsuario():
    return ('nomeUsuarioLogado' in session)

#Define a rota para exibir a página do usuário logado
@app.get('/pagina_usuario_logado')
def paginanomeUsuarioLogado():
    if validarAutenticacaoUsuario() == True:
        return render_template('pagina_usuario_logado.html', nomeUsuario=session['nomeUsuarioLogado'])
    else:
        return redirect("/login")

#Define uma ação para tratar erros 404 (página não encontrada
@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")

#Inicia o servidor Flask, chamando o método run do objeto app
if __name__ == '__main__':
    app.run(debug=True, port=80)