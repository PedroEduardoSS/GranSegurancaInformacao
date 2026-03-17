# Camada 6 — Apresentação

## O que é?

A **Camada de Apresentação** é responsável pela **tradução, codificação, compressão e criptografia** dos dados. Ela garante que os dados enviados por uma aplicação possam ser compreendidos pela aplicação receptora, independente de diferenças de formato ou representação.

## Responsabilidades

- Tradução de formatos (ex: ASCII ↔ EBCDIC, UTF-8 ↔ UTF-16)
- Serialização e desserialização (JSON, XML, Protobuf)
- Compressão de dados (gzip, deflate)
- Criptografia e descriptografia (TLS/SSL)
- Codificação (Base64, encoding de caracteres)

## Formatos e padrões

| Formato/Padrão | Uso |
|---|---|
| JSON / XML | Serialização de dados |
| Base64 | Codificação binário → texto |
| gzip / zlib | Compressão |
| TLS/SSL | Criptografia |
| JPEG, PNG, MP4 | Codificação de mídia |
| ASN.1 | Notação de estruturas de dados |

## Exemplo de código — Serialização, Compressão e Criptografia

```python
# Python — Serialização de dados (JSON)
import json
from dataclasses import dataclass, asdict

@dataclass
class Usuario:
    nome: str
    idade: int
    email: str

usuario = Usuario("Alice", 30, "alice@exemplo.com")

# Serializando para JSON (texto — interoperável entre linguagens)
json_str = json.dumps(asdict(usuario), ensure_ascii=False, indent=2)
print(f"JSON:\n{json_str}")

# Desserializando
dados = json.loads(json_str)
recuperado = Usuario(**dados)
print(f"Recuperado: {recuperado}")
```

```python
# Python — Compressão de dados (gzip / zlib)
import gzip
import zlib

dados = b"Camada de Apresentacao: responsavel por compressao de dados! " * 100
print(f"Tamanho original : {len(dados):,} bytes")

# Compressão gzip
comprimido_gzip = gzip.compress(dados, compresslevel=9)
print(f"Gzip comprimido  : {len(comprimido_gzip):,} bytes "
      f"({100 * len(comprimido_gzip) / len(dados):.1f}%)")

# Compressão zlib
comprimido_zlib = zlib.compress(dados, level=9)
print(f"Zlib comprimido  : {len(comprimido_zlib):,} bytes "
      f"({100 * len(comprimido_zlib) / len(dados):.1f}%)")

# Descomprimindo e verificando integridade
restaurado = gzip.decompress(comprimido_gzip)
assert restaurado == dados
print("Dados restaurados com sucesso!")
```

```python
# Python — Codificação Base64 (binário → texto ASCII)
import base64

# Base64 é usado em: JWT tokens, imagens em HTML, anexos de e-mail
mensagem = b"Dados confidenciais para transmissao segura"

encoded = base64.b64encode(mensagem)
print(f"Original : {mensagem.decode()}")
print(f"Base64   : {encoded.decode()}")

decoded = base64.b64decode(encoded)
assert decoded == mensagem
print("Base64 decode OK")

# Base64 URL-safe (usado em JWT)
url_safe = base64.urlsafe_b64encode(mensagem)
print(f"URL-safe : {url_safe.decode()}")
```

```python
# Python — Criptografia simétrica com Fernet (AES-128)
from cryptography.fernet import Fernet

# Geração de chave (deve ser armazenada com segurança)
chave = Fernet.generate_key()
cipher = Fernet(chave)

mensagem = b"Dados confidenciais da Camada de Apresentacao"

# Criptografando
cifrado = cipher.encrypt(mensagem)
print(f"Cifrado : {cifrado[:60]}...")

# Descriptografando
decifrado = cipher.decrypt(cifrado)
print(f"Original: {decifrado.decode()}")
```

```python
# Python — Encoding de caracteres (tradução entre formatos)
texto = "Olá, rede! 🌐"

# Diferentes encodings — a Camada de Apresentação trata disso
for encoding in ['utf-8', 'utf-16', 'latin-1']:
    try:
        encoded = texto.encode(encoding)
        decoded = encoded.decode(encoding)
        print(f"{encoding:10s}: {len(encoded)} bytes — OK")
    except UnicodeEncodeError as e:
        print(f"{encoding:10s}: falhou ({e})")
```

