# Camada 7 — Aplicação

## O que é?

A **Camada de Aplicação** é a mais próxima do usuário final. Ela fornece interfaces e protocolos que as aplicações usam para se comunicar pela rede. É aqui que residem os protocolos que você usa todos os dias: HTTP, DNS, FTP, SMTP, etc.

## Responsabilidades

- Interface direta com o software do usuário
- Protocolos de alto nível (HTTP, DNS, FTP, SMTP)
- Autenticação e autorização a nível de aplicação
- Serviços de diretório (LDAP)
- Transferência de arquivos, e-mail, navegação web

## Protocolos principais

| Protocolo | Porta | Descrição |
|---|---|---|
| HTTP/HTTPS | 80/443 | Navegação web |
| DNS | 53 | Resolução de nomes |
| FTP/SFTP | 21/22 | Transferência de arquivos |
| SMTP | 25/587 | Envio de e-mail |
| IMAP/POP3 | 993/995 | Recebimento de e-mail |
| SSH | 22 | Acesso remoto seguro |
| DHCP | 67/68 | Atribuição dinâmica de IP |
| SNMP | 161 | Monitoramento de rede |

## Exemplo de código — HTTP, DNS, SMTP e mais

```python
# Python — Cliente HTTP com requests
import requests

# GET — busca de recurso
response = requests.get(
    "https://jsonplaceholder.typicode.com/users/1",
    headers={"Accept": "application/json"},
    timeout=10
)
print(f"Status  : {response.status_code}")
print(f"Servidor: {response.headers.get('Server', 'N/A')}")
dados = response.json()
print(f"Usuário : {dados['name']} <{dados['email']}>")

# POST — envio de dados
novo = requests.post(
    "https://jsonplaceholder.typicode.com/posts",
    json={"title": "Camada 7", "body": "OSI Application Layer", "userId": 1}
)
print(f"Criado  : status {novo.status_code} — ID: {novo.json()['id']}")
```

```python
# Python — Resolução DNS (protocolo da Camada 7)
import socket

# Resolução simples
host = "www.google.com"
ip = socket.gethostbyname(host)
print(f"{host} -> {ip}")

# Resolução reversa (IP -> hostname)
try:
    hostname = socket.gethostbyaddr("8.8.8.8")
    print(f"8.8.8.8 -> {hostname[0]}")
except socket.herror:
    print("Resolução reversa não disponível")

# Obtendo todas as interfaces do host
infos = socket.getaddrinfo("github.com", 443)
for info in infos[:3]:
    familia, tipo, proto, nome, endereco = info
    print(f"  {endereco[0]:40s} porta {endereco[1]}")
```

```python
# Python — Servidor HTTP simples do zero
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/status':
            resposta = {
                "status": "ok",
                "camada": 7,
                "protocolo": "HTTP/1.1",
                "modelo": "OSI"
            }
            corpo = json.dumps(resposta, indent=2).encode()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(corpo))
            self.end_headers()
            self.wfile.write(corpo)
        else:
            self.send_error(404, "Rota não encontrada")
    
    def log_message(self, format, *args):
        print(f"  [{self.client_address[0]}] {format % args}")

# Iniciando o servidor
# servidor = HTTPServer(('0.0.0.0', 8080), Handler)
# print("Servidor HTTP na porta 8080")
# servidor.serve_forever()
```

```python
# Python — API REST com Flask
from flask import Flask, jsonify, request

app = Flask(__name__)
banco = {}

@app.route('/usuarios', methods=['GET'])
def listar():
    return jsonify(list(banco.values()))

@app.route('/usuarios', methods=['POST'])
def criar():
    dados = request.json
    uid = len(banco) + 1
    banco[uid] = {"id": uid, **dados}
    return jsonify(banco[uid]), 201

@app.route('/usuarios/<int:uid>', methods=['GET'])
def buscar(uid):
    usuario = banco.get(uid)
    if not usuario:
        return jsonify({"erro": "não encontrado"}), 404
    return jsonify(usuario)

@app.route('/usuarios/<int:uid>', methods=['DELETE'])
def deletar(uid):
    banco.pop(uid, None)
    return '', 204

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
```

