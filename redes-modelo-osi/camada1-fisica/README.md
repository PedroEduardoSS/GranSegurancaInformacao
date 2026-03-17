# Camada 1 — Física

## O que é?

A **Camada Física** é a base do modelo OSI. Ela é responsável pela transmissão e recepção de fluxos de bits brutos através de um meio físico — cabos, fibra óptica, ondas de rádio, etc. Não existe noção de pacotes ou endereços aqui: apenas sinais elétricos, ópticos ou eletromagnéticos.

## Responsabilidades

- Definição de tensões, frequências e temporização dos sinais
- Definição do tipo de cabo/conector (RJ45, fibra, coaxial)
- Codificação de bits em sinais (NRZ, Manchester, etc.)
- Taxas de transmissão (baudrate / bitrate)
- Modos de transmissão: simplex, half-duplex, full-duplex
- Topologia física da rede (estrela, barramento, anel)

## Exemplos de hardware

| Dispositivo | Função |
|---|---|
| Hub | Repete o sinal para todas as portas |
| Repetidor | Regenera o sinal elétrico |
| Cabo UTP/STP | Meio de transmissão |
| Fibra óptica | Transmissão via luz |
| Modem | Modula/demodula sinais analógicos |

## Exemplo de código — Comunicação serial (bits físicos via porta serial)

```python
# Python — leitura/escrita de bits via porta serial (UART)
# Simula o nível mais baixo de comunicação física entre dois dispositivos
import serial
import time

# Configuração da porta serial (parâmetros físicos da comunicação)
ser = serial.Serial(
    port='/dev/ttyUSB0',   # porta física
    baudrate=9600,         # velocidade em bits/segundo
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

# Enviando bits via meio físico
mensagem = b'\x48\x65\x6C\x6C\x6F'  # "Hello" em bytes brutos
ser.write(mensagem)
print(f"Enviados {len(mensagem)} bytes pelo meio físico")

# Recebendo bits
dados = ser.read(5)
print(f"Recebidos: {dados}")

ser.close()
```

```c
// C — Configuração de interface de rede em baixo nível (Linux)
// Demonstra acesso físico à NIC via raw socket
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <linux/if_packet.h>
#include <net/ethernet.h>

int main() {
    // Cria socket raw — acesso direto ao hardware de rede
    int sockfd = socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL));
    if (sockfd < 0) {
        perror("Erro ao criar socket raw");
        return 1;
    }

    printf("Socket raw criado — acesso direto à camada física disponível\n");

    // Buffer para capturar quadros brutos da placa de rede
    unsigned char buffer[65536];
    struct sockaddr saddr;
    int saddr_len = sizeof(saddr);

    int data_size = recvfrom(sockfd, buffer, 65536, 0, &saddr, &saddr_len);
    printf("Capturados %d bytes brutos do meio físico\n", data_size);

    return 0;
}
```

## Curiosidade

> A Camada Física não sabe o que os bits significam — ela apenas os transmite. É como um carteiro que entrega cartas sem saber o conteúdo.

---

## Vulnerabilidades e Riscos

### Principais ameaças

| Ataque / Risco | Descrição |
|---|---|
| **Wiretapping (escuta)** | Interceptação física do cabo para capturar sinais elétricos ou ópticos |
| **Jamming** | Emissão de interferência eletromagnética para derrubar a comunicação sem fio |
| **Sniffing passivo** | Conectar um dispositivo ao meio físico para capturar todo o tráfego |
| **Corte de cabo** | Sabotagem física da infraestrutura (ataques a data centers, backbones) |
| **Tap de fibra óptica** | Dobrar levemente a fibra para capturar o sinal de luz sem romper o cabo |
| **Emanação de van Eck** | Captura de sinais eletromagnéticos emitidos por monitores e cabos (TEMPEST) |
| **Evil Twin (Wi-Fi)** | Criar um ponto de acesso físico falso com o mesmo SSID da rede legítima |

### Demonstração — Detecção de interferência e sniffing

