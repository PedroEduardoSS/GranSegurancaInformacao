# Camada 5 — Sessão

## O que é?

A **Camada de Sessão** gerencia o estabelecimento, manutenção e encerramento de **sessões** entre aplicações. Uma sessão é uma conexão lógica de mais alto nível que pode sobreviver a interrupções temporárias da rede.

## Responsabilidades

- Estabelecimento, gerenciamento e encerramento de sessões
- Sincronização — pontos de verificação (checkpoints) para retomada
- Controle de diálogo — half-duplex ou full-duplex
- Autenticação e autorização de sessão
- Recuperação de sessões após falhas

## Protocolos e tecnologias

| Protocolo | Uso |
|---|---|
| NetBIOS | Sessões em redes Windows |
| RPC | Chamadas remotas de procedimento |
| PPTP | VPN com gerenciamento de sessão |
| SIP | Sessões de voz/vídeo (VoIP) |
| TLS/SSL | Sessões seguras (negociação inicial) |

## Exemplo de código — Gerenciamento de Sessões

```python
# Python — Sessões HTTP com requests (persistência de conexão)
import requests

# Session mantém cookies, headers e conexão TCP reutilizada (keep-alive)
session = requests.Session()

# Configurando headers padrão da sessão
session.headers.update({
    'User-Agent': 'MeuApp/1.0',
    'Accept': 'application/json'
})

# A sessão reutiliza a conexão TCP entre requisições
response1 = session.get('https://httpbin.org/cookies/set/sessao_id/abc123')
response2 = session.get('https://httpbin.org/cookies')

print(f"Cookies da sessão: {session.cookies.get_dict()}")
print(f"Resposta: {response2.json()}")

session.close()
```

```python
# Python — Gerenciador de sessão com checkpoint (recovery)
import json
import os
import time
from datetime import datetime

class GerenciadorSessao:
    """Simula a Camada de Sessão: cria, mantém e restaura sessões"""
    
    def __init__(self, sessao_id: str):
        self.sessao_id = sessao_id
        self.checkpoint_file = f"sessao_{sessao_id}.json"
        self.dados = self._restaurar_sessao()
    
    def _restaurar_sessao(self) -> dict:
        """Restaura sessão de um checkpoint (recovery após falha)"""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, 'r') as f:
                dados = json.load(f)
            print(f"Sessão {self.sessao_id} restaurada do checkpoint!")
            return dados
        return {
            "id": self.sessao_id,
            "criada_em": datetime.now().isoformat(),
            "ultimo_checkpoint": None,
            "progresso": 0
        }
    
    def salvar_checkpoint(self):
        """Salva ponto de verificação para recuperação"""
        self.dados["ultimo_checkpoint"] = datetime.now().isoformat()
        with open(self.checkpoint_file, 'w') as f:
            json.dump(self.dados, f, indent=2)
        print(f"Checkpoint salvo — progresso: {self.dados['progresso']}%")
    
    def atualizar_progresso(self, progresso: int):
        self.dados["progresso"] = progresso
    
    def encerrar(self):
        """Encerramento gracioso da sessão"""
        if os.path.exists(self.checkpoint_file):
            os.remove(self.checkpoint_file)
        print(f"Sessão {self.sessao_id} encerrada corretamente.")

# Uso
sessao = GerenciadorSessao("usuario_42")
sessao.atualizar_progresso(30)
sessao.salvar_checkpoint()
sessao.atualizar_progresso(60)
sessao.salvar_checkpoint()
sessao.encerrar()
```

```python
# Python — Sessão com autenticação via token
import secrets
import time

class SessaoAutenticada:
    _sessoes_ativas: dict = {}
    
    @classmethod
    def criar(cls, usuario: str, senha: str) -> str:
        if usuario == "admin" and senha == "1234":
            token = secrets.token_hex(32)
            cls._sessoes_ativas[token] = {
                "usuario": usuario,
                "criada_em": time.time(),
                "expira_em": time.time() + 3600  # 1 hora
            }
            print(f"Sessão criada para '{usuario}'")
            return token
        raise PermissionError("Credenciais inválidas")
    
    @classmethod
    def validar(cls, token: str) -> dict:
        sessao = cls._sessoes_ativas.get(token)
        if not sessao:
            raise ValueError("Sessão não encontrada")
        if time.time() > sessao["expira_em"]:
            del cls._sessoes_ativas[token]
            raise TimeoutError("Sessão expirada")
        return sessao
    
    @classmethod
    def encerrar(cls, token: str):
        cls._sessoes_ativas.pop(token, None)
        print("Sessão encerrada (logout)")

token = SessaoAutenticada.criar("admin", "1234")
info  = SessaoAutenticada.validar(token)
print(f"Sessão válida para: {info['usuario']}")
SessaoAutenticada.encerrar(token)
```