```python
# Python — Envio de e-mail via SMTP
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(destinatario: str, assunto: str, corpo: str):
    msg = MIMEMultipart()
    msg['From']    = "remetente@exemplo.com"
    msg['To']      = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain', 'utf-8'))
    
    # Conecta ao servidor SMTP (protocolo da Camada 7)
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()  # ativa TLS (Camada 6)
        smtp.login("usuario@gmail.com", "senha_app")
        smtp.sendmail(msg['From'], destinatario, msg.as_string())
        print(f"E-mail enviado para {destinatario}")

# enviar_email("destino@exemplo.com", "Teste OSI", "Camada 7 funcionando!")
```

```python
# Python — WebSocket (comunicação bidirecional na Camada 7)
import asyncio
import websockets

async def servidor_ws(websocket, path):
    print(f"Cliente conectado: {websocket.remote_address}")
    async for mensagem in websocket:
        print(f"Recebido: {mensagem}")
        await websocket.send(f"Echo: {mensagem}")

async def cliente_ws():
    async with websockets.connect("ws://localhost:8765") as ws:
        await ws.send("Olá via WebSocket!")
        resposta = await ws.recv()
        print(f"Resposta: {resposta}")

# start_server = websockets.serve(servidor_ws, "localhost", 8765)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()
```

## Curiosidade

> Quando você digita `google.com` no navegador, a Camada 7 inicia uma consulta **DNS** para descobrir o IP, depois realiza um **TLS Handshake** (Camada 6) e, por fim, envia uma requisição **HTTP GET**. Você está usando ao mesmo tempo dois protocolos da Camada de Aplicação — e tudo isso acontece em milissegundos!

---

## Vulnerabilidades e Riscos

### Principais ameaças

| Ataque / Risco | Descrição |
|---|---|
| **SQL Injection** | Inserir código SQL malicioso em campos de entrada para manipular o banco de dados |
| **Cross-Site Scripting (XSS)** | Injetar scripts maliciosos em páginas web visualizadas por outros usuários |
| **DNS Spoofing / Cache Poisoning** | Envenenar o cache DNS para redirecionar domínios a IPs maliciosos |
| **HTTP Request Smuggling** | Explorar ambiguidades entre front-end e back-end para injetar requisições |
| **Directory Traversal** | Usar `../` para acessar arquivos fora do diretório permitido |
| **SSRF (Server-Side Request Forgery)** | Forçar o servidor a fazer requisições a serviços internos |
| **Command Injection** | Injetar comandos do SO via parâmetros da aplicação |
| **DNS Tunneling** | Usar consultas DNS para exfiltrar dados ou criar canal C2 encoberto |
| **Open Redirect** | Redirecionar usuários a URLs externas maliciosas via parâmetro manipulado |
| **HTTP Flood (Layer 7 DDoS)** | Inundar o servidor com requisições HTTP legítimas (difícil de bloquear) |

### Demonstração — As principais vulnerabilidades e como mitigá-las

```python
# Python — SQL Injection: vulnerável vs. seguro
import sqlite3

# Configuração do banco de demonstração
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE usuarios (id INTEGER, nome TEXT, senha TEXT)")
conn.execute("INSERT INTO usuarios VALUES (1, 'alice', 'senha123')")
conn.execute("INSERT INTO usuarios VALUES (2, 'admin', 'adminpass')")
conn.commit()

# ❌ VULNERÁVEL — concatenação direta de input na query
def login_vulneravel(nome: str, senha: str):
    query = f"SELECT * FROM usuarios WHERE nome='{nome}' AND senha='{senha}'"
    print(f"Query: {query}")
    return conn.execute(query).fetchone()

# Ataque clássico: ' OR '1'='1 — bypassa a autenticação completamente
usuario = login_vulneravel("admin' --", "qualquer_coisa")
print(f"❌ Login vulnerável retornou: {usuario}")

# ✅ SEGURO — parametrização com placeholders
def login_seguro(nome: str, senha: str):
    query = "SELECT * FROM usuarios WHERE nome=? AND senha=?"
    # O driver trata os parâmetros como dados, nunca como código SQL
    return conn.execute(query, (nome, senha)).fetchone()

usuario = login_seguro("admin' --", "qualquer_coisa")
print(f"✅ Login seguro retornou: {usuario}")  # None — ataque bloqueado

usuario = login_seguro("admin", "adminpass")
print(f"✅ Login legítimo: {usuario}")
```

