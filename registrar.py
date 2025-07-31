import json
USUARIOS_ARQUIVO = 'data/usuarios.json'

import re
from criptografia import Criptografia

def senha_valida(senha):
    # Senha com pelo menos 8 caracteres, uma letra maiúscula, uma minúscula e um número
    padrao = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
    return re.match(padrao, senha) is not None

def CriarUsuario(nome, senha):
    try:
        with open(USUARIOS_ARQUIVO, 'r') as f:
            usuarios = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        usuarios = {}

    # Criptografa a senha antes de salvar
    senha_hash = Criptografia(senha)

    # Adiciona novo usuário
    usuarios[nome] = senha_hash

    # Salva o arquivo atualizado
    with open(USUARIOS_ARQUIVO, 'w') as f:
        json.dump(usuarios, f, indent=4)

    print(f"Usuário {nome} criado com sucesso!")

def RegistroPrincipal(nome, senha, senha2): 
    try:
        with open(USUARIOS_ARQUIVO, 'r') as f:
            usuarios = json.load(f)
            print("File found")
    except (FileNotFoundError, json.JSONDecodeError):
        usuarios = {}
        print("File not found")

    # Verifica se usuário já existe

    if not senha_valida(senha):
        return 0 # Senha invalida

    if nome in usuarios:
        return 1  # Usuário já existe

    # Verifica se as senhas batem
    if senha != senha2:
        return 2  # Senhas não coincidem

    # Se chegou aqui, está tudo certo
    return 3  # Sucesso