## Curiosidade

> Quando você assiste a um vídeo no YouTube e a internet cai brevemente, o player consegue retomar de onde parou — isso é gerenciamento de sessão em ação. A Camada de Sessão define como e quando retomar uma comunicação interrompida.

---

## Vulnerabilidades e Riscos

### Principais ameaças

| Ataque / Risco | Descrição |
|---|---|
| **Session Hijacking** | Roubar ou forjar o token/ID de sessão para assumir a identidade do usuário |
| **Session Fixation** | Forçar o usuário a usar um session ID conhecido pelo atacante |
| **Replay Attack** | Capturar e reenviar tokens de sessão válidos para se autenticar |
| **Brute Force de Session ID** | Adivinhar IDs de sessão quando gerados com entropia baixa |
| **Cross-Site Request Forgery (CSRF)** | Explorar a sessão autenticada do usuário para executar ações não autorizadas |
| **Man-in-the-Middle** | Interceptar sessões não criptografadas para capturar tokens |
| **Session Timeout ausente** | Sessões sem expiração ficam válidas indefinidamente após logout |
| **Concurrent Sessions** | Ausência de controle permite múltiplas sessões ativas para o mesmo usuário |

### Demonstração — Session Hijacking e boas práticas

```python
# Python — Gerando tokens de sessão seguros vs. inseguros
import secrets
import hashlib
import time
import random
import string

# ❌ MAU EXEMPLO — Session ID previsível (fácil de adivinhar)
def session_id_inseguro(usuario: str) -> str:
    timestamp = int(time.time())
    return f"{usuario}_{timestamp}"  # completamente previsível

# ❌ MAU EXEMPLO — ID baseado em random() padrão (não criptográfico)
def session_id_fraco() -> str:
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(16))  # apenas 16 chars, não-criptográfico

# ✅ BOM EXEMPLO — Token criptograficamente seguro
def session_id_seguro() -> str:
    return secrets.token_hex(32)  # 256 bits de entropia — imprevisível

# Comparação
print("Session IDs inseguros:")
print(f"  Previsível : {session_id_inseguro('alice')}")
print(f"  Fraco      : {session_id_fraco()}")
print(f"\nSession ID seguro:")
print(f"  Seguro     : {session_id_seguro()}")
```