```python
# Python — Command Injection: vulnerável vs. seguro
import subprocess
import shlex

# ❌ VULNERÁVEL — passa input diretamente ao shell
def ping_vulneravel(host: str) -> str:
    cmd = f"ping -c 1 {host}"
    print(f"Executando: {cmd}")
    # Se host = "google.com; rm -rf /tmp/teste" — executa dois comandos!
    resultado = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return resultado.stdout

# Demonstração do payload
host_malicioso = "google.com; echo 'INJECAO EXECUTADA'"
# ping_vulneravel(host_malicioso)  # executaria o echo!

# ✅ SEGURO — usa lista de argumentos (sem shell=True)
def ping_seguro(host: str) -> str:
    # Valida o input antes
    import re
    if not re.match(r'^[a-zA-Z0-9.\-]+$', host):
        raise ValueError(f"Host inválido: {host}")
    
    resultado = subprocess.run(
        ["ping", "-c", "1", host],  # lista — sem interpretação de shell
        capture_output=True,
        text=True,
        timeout=5
    )
    return resultado.stdout

try:
    ping_seguro("google.com; echo INJECAO")
except ValueError as e:
    print(f"✅ Injection bloqueada: {e}")
```

```python
# Python — Directory Traversal: vulnerável vs. seguro
import os
from pathlib import Path

BASE_DIR = Path("/var/www/arquivos")

# ❌ VULNERÁVEL — usa o path diretamente sem validação
def ler_arquivo_vulneravel(nome: str) -> str:
    caminho = BASE_DIR / nome
    # nome = "../../../../etc/passwd" -> leria /etc/passwd!
    with open(caminho) as f:
        return f.read()

# ✅ SEGURO — verifica que o path resolvido está dentro do diretório base
def ler_arquivo_seguro(nome: str) -> str:
    # resolve() normaliza ../.. e symlinks
    caminho = (BASE_DIR / nome).resolve()
    
    # Garante que o arquivo está dentro do diretório permitido
    if not str(caminho).startswith(str(BASE_DIR.resolve())):
        raise PermissionError(
            f"Acesso negado: '{nome}' tenta sair do diretório base"
        )
    
    if not caminho.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {nome}")
    
    with open(caminho) as f:
        return f.read()

try:
    ler_arquivo_seguro("../../../../etc/passwd")
except PermissionError as e:
    print(f"✅ Traversal bloqueado: {e}")
```

```python
# Python — DNS Spoofing: simulando e detectando cache poisoning
import socket
import hashlib
import time

class CacheDNSSeguro:
    """
    Cache DNS com verificação de integridade.
    Simula como um resolver poderia detectar respostas manipuladas.
    """
    def __init__(self):
        self._cache: dict = {}
        self._hashes_conhecidos: dict = {}
    
    def resolver(self, dominio: str) -> str:
        """Resolve um domínio e detecta mudanças suspeitas"""
        if dominio in self._cache:
            ip_cache, timestamp = self._cache[dominio]
            # Verifica se o cache ainda é válido (TTL de 5 min)
            if time.time() - timestamp < 300:
                return ip_cache
        
        # Resolve o domínio
        ip = socket.gethostbyname(dominio)
        
        # Detecta mudança inesperada no IP (possível cache poisoning)
        hash_atual = hashlib.sha256(f"{dominio}:{ip}".encode()).hexdigest()
        if dominio in self._hashes_conhecidos:
            if hash_atual != self._hashes_conhecidos[dominio]:
                print(f"⚠️  ALERTA: IP de '{dominio}' mudou! "
                      f"Possível DNS Spoofing.")
        
        self._cache[dominio] = (ip, time.time())
        self._hashes_conhecidos[dominio] = hash_atual
        return ip

cache = CacheDNSSeguro()
try:
    ip = cache.resolver("github.com")
    print(f"✅ github.com -> {ip}")
except Exception as e:
    print(f"Erro na resolução: {e}")
```

