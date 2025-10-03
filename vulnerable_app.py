import sqlite3
import subprocess
import pickle
from typing import Any

DB_PATH = "test.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, bio TEXT)")
    cur.execute("INSERT OR IGNORE INTO users (id, username, bio) VALUES (1, 'alice', 'admin')")
    conn.commit()
    conn.close()

# 1) SQL Injection: consulta construída por concatenação/interpolação
def find_user_by_name(username: str):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # *** VULNERABLE: string formatting / f-string used directly em query ***
    query = f"SELECT id, username, bio FROM users WHERE username = '{username}'"
    cur.execute(query)
    result = cur.fetchall()
    conn.close()
    return result

# 2) Command Injection: usando subprocess com shell=True e input direto do usuário
def ping_host(host: str):
    # *** VULNERABLE: shell=True com interpolação direta ***
    cmd = f"ping -c 1 {host}"
    subprocess.run(cmd, shell=True, check=False)

# 3) Unsafe deserialization: carregando pickle de fonte não confiável
def load_session(data: bytes) -> Any:
    # *** VULNERABLE: deserialização sem validação ***
    obj = pickle.loads(data)
    return obj

if __name__ == "__main__":
    init_db()
    # exemplos de chamadas (apenas para fins de teste local)
    print(find_user_by_name("alice"))
    # ping_host("127.0.0.1")  # descomente só em ambiente de teste
    # load_session(b"")       # exemplo: forneça um payload pickle gerado localmente para testar deteção

