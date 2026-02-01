FROM kalilinux/kali-rolling

# Evita interações durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    kali-linux-headless \
    git \
    python3 \
    python3-pip \
    curl \
    # --- FERRAMENTAS DE METADADOS ---
    libimage-exiftool-perl \
    mat2 \
    # --- FERRAMENTAS OSINT ---
    theharvester \
    amass \
    sherlock \
    subfinder \
    && apt-get clean

# Ferramentas via Python PIP
RUN pip3 install --break-system-packages \
    holehe \
    photon \
    socialscan \
    gallery-dl

WORKDIR /root/osint