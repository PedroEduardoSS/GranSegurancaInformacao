from scapy.all import sniff, Raw

def catch_packet(packet):
    if packet.haslayer(Raw):
        dados = packet[Raw].load.decode(errors="ignore")
        
        if len(dados) > 10:
            print(dados)

sniff(
    iface="Wi-Fi",
    filter="tcp port 5000",
    prn=catch_packet,
    store=False
)