import hashlib

def Criptografia(senha):

 senha = senha.encode()  # Senha convertida para bytes
 hash_objeto = hashlib.sha256(senha)  # Objeto que contém o cálculo do hash
 hash_hex = hash_objeto.hexdigest()  # Hash SHA-256 em formato legível

 return hash_hex