```python
# Python — Demonstrando Session Fixation e como prevenir
# Na Session Fixation, o atacante define um session ID antes do login.
# Se o servidor reutilizar esse ID após autenticação, o atacante pode hijack a sessão.

class SessaoVulneravel:
    """❌ VULNERÁVEL a Session Fixation — reutiliza o ID após login"""
    _sessoes: dict = {}
    
    @classmethod
    def criar(cls) -> str:
        sid = secrets.token_hex(16)
        cls._sessoes[sid] = {"autenticado": False, "usuario": None}
        return sid
    
    @classmethod
    def autenticar(cls, sid: str, usuario: str):
        if sid in cls._sessoes:
            # ❌ ERRO: reutiliza o mesmo ID — atacante que conhecia o ID pré-auth
            # agora tem acesso à sessão autenticada
            cls._sessoes[sid]["autenticado"] = True
            cls._sessoes[sid]["usuario"] = usuario
            return sid
        raise ValueError("Sessão inválida")


class SessaoSegura:
    """✅ SEGURA — regenera o session ID após autenticação"""
    _sessoes: dict = {}
    
    @classmethod
    def criar(cls) -> str:
        sid = secrets.token_hex(16)
        cls._sessoes[sid] = {"autenticado": False, "usuario": None}
        return sid
    
    @classmethod
    def autenticar(cls, sid_antigo: str, usuario: str) -> str:
        if sid_antigo not in cls._sessoes:
            raise ValueError("Sessão inválida")
        
        # ✅ Invalida o ID antigo e cria um novo após autenticação
        del cls._sessoes[sid_antigo]
        novo_sid = secrets.token_hex(32)  # novo token com mais entropia
        cls._sessoes[novo_sid] = {
            "autenticado": True,
            "usuario": usuario,
            "criada_em": time.time(),
            "expira_em": time.time() + 3600,
            "ip_origem": None  # poderia vincular ao IP do cliente
        }
        print(f"Sessão regenerada após login. Novo ID: {novo_sid[:16]}...")
        return novo_sid
    
    @classmethod
    def validar(cls, sid: str) -> dict:
        sessao = cls._sessoes.get(sid)
        if not sessao or not sessao["autenticado"]:
            raise PermissionError("Sessão inválida ou não autenticada")
        if time.time() > sessao["expira_em"]:
            del cls._sessoes[sid]
            raise TimeoutError("Sessão expirada")
        return sessao
    
    @classmethod
    def encerrar(cls, sid: str):
        """Invalidação explícita no logout"""
        if sid in cls._sessoes:
            del cls._sessoes[sid]
            print("Sessão invalidada com sucesso (logout seguro)")
```

```python
# Python — Detectando uso anômalo de sessão (mudança de IP / User-Agent)
import hashlib

class SessaoComDeteccaoAnomalia:
    _sessoes: dict = {}
    
    @classmethod
    def criar(cls, usuario: str, ip: str, user_agent: str) -> str:
        sid = secrets.token_hex(32)
        # Cria uma impressão digital da sessão no momento do login
        fingerprint = hashlib.sha256(f"{ip}:{user_agent}".encode()).hexdigest()
        cls._sessoes[sid] = {
            "usuario"    : usuario,
            "fingerprint": fingerprint,
            "criada_em"  : time.time(),
            "expira_em"  : time.time() + 3600,
            "ultimo_uso" : time.time()
        }
        return sid
    
    @classmethod
    def validar(cls, sid: str, ip: str, user_agent: str) -> dict:
        sessao = cls._sessoes.get(sid)
        if not sessao:
            raise ValueError("Sessão não encontrada")
        
        if time.time() > sessao["expira_em"]:
            del cls._sessoes[sid]
            raise TimeoutError("Sessão expirada")
        
        # Verifica se a sessão está sendo usada do mesmo contexto
        fingerprint_atual = hashlib.sha256(f"{ip}:{user_agent}".encode()).hexdigest()
        if fingerprint_atual != sessao["fingerprint"]:
            # Possível session hijacking — contexto mudou
            del cls._sessoes[sid]  # invalida imediatamente
            raise SecurityWarning(
                f"⚠️  Anomalia detectada! Sessão de '{sessao['usuario']}' "
                f"invalidada por mudança de contexto."
            )
        
        sessao["ultimo_uso"] = time.time()
        return sessao

# Teste
try:
    sid = SessaoComDeteccaoAnomalia.criar("alice", "192.168.1.10", "Mozilla/5.0")
    sessao = SessaoComDeteccaoAnomalia.validar(sid, "192.168.1.10", "Mozilla/5.0")
    print(f"✅ Sessão válida para: {sessao['usuario']}")
    
    # Simula uso de outro IP (possível hijacking)
    sessao = SessaoComDeteccaoAnomalia.validar(sid, "10.0.0.99", "curl/7.68")
except Exception as e:
    print(str(e))
```

### Mitigações

- **Regenerar session ID após login** — previne Session Fixation
- **Tokens criptograficamente seguros** — usar `secrets.token_hex(32)` ou equivalente
- **Expiração de sessão** — timeout de inatividade + tempo máximo absoluto
- **Vincular sessão ao IP/User-Agent** — detectar hijacking por mudança de contexto
- **HTTPS obrigatório** — previne interceptação de tokens por MitM
- **Cookie com flags `HttpOnly` e `Secure`** — impede acesso via JavaScript e transmissão em HTTP claro
- **Invalidação explícita no logout** — garantir que o token seja deletado no servidor