## Curiosidade

> O **HTTPS** usa TLS, que opera nessa camada, para criptografar a comunicação. Antes de qualquer dado da aplicação trafegar, ocorre o **TLS Handshake**, onde cliente e servidor negociam algoritmos de criptografia e trocam chaves — tudo transparente para o usuário.

---

## Vulnerabilidades e Riscos

### Principais ameaças

| Ataque / Risco | Descrição |
|---|---|
| **SSL/TLS Downgrade** | Forçar o uso de versões antigas (SSLv3, TLS 1.0) com vulnerabilidades conhecidas |
| **POODLE** | Exploita o SSLv3 para descriptografar dados via padding oracle |
| **BEAST** | Ataque contra TLS 1.0 usando vulnerabilidade no modo CBC |
| **CRIME / BREACH** | Exploita compressão + criptografia para vazar dados via análise de tamanho |
| **Deserialização insegura** | Objetos serializados maliciosos podem executar código arbitrário |
| **Padding Oracle** | Manipulação do padding de blocos cifrados para recuperar plaintext |
| **Certificate Spoofing** | Usar certificados TLS falsos ou auto-assinados em ataques MitM |
| **Weak Cipher Suites** | Uso de algoritmos fracos como RC4, DES, MD5 para integridade |
| **XXE Injection** | Entidades externas em XML para ler arquivos do servidor ou SSRF |

### Demonstração — Deserialização insegura, TLS e criptografia segura

```python
# Python — Deserialização insegura com Pickle (vulnerabilidade crítica)
import pickle
import os
import subprocess

# ❌ PERIGO: Pickle pode executar código arbitrário ao desserializar
class PayloadMalicioso:
    """
    Esta classe demonstra por que NUNCA se deve desserializar
    dados pickle de fontes não confiáveis.
    """
    def __reduce__(self):
        # __reduce__ é chamado automaticamente pelo pickle ao desserializar
        # Isso poderia executar QUALQUER comando no sistema
        cmd = "echo 'Código arbitrário executado via Pickle!'"
        return (subprocess.check_output, ([cmd], {"shell": True}))

# Serializa o payload malicioso
payload = pickle.dumps(PayloadMalicioso())
print(f"Payload malicioso serializado: {len(payload)} bytes")
print(f"Primeiros bytes: {payload[:20]}")

# ❌ Em um servidor vulnerável, isso executaria o código:
# resultado = pickle.loads(payload)  # NUNCA faça isso com dados externos!
print("\n⚠️  NUNCA use pickle.loads() com dados de fontes não confiáveis!")
```

```python
# Python — Alternativas seguras à deserialização
import json
import base64
from dataclasses import dataclass, asdict

@dataclass
class DadosUsuario:
    nome: str
    idade: int
    email: str

usuario = DadosUsuario("Alice", 30, "alice@exemplo.com")

# ✅ JSON — seguro para dados não confiáveis (não executa código)
json_str = json.dumps(asdict(usuario))
recuperado = DadosUsuario(**json.loads(json_str))
print(f"✅ JSON seguro: {recuperado}")

# ✅ Validação rigorosa antes de desserializar
def desserializar_seguro(dados_json: str, campos_esperados: set) -> dict:
    obj = json.loads(dados_json)
    
    # Verifica que apenas campos esperados estão presentes
    campos_recebidos = set(obj.keys())
    campos_inesperados = campos_recebidos - campos_esperados
    if campos_inesperados:
        raise ValueError(f"Campos não permitidos: {campos_inesperados}")
    
    # Valida tipos
    for campo, valor in obj.items():
        if not isinstance(valor, (str, int, float, bool, type(None))):
            raise TypeError(f"Tipo não permitido no campo '{campo}': {type(valor)}")
    
    return obj

resultado = desserializar_seguro(json_str, {"nome", "idade", "email"})
print(f"✅ Desserialização validada: {resultado}")
```

