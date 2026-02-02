# 🕵️‍♂️ OSINT & Metadata Investigation Lab

Este projeto fornece um ambiente isolado e pronto para uso baseado em Kali Linux e Docker. Ele foi projetado para analistas de segurança e investigadores digitais (OSINT) que precisam de ferramentas de coleta de dados e análise de metadados sem poluir o sistema operacional principal.

## 🛠️ Ferramentas Incluídas

### Análise de Arquivos (Metadados)

|Ferramenta|Descrição|
|---|---|
|ExifTool|A ferramenta definitiva para ler, escrever e editar metadados em quase qualquer tipo de arquivo (Imagens, PDFs, Vídeos).|
|MAT2|Ferramenta forense focada em privacidade para remover metadados de arquivos antes de compartilhá-los.|

### Investigação de Pessoas e Usuários

Ferramenta|Descrição
|---|---|
Sherlock|Busca o mesmo nome de usuário em centenas de redes sociais simultaneamente.
Holehe|Verifica em quais sites um endereço de e-mail está cadastrado (utiliza funções de recuperação de senha).
SocialScan|Verifica a disponibilidade de nomes de usuário e e-mails em plataformas populares com alta precisão.

### Reconhecimento de Infraestrutura e Web

Ferramenta|Descrição
|---|---|
theHarvester|Coleta e-mails, nomes de subdomínios, IPs e URLs usando mecanismos de busca e bancos de dados públicos.
Amass|Mapeamento profundo de superfícies de ataque e descoberta de ativos de rede.
Subfinder|Ferramenta extremamente rápida para descoberta de subdomínios passivos.
Photon|Crawler inteligente que extrai URLs, e-mails, contas de redes sociais e arquivos de um site alvo.|
SpiderFoot|Ferramenta de automação OSINT com interface web que integra centenas de fontes de dados.

## 🚀 Comandos Rápidos

1. **Iniciar o ambiente**
Para construir a imagem e subir os containers em segundo plano:
`docker compose up -d`

2. **Acessar o terminal de investigação (Kali)**
Este é o comando que você mais usará para rodar as ferramentas de linha de comando:
`docker exec -it kali-osint bash`

3. **Acessar o SpiderFoot (Interface Web)**
Abra o seu navegador no endereço:
`http://localhost:5001`

4. **Parar o laboratório**
Para desligar os containers:
`docker compose stop`

## 📂 Como usar a pasta de investigação

A pasta local ./investigacoes está sincronizada com a pasta /root/osint dentro do container.

- Para analisar um arquivo: Coloque a imagem ou PDF na pasta ./investigacoes no seu computador e, dentro do container, rode exiftool nome_do_arquivo.jpg.

- Para salvar relatórios: Sempre salve os outputs das ferramentas dentro de /root/osint para que eles não sumam quando o container for destruído.

## 📋 Exemplos de Uso no Terminal

Buscar um usuário no Sherlock:
`sherlock nome_do_alvo`

Verificar cadastros de um e-mail com Holehe:
`holehe alvo@gmail.com`

Extrair GPS e dados de uma foto:
`exiftool foto_suspeita.jpg | grep -i "GPS"`

Mapear subdomínios de uma empresa:
`subfinder -d empresa.com.br`