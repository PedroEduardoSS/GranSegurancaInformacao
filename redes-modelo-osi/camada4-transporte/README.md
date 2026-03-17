# Camada 4 — Transporte

## O que é?

A **Camada de Transporte** garante a entrega de dados de ponta a ponta entre processos em hosts diferentes. Ela introduz o conceito de **portas**, permitindo que múltiplas aplicações usem a rede simultaneamente no mesmo dispositivo.

## Responsabilidades

- Multiplexação/demultiplexação via portas (0–65535)
- Controle de fluxo
- Controle de erros e retransmissão
- Segmentação e remontagem de dados
- Estabelecimento, manutenção e encerramento de conexões

## TCP vs UDP

| Característica | TCP | UDP |
|---|---|---|
| Orientado à conexão | ✅ Sim | ❌ Não |
| Confiabilidade | ✅ Garantida | ❌ Não garantida |
| Ordem dos pacotes | ✅ Mantida | ❌ Não garantida |
| Velocidade | Mais lento | Mais rápido |
| Uso típico | HTTP, FTP, SSH | DNS, streaming, jogos |

## Portas conhecidas

| Porta | Protocolo |
|---|---|
| 80 | HTTP |
| 443 | HTTPS |
| 22 | SSH |
| 53 | DNS |
| 3306 | MySQL |

## Exemplo de código — TCP e UDP

```python
# Python — Servidor TCP (orientado à conexão)
import socket
import threading

def servidor_tcp():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('0.0.0.0', 9000))
    servidor.listen(5)
    print("Servidor TCP aguardando conexões na porta 9000...")

    conn, addr = servidor.accept()
    print(f"Conexão estabelecida com {addr}")  # handshake TCP concluído
    
    dados = conn.recv(1024)
    print(f"Recebido: {dados.decode()}")
    conn.send(b"ACK: mensagem recebida!")
    conn.close()
    servidor.close()

# Cliente TCP
def cliente_tcp():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # three-way handshake: SYN -> SYN-ACK -> ACK
    cliente.connect(('127.0.0.1', 9000))
    cliente.send(b"Ola servidor!")
    resposta = cliente.recv(1024)
    print(f"Resposta: {resposta.decode()}")
    cliente.close()

# Para usar: rode servidor_tcp() em uma thread e cliente_tcp() na outra
t = threading.Thread(target=servidor_tcp)
t.start()
cliente_tcp()
t.join()
```

```python
# Python — Servidor UDP (sem conexão, mais rápido)
import socket
import threading

def servidor_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 9001))
    print("Servidor UDP escutando na porta 9001...")
    
    dados, addr = sock.recvfrom(1024)  # sem conexão prévia
    print(f"Datagrama de {addr}: {dados.decode()}")
    sock.sendto(b"OK", addr)
    sock.close()

def cliente_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # dispara e esquece — sem garantia de entrega
    sock.sendto(b"Ping UDP!", ('127.0.0.1', 9001))
    resposta, _ = sock.recvfrom(1024)
    print(f"Resposta UDP: {resposta.decode()}")
    sock.close()

t = threading.Thread(target=servidor_udp)
t.start()
import time; time.sleep(0.1)
cliente_udp()
t.join()
```

```python
# Python — Port scanner (verifica portas abertas via TCP)
import socket

def scan_porta(host: str, porta: int, timeout: float = 0.5) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        resultado = sock.connect_ex((host, porta))
        sock.close()
        return resultado == 0
    except Exception:
        return False

host = "127.0.0.1"
portas_comuns = [22, 80, 443, 3306, 5432, 6379, 8080]

print(f"Escaneando {host}...")
for porta in portas_comuns:
    status = "aberta" if scan_porta(host, porta) else "fechada"
    print(f"  Porta {porta:5d}: {status}")
```

## Curiosidade

> O **three-way handshake** do TCP é o processo de estabelecer uma conexão confiável: o cliente envia **SYN**, o servidor responde **SYN-ACK**, e o cliente confirma com **ACK**. Só depois disso os dados trafegam. O encerramento usa um processo de **four-way handshake** com FIN e ACK.

---

## Vulnerabilidades e Riscos

### Principais ameaças

| Ataque / Risco | Descrição |
|---|---|
| **SYN Flood** | Inundar o servidor com SYNs sem completar o handshake, esgotando a fila de conexões |
| **TCP Session Hijacking** | Adivinhar o número de sequência TCP para injetar dados em uma sessão ativa |
| **UDP Flood** | Enviar datagramas UDP em massa para saturar a largura de banda do alvo |
| **Port Scanning** | Varredura de portas para descobrir serviços exposto (precursor de ataques) |
| **Slowloris** | Manter muitas conexões TCP abertas com envio lento para esgotar o servidor |
| **Reset Attack (RST)** | Enviar pacotes TCP RST falsificados para derrubar conexões legítimas |
| **UDP Amplification** | Usar serviços UDP (DNS, NTP) para amplificar ataques DDoS |
| **TLS Downgrade** | Forçar a negociação de versões antigas e inseguras do TLS |

### Demonstração — SYN Flood, detecção e hardening

