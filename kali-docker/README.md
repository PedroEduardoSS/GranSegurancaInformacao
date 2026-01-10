# 🧪 Kali Linux Docker Lab (GUI & Secure)

Este projeto configura um ambiente de Kali linux isolado, seguro e persistente utilizando Docker Compose. Ele inclui uma interface gráfica (XFCE) acessível via navegador e um usuário não-root para aumentar a segurança.

## 🚀 Funcionalidades

Interface Gráfica (GUI): Acesso via NoVNC no navegador (porta 6080).

Persistência de Dados: Pasta ./data sincronizada com o container.

Segurança: Limitação de CPU/RAM e redução de privilégios do Kernel (cap_drop).

Pronto para Uso: Ferramentas essenciais de rede já pré-instaladas.

## 🛠️ Pré-requisitos

Docker instalado.

Docker Compose instalado.

## 📂 Estrutura do Projeto

kali-lab/

├── docker-compose.yml

├── Dockerfile

├── README.md

└── data/

## ⚡ Como Iniciar

1. Construir e subir o ambiente:
`docker-compose up -d --build`

2. Acessar a Interface Gráfica: Abra seu navegador e vá para:

    URL: http://localhost:6080/vnc.html

    Senha: password

3. Acessar via Terminal (Linha de Comando):
`docker exec -it kali_gui_lab /bin/bash`

## 🛠️ Comandos Úteis dentro do Kali

| Tarefa | Comando |
|---|---|
|Atualizar Repositórios|sudo apt update|
|Atualizar sistema |sudo apt upgrade|
|Instalar novas ferramentas|sudo apt install <nome-do-pacote>|

## 💾 Persistência e Usuário

- Arquivos: Salve sempre seus relatórios e scripts em /home/kali-user/work. Eles ficarão salvos na pasta ./data da sua máquina real.

- Usuário Padrão: kali-user

- Senha Sudo: kali

## 🔒 Segurança do Laboratório
Este laboratório foi configurado com boas práticas:

- Capacidades: O container não tem acesso total ao hardware (apenas NET_RAW e NET_ADMIN para ferramentas de rede).

- Recursos: Limitado a 2 CPUs e 4GB de RAM para não travar o computador hospedeiro.

- Isolamento: Rede bridge dedicada (kali_internal).

## 🛑 Encerrando o Ambiente

Para parar o laboratório mas manter os arquivos e o container:
`docker-compose stop`

Para remover o container completamente (os arquivos na pasta /data não serão excluídos):
`docker-compose down`

Para iniciar o ambiente novamente, se já tiver sido criado anteriormente com :
`docker-compose start`
