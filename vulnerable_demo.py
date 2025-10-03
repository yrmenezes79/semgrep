# vulnerable_demo.py
import os
import hashlib
import pickle
import subprocess
import json
from typing import Any

# 1) Credenciais/API key hardcoded (sensitive info in source)
API_KEY = "supersecretapikey_12345"

DB_PATH = "demo.db"
TEMP_PATH = "/tmp/session_info.txt"

def hash_password_md5(password: str) -> str:
    # 2) Uso de MD5 para "hash" de senha (MD5 é quebrável)
    return hashlib.md5(password.encode("utf-8")).hexdigest()

def save_user(username: str, password: str):
    # Simula salvar usuário em "banco" (arquivo JSON) com senha MD5 - inseguro
    users = {}
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            users = json.load(f)
    users[username] = {"password": hash_password_md5(password)}
    with open(DB_PATH, "w") as f:
        json.dump(users, f)

def authenticate(username: str, password: str) -> bool:
    # 3) Comparação de senha sem sal e com MD5
    if not os.path.exists(DB_PATH):
        return False
    with open(DB_PATH, "r") as f:
        users = json.load(f)
    user = users.get(username)
    if not user:
        return False
    return user["password"] == hash_password_md5(password)

def process_input_file(path: str):
    # 4) Lê um arquivo JSON que contém dados arbitrários de usuário
    # Espera campos: "script", "session_pickle"
    with open(path, "rb") as f:
        data = f.read()
    # Assume UTF-8 JSON — se não for, a função falhará
    payload = json.loads(data.decode("utf-8"))

    # 5) Uso de eval() em input do usuário -> execução arbitrária de código
    if "script" in payload:
        script = payload["script"]
        print("Executando script (vulnerável):")
        result = eval(script)  # **** VULNERÁVEL ****
        print("Resultado:", result)

    # 6) Unsafe deserialization com pickle.loads em dados do arquivo
    if "session_pickle" in payload:
        p = payload["session_pickle"].encode("latin1")  # supõe que foi serializado e armazenado
        session = pickle.loads(p)  # **** VULNERÁVEL ****
        print("Session desserializada:", session)

def create_temp_file(user: str, content: str):
    # 7) Cria arquivo temporário com nome previsível e permissões inseguras
    fname = f"/tmp/{user}_session.txt"  # nome previsível
    with open(fname, "w") as f:
        f.write(content)
    # Permissões 777 (inseguro)
    os.chmod(fname, 0o777)
    print("Arquivo temporário criado:", fname)

def run_system_task(command: str):
    # 8) Executa comando com shell=True e input direto
    print("Rodando comando:", command)
    subprocess.run(command, shell=True)  # **** VULNERÁVEL ****

if __name__ == "__main__":
    # fluxinho demo (não use em produção)
    save_user("alice", "password123")
    print("Autenticado alice:", authenticate("alice", "password123"))

    # Se existir um arquivo input.json, processa
    if os.path.exists("input.json"):
        process_input_file("input.json")

    create_temp_file("alice", "dados de sessão sensíveis")
    # Exemplo de comando (não forneça input externo em produção)
    run_system_task("ls -la /tmp")