```python
# Python — Simulação de SYN Flood com Scapy (educacional)
# O SYN Flood explora o three-way handshake:
# o servidor aloca recursos para cada SYN recebido,
# mas o atacante nunca envia o ACK final — esgotando a fila (backlog).
from scapy.all import IP, TCP, send, RandShort
import random

def syn_flood_demo(ip_alvo: str, porta_alvo: int, quantidade: int = 10):
    """
    Demonstração conceitual do SYN Flood.
    NUNCA execute contra sistemas sem autorização explícita.
    """
    print(f"Demonstração SYN Flood -> {ip_alvo}:{porta_alvo}")
    for i in range(quantidade):
        ip_falso = f"{random.randint(1,254)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
        pkt = IP(src=ip_falso, dst=ip_alvo) / TCP(
            sport=RandShort(),   # porta origem aleatória
            dport=porta_alvo,
            flags="S",           # apenas SYN — sem completar o handshake
            seq=random.randint(0, 2**32 - 1)
        )
        # send(pkt, verbose=False)  # comentado intencionalmente
        print(f"  [{i+1:3d}] SYN forjado de {ip_falso} -> {ip_alvo}:{porta_alvo}")
    print("Demonstração concluída (nenhum pacote real foi enviado).")
```

```python
# Python — Detectando SYN Flood monitorando conexões em estado SYN_RECV
import subprocess
from collections import Counter

def detectar_syn_flood(limiar: int = 20) -> bool:
    """
    Verifica a tabela de conexões TCP do sistema.
    Muitas conexões em SYN_RECV de IPs distintos = possível SYN Flood.
    """
    saida = subprocess.check_output(
        ["ss", "-tn", "state", "syn-recv"]
    ).decode()
    
    linhas = [l for l in saida.strip().split('\n') if l and 'Recv' not in l]
    
    if not linhas:
        print("✅ Nenhuma conexão SYN_RECV pendente.")
        return False
    
    # Extrai IPs de origem
    origens = []
    for linha in linhas:
        partes = linha.split()
        if len(partes) >= 5:
            peer = partes[4]  # formato: IP:porta
            ip = peer.rsplit(':', 1)[0]
            origens.append(ip)
    
    contagem = Counter(origens)
    total = len(linhas)
    
    print(f"Conexões SYN_RECV pendentes: {total}")
    for ip, qtd in contagem.most_common(5):
        print(f"  {ip:20s}: {qtd} conexões")
    
    if total >= limiar:
        print(f"\n⚠️  ALERTA: {total} SYN_RECV >= limiar {limiar} — possível SYN Flood!")
        return True
    
    return False

detectar_syn_flood()
```

```python
# Python — Implementando servidor TCP com proteção básica contra abuso
import socket
import threading
import time
from collections import defaultdict

class ServidorTCPProtegido:
    def __init__(self, host: str, porta: int):
        self.host = host
        self.porta = porta
        self.conexoes_por_ip: dict = defaultdict(list)
        self.MAX_CONN_POR_IP = 5       # máximo de conexões simultâneas por IP
        self.RATE_LIMIT_JANELA = 60    # segundos
        self.lock = threading.Lock()
    
    def _verificar_rate_limit(self, ip: str) -> bool:
        """Retorna True se o IP excedeu o limite de conexões"""
        agora = time.time()
        with self.lock:
            # Remove timestamps antigos
            self.conexoes_por_ip[ip] = [
                t for t in self.conexoes_por_ip[ip]
                if agora - t < self.RATE_LIMIT_JANELA
            ]
            if len(self.conexoes_por_ip[ip]) >= self.MAX_CONN_POR_IP:
                return True
            self.conexoes_por_ip[ip].append(agora)
        return False
    
    def _tratar_cliente(self, conn: socket.socket, addr: tuple):
        ip, porta = addr
        
        if self._verificar_rate_limit(ip):
            print(f"🚫 Conexão bloqueada (rate limit): {ip}")
            conn.close()
            return
        
        try:
            conn.settimeout(10)  # timeout contra Slowloris
            dados = conn.recv(1024)
            if dados:
                print(f"✅ [{ip}] Recebido: {dados[:50]}")
                conn.send(b"HTTP/1.1 200 OK\r\n\r\nOK")
        except socket.timeout:
            print(f"⏱️  Timeout na conexão de {ip} (possível Slowloris)")
        finally:
            conn.close()
    
    def iniciar(self):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # SYN cookies — proteção a nível de SO contra SYN Flood
        # Ativado via: sysctl -w net.ipv4.tcp_syncookies=1
        srv.bind((self.host, self.porta))
        srv.listen(128)
        print(f"Servidor protegido em {self.host}:{self.porta}")
        while True:
            conn, addr = srv.accept()
            t = threading.Thread(target=self._tratar_cliente, args=(conn, addr))
            t.daemon = True
            t.start()
```

```bash
# Bash — Hardening TCP/IP no Linux (mitigações a nível de kernel)

# Ativar SYN Cookies (principal defesa contra SYN Flood)
sysctl -w net.ipv4.tcp_syncookies=1

# Reduzir número de retransmissões SYN-ACK (libera recursos mais rápido)
sysctl -w net.ipv4.tcp_synack_retries=2

# Aumentar backlog do socket para absorver picos
sysctl -w net.ipv4.tcp_max_syn_backlog=4096

# Desabilitar pacotes ICMP Redirect
sysctl -w net.ipv4.conf.all.accept_redirects=0

# Ativar proteção contra IP Spoofing (rp_filter)
sysctl -w net.ipv4.conf.all.rp_filter=1

# Verificar portas abertas e processos associados
ss -tlnp
```

### Mitigações

- **SYN Cookies** — o servidor não aloca estado até o handshake ser completado
- **Firewall com rate limiting** — limitar SYNs por segundo por IP (`iptables -m limit`)
- **TCP Timestamps** — dificulta ataques de previsão de número de sequência
- **TLS 1.3** — elimina negociação de versões inseguras (previne downgrade)
- **Timeout agressivo** — desconectar clientes lentos (previne Slowloris)
- **Load balancer / CDN** — absorve floods antes de atingir o servidor de origem