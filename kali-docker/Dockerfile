FROM kalilinux/kali-rolling

# Evita prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Atualiza e instala ferramentas básicas + sudo
RUN apt-get update && apt-get install -y \
    kali-linux-headless \
    sudo \
    vim \
    curl \
    iputils-ping \
    && apt-get clean

# Cria um usuário não-root para segurança
RUN useradd -m -s /bin/bash kali-user && \
    echo "kali-user:kali" | chpasswd && \
    adduser kali-user sudo

# Define o usuário padrão
USER kali-user
WORKDIR /home/kali-user