```python
# Python — SSRF: vulnerável vs. seguro
import ipaddress
import urllib.parse
import requests

# Lista de faixas privadas que não devem ser acessadas pelo servidor
REDES_PRIVADAS = [
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv4Network("127.0.0.0/8"),
    ipaddress.IPv4Network("169.254.0.0/16"),  # link-local
    ipaddress.IPv4Network("0.0.0.0/8"),
]

def ip_e_privado(ip_str: str) -> bool:
    try:
        ip = ipaddress.IPv4Address(ip_str)
        return any(ip in rede for rede in REDES_PRIVADAS)
    except ValueError:
        return False

# ✅ Fetch de URL seguro (previne SSRF)
def fetch_seguro(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    
    # Apenas HTTP/HTTPS
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Scheme não permitido: {parsed.scheme}")
    
    # Resolve o IP e verifica se é privado
    try:
        ip = socket.gethostbyname(parsed.hostname)
    except socket.gaierror:
        raise ValueError(f"Hostname não resolvível: {parsed.hostname}")
    
    if ip_e_privado(ip):
        raise PermissionError(
            f"SSRF bloqueado: '{parsed.hostname}' resolve para IP privado {ip}"
        )
    
    response = requests.get(url, timeout=5, allow_redirects=False)
    return response.text[:200]

# Testando
try:
    fetch_seguro("http://192.168.1.1/admin")
except PermissionError as e:
    print(f"✅ SSRF bloqueado: {e}")

try:
    fetch_seguro("http://localhost:6379")  # tentativa de acessar Redis interno
except PermissionError as e:
    print(f"✅ SSRF bloqueado: {e}")
```

```python
# Python — Rate limiting para prevenir HTTP Flood e brute force
import time
from collections import defaultdict
from functools import wraps

class RateLimiter:
    def __init__(self, max_requisicoes: int, janela_segundos: int):
        self.max_req = max_requisicoes
        self.janela  = janela_segundos
        self._historico: dict = defaultdict(list)
    
    def verificar(self, identificador: str) -> bool:
        """Retorna True se a requisição deve ser bloqueada"""
        agora = time.time()
        historico = self._historico[identificador]
        
        # Remove timestamps fora da janela
        self._historico[identificador] = [
            t for t in historico if agora - t < self.janela
        ]
        
        if len(self._historico[identificador]) >= self.max_req:
            return True  # bloqueado
        
        self._historico[identificador].append(agora)
        return False  # permitido

# Exemplo de uso em uma rota Flask
limiter = RateLimiter(max_requisicoes=10, janela_segundos=60)

def rota_protegida(ip_cliente: str, endpoint: str):
    chave = f"{ip_cliente}:{endpoint}"
    if limiter.verificar(chave):
        return {"erro": "Rate limit excedido. Tente novamente em 60s."}, 429
    return {"dados": "resposta normal"}, 200

# Simulação de ataque e resposta
ip_atacante = "1.2.3.4"
for i in range(15):
    resposta, status = rota_protegida(ip_atacante, "/api/login")
    simbolo = "✅" if status == 200 else "🚫"
    print(f"  Req {i+1:2d}: {simbolo} {status} — {resposta}")
```

### Mitigações

- **Parametrização de queries** — nunca concatenar input do usuário em SQL
- **Validação e sanitização de input** — whitelist de caracteres permitidos por campo
- **WAF (Web Application Firewall)** — bloqueia padrões de SQLi, XSS, traversal
- **DNSSEC** — assina digitalmente respostas DNS para prevenir spoofing
- **Rate limiting** por IP e por conta — protege contra brute force e floods
- **Content Security Policy (CSP)** — restringe origens de scripts para mitigar XSS
- **SSRF protection** — bloquear resoluções para IPs privados no servidor
- **Princípio do mínimo privilégio** — usuário do banco sem permissão de DROP/ALTER