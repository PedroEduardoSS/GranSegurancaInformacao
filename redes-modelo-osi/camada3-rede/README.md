# Camada 3 — Rede

## O que é?

A **Camada de Rede** é responsável pelo **endereçamento lógico** e pelo **roteamento** de pacotes entre redes diferentes. Enquanto a Camada 2 cuida de dispositivos na mesma rede local, a Camada 3 permite a comunicação entre redes distintas — como acontece na Internet.

## Responsabilidades

- Endereçamento lógico (IPv4, IPv6)
- Roteamento — determinar o melhor caminho entre origem e destino
- Fragmentação e remontagem de pacotes
- Tradução de endereços (NAT)
- Controle de congestionamento

## Protocolos principais

| Protocolo | Descrição |
|---|---|
| IPv4 | Endereçamento 32 bits (ex: 192.168.1.1) |
| IPv6 | Endereçamento 128 bits |
| ICMP | Mensagens de controle (ping) |
| ARP | Resolução MAC ↔ IP |
| OSPF / BGP | Protocolos de roteamento |

## Dispositivo

- **Roteador** — opera na Camada 3, encaminha pacotes entre redes

## Exemplo de código — IP, roteamento e ICMP

```python
# Python — Manipulando endereços IPv4
import ipaddress
import socket

# Trabalhando com sub-redes
rede = ipaddress.IPv4Network('192.168.1.0/24')
print(f"Rede       : {rede.network_address}")
print(f"Broadcast  : {rede.broadcast_address}")
print(f"Máscara    : {rede.netmask}")
print(f"Total hosts: {rede.num_addresses - 2}")

# Verificando se um IP pertence à rede
ip = ipaddress.IPv4Address('192.168.1.100')
print(f"{ip} está na rede: {ip in rede}")

# Listando os primeiros 5 hosts
for host in list(rede.hosts())[:5]:
    print(f"  Host: {host}")

# Calculando supernet
supernet = rede.supernet()
print(f"Supernet: {supernet}")
```

```python
# Python — Ping ICMP (Camada 3)
import os
import platform

def ping(host: str) -> bool:
    sistema = platform.system().lower()
    flag = "-n" if sistema == "windows" else "-c"
    resposta = os.system(f"ping {flag} 1 -W 1 {host} > /dev/null 2>&1")
    return resposta == 0

hosts = ["8.8.8.8", "1.1.1.1", "192.168.1.1"]
for h in hosts:
    status = "online" if ping(h) else "offline"
    print(f"{h:15s} — {status}")
```

```python
# Python — Construindo pacote IP com Scapy
from scapy.all import IP, ICMP, TCP, send, sr1, traceroute

# Criando pacote IP + ICMP (ping)
pacote = IP(dst="8.8.8.8") / ICMP()
print(pacote.summary())

# Enviando e aguardando resposta
resposta = sr1(pacote, timeout=2, verbose=False)
if resposta:
    print(f"Resposta de {resposta[IP].src} — TTL: {resposta[IP].ttl}")

# Traceroute manual — explora o campo TTL
for ttl in range(1, 6):
    pkt = IP(dst="8.8.8.8", ttl=ttl) / ICMP()
    resp = sr1(pkt, timeout=1, verbose=False)
    if resp:
        print(f"Salto {ttl}: {resp[IP].src}")
```

## Curiosidade

> O campo **TTL (Time to Live)** de um pacote IP decrementa em 1 a cada roteador. Quando chega a 0, o pacote é descartado e um ICMP "Time Exceeded" é enviado de volta — é assim que o comando `traceroute` funciona!

---

## Vulnerabilidades e Riscos

### Principais ameaças

| Ataque / Risco | Descrição |
|---|---|
| **IP Spoofing** | Falsificar o endereço IP de origem para mascarar a identidade do atacante |
| **ICMP Flood (Ping Flood)** | Inundar o alvo com pacotes ICMP para causar negação de serviço (DoS) |
| **Smurf Attack** | Enviar ICMP broadcast com IP de origem falsificado (amplificação de DoS) |
| **Route Hijacking / BGP Hijacking** | Anunciar rotas BGP falsas para desviar o tráfego da Internet |
| **IP Fragmentation Attack** | Enviar fragmentos IP malformados para causar crash em sistemas vulneráveis |
| **Teardrop Attack** | Fragmentos com offsets sobrepostos para derrubar a pilha TCP/IP |
| **ICMP Redirect Attack** | Enviar ICMP Redirect para alterar a tabela de rotas da vítima |
| **TTL Manipulation** | Manipular o TTL para evadir firewalls e sistemas de detecção de intrusão |

### Demonstração — IP Spoofing, detecção e proteção