```python
# Python — Verificando a força de uma configuração TLS
import ssl
import socket

def auditar_tls(host: str, porta: int = 443):
    """Analisa o certificado e as capacidades TLS de um servidor"""
    
    contexto = ssl.create_default_context()
    
    try:
        with socket.create_connection((host, porta), timeout=5) as sock:
            with contexto.wrap_socket(sock, server_hostname=host) as ssock:
                versao       = ssock.version()
                cipher_info  = ssock.cipher()
                cert         = ssock.getpeercert()
                
                print(f"Host        : {host}:{porta}")
                print(f"Versão TLS  : {versao}")
                print(f"Cipher      : {cipher_info[0]}")
                print(f"Bits        : {cipher_info[2]}")
                
                # Avalia a segurança
                versoes_fracas = {"SSLv2", "SSLv3", "TLSv1", "TLSv1.1"}
                if versao in versoes_fracas:
                    print(f"⚠️  ALERTA: versão {versao} é obsoleta e insegura!")
                else:
                    print(f"✅ Versão TLS adequada")
                
                cifras_fracas = {"RC4", "DES", "3DES", "NULL", "EXPORT"}
                nome_cifra = cipher_info[0].upper()
                for fraca in cifras_fracas:
                    if fraca in nome_cifra:
                        print(f"⚠️  ALERTA: cipher fraco detectado: {cipher_info[0]}")
                        break
                else:
                    print(f"✅ Cipher suite adequada")
                    
    except ssl.SSLError as e:
        print(f"Erro TLS: {e}")
    except Exception as e:
        print(f"Erro de conexão: {e}")

auditar_tls("github.com")
```

```python
# Python — XXE Injection em parsers XML (vulnerabilidade de apresentação)
import xml.etree.ElementTree as ET
from defusedxml import ElementTree as SafeET  # pip install defusedxml

# ❌ XML malicioso com entidade externa (XXE)
xml_malicioso = """<?xml version="1.0"?>
<!DOCTYPE dados [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<usuario>
  <nome>&xxe;</nome>
</usuario>
"""

# ❌ Parser padrão pode processar a entidade e vazar /etc/passwd
try:
    tree = ET.fromstring(xml_malicioso)
    print(f"❌ Parser inseguro processou: {tree.find('nome').text[:50]}")
except ET.ParseError as e:
    print(f"Parser rejeitou: {e}")

# ✅ Parser seguro rejeita entidades externas automaticamente
try:
    tree = SafeET.fromstring(xml_malicioso)
except Exception as e:
    print(f"✅ defusedxml bloqueou XXE: {type(e).__name__}")
```

```python
# Python — Verificando uso de algoritmos criptográficos seguros
import hashlib
import hmac
import secrets

# ❌ Algoritmos fracos — não usar para senhas ou integridade crítica
md5_hash  = hashlib.md5(b"senha123").hexdigest()
sha1_hash = hashlib.sha1(b"senha123").hexdigest()
print(f"❌ MD5  (fraco): {md5_hash}")
print(f"❌ SHA1 (fraco): {sha1_hash}")

# ✅ Algoritmos seguros
sha256_hash = hashlib.sha256(b"senha123").hexdigest()
sha3_hash   = hashlib.sha3_256(b"senha123").hexdigest()
print(f"✅ SHA-256: {sha256_hash[:32]}...")
print(f"✅ SHA3-256: {sha3_hash[:32]}...")

# ✅ HMAC para integridade de mensagens (autenticado)
chave   = secrets.token_bytes(32)
mensagem = b"dados importantes"
mac = hmac.new(chave, mensagem, hashlib.sha256).hexdigest()
print(f"✅ HMAC-SHA256: {mac[:32]}...")

# ✅ Comparação segura (previne timing attack)
mac2 = hmac.new(chave, mensagem, hashlib.sha256).hexdigest()
valido = hmac.compare_digest(mac, mac2)
print(f"✅ Integridade verificada: {valido}")
```

### Mitigações

- **TLS 1.2+ obrigatório** — desabilitar SSLv3, TLS 1.0 e TLS 1.1 no servidor
- **Cipher suites fortes** — apenas ECDHE, AES-GCM, ChaCha20; banir RC4, DES, NULL
- **Nunca usar Pickle com dados externos** — prefira JSON com validação de esquema
- **defusedxml** para parsear XML — neutraliza XXE e outras injeções XML
- **HSTS (HTTP Strict Transport Security)** — força HTTPS e previne downgrade
- **Certificate Pinning** — em apps móveis, validar o certificado esperado explicitamente
- **Algoritmos modernos** — SHA-256+, AES-256-GCM, Ed25519; nunca MD5 ou SHA1 para segurança