```python
# Python — Monitorando qualidade do sinal Wi-Fi (detectando possível jamming)
import subprocess
import re
import time

def obter_qualidade_wifi(interface: str = "wlan0") -> dict:
    """Lê métricas do sinal físico da interface Wi-Fi"""
    try:
        saida = subprocess.check_output(
            ["iwconfig", interface], stderr=subprocess.DEVNULL
        ).decode()
        
        # Extraindo métricas físicas do sinal
        qualidade  = re.search(r'Link Quality=(\d+/\d+)', saida)
        nivel      = re.search(r'Signal level=(-?\d+) dBm', saida)
        ruido      = re.search(r'Noise level=(-?\d+) dBm', saida)
        
        return {
            "qualidade" : qualidade.group(1) if qualidade else "N/A",
            "sinal_dbm" : int(nivel.group(1)) if nivel else None,
            "ruido_dbm" : int(ruido.group(1)) if ruido else None,
        }
    except Exception as e:
        return {"erro": str(e)}

def detectar_jamming(interface: str, amostras: int = 10, intervalo: float = 1.0):
    """
    Monitora o sinal ao longo do tempo.
    Queda abrupta no nível do sinal pode indicar jamming ou interferência física.
    """
    historico = []
    print(f"Monitorando interface {interface} por {amostras}s...")
    
    for i in range(amostras):
        info = obter_qualidade_wifi(interface)
        sinal = info.get("sinal_dbm")
        historico.append(sinal)
        print(f"  [{i+1:02d}] Sinal: {sinal} dBm")
        time.sleep(intervalo)
    
    validos = [s for s in historico if s is not None]
    if len(validos) >= 2:
        variacao = max(validos) - min(validos)
        if variacao > 20:
            print(f"\n⚠️  ALERTA: variação de {variacao} dBm detectada — possível jamming ou interferência!")
        else:
            print(f"\n✅ Sinal estável (variação: {variacao} dBm)")

# detectar_jamming("wlan0")
```

```python
# Python — Detectando modo promíscuo em interfaces (indica possível sniffing físico)
import subprocess

def verificar_modo_promiscuo() -> list:
    """
    Interfaces em modo promíscuo capturam TODOS os pacotes do meio físico,
    não apenas os destinados àquela máquina — sinal de possível sniffing.
    """
    suspeitas = []
    
    try:
        saida = subprocess.check_output(["ip", "link", "show"]).decode()
        linhas = saida.split('\n')
        
        for linha in linhas:
            if 'PROMISC' in linha:
                # Extrai o nome da interface
                partes = linha.split(':')
                if len(partes) >= 2:
                    nome = partes[1].strip().split('@')[0]
                    suspeitas.append(nome)
                    print(f"⚠️  Interface em modo promíscuo: {nome}")
        
        if not suspeitas:
            print("✅ Nenhuma interface em modo promíscuo detectada.")
    
    except Exception as e:
        print(f"Erro: {e}")
    
    return suspeitas

verificar_modo_promiscuo()
```

```bash
# Bash — Verificar cabos e interfaces suspeitas no Linux

# Listar todas as interfaces e seus estados físicos
ip link show

# Verificar se alguma interface está em modo promíscuo
ip link show | grep PROMISC

# Ver estatísticas físicas de erros na interface (colisões, drops)
ip -s link show eth0

# Verificar redes Wi-Fi visíveis (detectar Evil Twin — SSIDs duplicados)
nmcli dev wifi list | sort -k3

# Verificar logs de conexões físicas (plug/unplug de cabos)
dmesg | grep -i "link\|carrier\|cable"
```

### Mitigações

- **Cabos blindados (STP)** e instalação em calhas fechadas para dificultar wiretapping
- **Fibra óptica** em vez de cobre — muito mais difícil de interceptar sem detecção
- **Monitoramento físico** de data centers com câmeras e controle de acesso
- **WPA3** e supressão de SSID para reduzir exposição em redes Wi-Fi
- **Detecção de RF** para identificar jammers e dispositivos não autorizados
- **Gaiola de Faraday** em ambientes de alta segurança (previne emanação EM)