```python
# Python — Construindo pacote com IP Spoofed (demonstração educacional)
# IP Spoofing é a base de muitos ataques de amplificação (DDoS)
from scapy.all import IP, ICMP, UDP, send

def demonstrar_ip_spoofing(ip_destino: str, ip_falso: str):
    """
    Cria pacote ICMP com IP de origem falsificado.
    Na prática, ISPs usem BCP38 para bloquear isso, mas redes
    internas mal configuradas ainda são vulneráveis.
    SOMENTE para fins educacionais em ambiente controlado.
    """
    pacote = IP(src=ip_falso, dst=ip_destino) / ICMP()
    print(f"Pacote criado: src={ip_falso} -> dst={ip_destino}")
    print(f"  Tamanho: {len(pacote)} bytes")
    print(f"  Resumo : {pacote.summary()}")
    # send(pacote, verbose=False)  # comentado intencionalmente
```

```python
# Python — Detectando varredura de rede (Nmap-like simplificado)
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed

def ping_tcp(ip: str, porta: int = 80, timeout: float = 0.3) -> bool:
    """Verifica se um host está ativo tentando conexão TCP"""
    try:
        with socket.create_connection((ip, porta), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        # ConnectionRefused = host ativo, mas porta fechada
        try:
            socket.create_connection((ip, 443), timeout=timeout)
            return True
        except:
            pass
    return False

def varrer_rede(cidr: str, max_workers: int = 50) -> list[str]:
    """Descobre hosts ativos em uma sub-rede — técnica usada por atacantes e admins"""
    rede = ipaddress.IPv4Network(cidr, strict=False)
    hosts_ativos = []
    
    print(f"Varrendo {rede} ({rede.num_addresses - 2} hosts possíveis)...")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futuros = {
            executor.submit(ping_tcp, str(ip)): str(ip)
            for ip in rede.hosts()
        }
        for futuro in as_completed(futuros):
            ip = futuros[futuro]
            if futuro.result():
                hosts_ativos.append(ip)
                print(f"  ✅ Ativo: {ip}")
    
    print(f"\nTotal: {len(hosts_ativos)} hosts ativos")
    return hosts_ativos

# varrer_rede("192.168.1.0/24")
```

```python
# Python — Detectando ICMP Flood (monitoramento de volume)
from scapy.all import sniff, IP, ICMP
from collections import defaultdict
import time

contadores = defaultdict(int)
INICIO = time.time()
LIMIAR_PPS = 50  # pacotes por segundo — acima disso, suspeito

def analisar_pacote(pkt):
    if pkt.haslayer(ICMP) and pkt.haslayer(IP):
        origem = pkt[IP].src
        contadores[origem] += 1
        
        elapsed = time.time() - INICIO
        pps = contadores[origem] / elapsed if elapsed > 0 else 0
        
        if pps > LIMIAR_PPS:
            print(f"⚠️  Possível ICMP Flood de {origem}: {pps:.0f} pkt/s")

def monitorar_icmp(interface: str = "eth0", duracao: int = 30):
    print(f"Monitorando ICMP em {interface} por {duracao}s...")
    sniff(iface=interface, filter="icmp", prn=analisar_pacote,
          store=False, timeout=duracao)
    
    print("\nResumo por origem:")
    for ip, total in sorted(contadores.items(), key=lambda x: -x[1]):
        print(f"  {ip:16s}: {total} pacotes ICMP")

# monitorar_icmp("eth0")
```

```python
# Python — Verificando regras de roteamento suspeitas
import subprocess

def auditar_rotas():
    """
    Exibe e analisa a tabela de roteamento.
    Rotas inesperadas podem indicar ICMP Redirect Attack ou comprometimento.
    """
    print("=== Tabela de Roteamento ===")
    saida = subprocess.check_output(["ip", "route", "show"]).decode()
    print(saida)
    
    # Verificando rota padrão (gateway)
    for linha in saida.split('\n'):
        if 'default' in linha:
            print(f"Gateway padrão: {linha.strip()}")
        if 'via' in linha and '169.254' in linha:
            print(f"⚠️  Rota APIPA suspeita detectada: {linha.strip()}")

auditar_rotas()
```

### Mitigações

- **BCP38 / Ingress Filtering** — roteadores descartam pacotes com IP de origem inválido (previne spoofing)
- **Rate limiting ICMP** — limitar requisições ICMP por segundo no firewall
- **ACLs no roteador** — bloquear faixas de IP privadas vindo da Internet
- **RPKI (Resource Public Key Infrastructure)** — valida anúncios BGP para prevenir hijacking
- **Firewall stateful** — rastreia conexões e bloqueia pacotes sem estado legítimo
- **Desabilitar ICMP Redirect** — `sysctl -w net.ipv4.conf.all.accept_redirects=0`