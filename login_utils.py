import json

from criptografia import Criptografia

USUARIOS_ARQUIVO = 'data/usuarios.json'

def LoginPrincipal(nome, senha):  
    try:
        with open(USUARIOS_ARQUIVO, 'r') as f:
            usuarios = json.load(f)
            print("File found")
    except (FileNotFoundError, json.JSONDecodeError):
        usuarios = {}
        print("File not found")

    senha = Criptografia(senha)
    print(senha)
   
   
    if nome in usuarios:
        print("Existe o usúario")

        if usuarios[nome] == senha:
            print("senha correta")
            return 6
        else:
            print("senha incorreta")
            return 5
    else:
        print("usuário não existe")
        return 4
