# Importa o Flask (para criar o servidor web) e o render_template (para exibir arquivos HTML)
import json
import os

from flask import Flask, render_template, request, session
from login_utils import LoginPrincipal
from registrar import RegistroPrincipal, CriarUsuario
from datetime import datetime, timedelta


# Cria uma instância da aplicação Flask (a "cara" do servidor)
app = Flask(__name__)
app.secret_key = 'sua-chave-secreta'  # ESSENCIAL para session funcionar

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USUARIOS_ARQUIVO = os.path.join(BASE_DIR, 'data', 'usuarios.json')

erro_msg = "Usuário ou senha incorretos."
tentativas_restantes = 5


# Define a rota principal ("/") — o que acontece quando o usuário acessa o site
@app.route('/')
def home():
    return render_template('login.html')


mensagens = {
    0: "Senha deve conter pelo menos 8 caracteres, uma letra maiúscula, uma minúscula e um número.",
    1: "Usuário já existe.",
    2: "As senhas não coincidem.",
    3: "Usuário registrado com sucesso!",
    4: "Esse usuário não existe.",
    5: f"Senha incorreta, tente novamente, tentativas restantes:",
    6: "Senha correta",

    # Pode adicionar outras mensagens aqui
}

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nome = request.form['username']
        senha = request.form['password']
        senha2 = request.form['password2']

        print(nome, senha, senha2)
        # Chama sua função de registro para validar e salvar
        can = RegistroPrincipal(nome, senha, senha2)
        print(can)
        erro_msg = mensagens.get(can, "Erro desconhecido")

        if can == 3:
            # Registro sucesso

         CriarUsuario(nome,senha)

         return "Registrado com sucesso!"  # Ou redirecionar para login
        else:
            # Caso erro, mostra a página de registro com a mensagem
            return render_template('registro.html', erro=erro_msg)
    else:
        return render_template('registro.html')




from datetime import datetime, timedelta
from flask import session, render_template, request

@app.route('/login', methods=['POST'])
def login():
    nome = request.form['username']
    senha = request.form['password']

    if 'tentativas_restantes' not in session:
        session['tentativas_restantes'] = 5  # Inicializa

    # Se o usuário estiver bloqueado
    if 'bloqueado_ate' in session:
        agora = datetime.now()
        desbloqueio = datetime.fromisoformat(session['bloqueado_ate'])
        if agora < desbloqueio:
            tempo_restante = desbloqueio - agora
            minutos_restantes = int(tempo_restante.total_seconds() // 60) + 1
            return render_template('login.html', erro=f"Limite de tentativas excedido. Tente novamente em {minutos_restantes} minutos.")

    can = LoginPrincipal(nome, senha)
    print(can)
    erro_msg = mensagens.get(can, "Erro desconhecido")

    if can == 5:
        session['tentativas_restantes'] -= 1

        if session['tentativas_restantes'] <= 0:
            session['bloqueado_ate'] = (datetime.now() + timedelta(minutes=30)).isoformat()
            return render_template('login.html', erro="Limite de tentativas excedido. Tente novamente em 30 minutos.")
        else:
            erro_msg = f"{erro_msg} {session['tentativas_restantes']}"
            return render_template('login.html', erro=erro_msg)

    if can != 6:
        return render_template('login.html', erro=erro_msg)
    else:
        session.pop('tentativas_restantes', None)
        session.pop('bloqueado_ate', None)
        return "Login sucesso"



# Garante que o app só vai rodar se esse arquivo for executado diretamente (não importado por outro)
if __name__ == '__main__':
     # Inicia o servidor em modo debug (atualiza sozinho ao salvar e mostra erros detalhados)
    app.run(debug=True)