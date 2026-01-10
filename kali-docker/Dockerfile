FROM kalilinux/kali-rolling

ENV DEBIAN_FRONTEND=noninteractive

# Instala Desktop XFCE, ferramentas de rede e NoVNC
RUN apt-get update && apt-get install -y \
    kali-desktop-xfce \
    kali-linux-headless \
    novnc \
    dbus-x11 \
    tigervnc-standalone-server \
    sudo \
    curl \
    && apt-get clean

# Cria usuário não-root
RUN useradd -m -s /bin/bash kali-user && \
    echo "kali-user:kali" | chpasswd && \
    adduser kali-user sudo

# Configura o diretório de trabalho e permissões para o VNC
USER kali-user
WORKDIR /home/kali-user

# Script de inicialização para o VNC e NoVNC
RUN mkdir -p .vnc && \
    echo "password" | vncpasswd -f > .vnc/passwd && \
    chmod 600 .vnc/passwd

# Porta do NoVNC (Web) e VNC (Direto)
EXPOSE 6080 5901

# Comando para iniciar o servidor VNC e o NoVNC
CMD vncserver :1 -geometry 1280x720 -depth 24 && \
    /usr/share/novnc/utils/novnc_proxy --vnc localhost:5901 --listen 6080