# IT Service Desk Lab

Laboratório prático de Docker desenvolvido para simular uma infraestrutura de TI utilizando containers, volumes, redes e Docker Compose.

O projeto foi desenvolvido com foco em aprendizado prático e documentação de conceitos utilizados em ambientes reais de infraestrutura.

---

## 🎯 Objetivo

Construir e documentar uma infraestrutura baseada em containers utilizando Docker, simulando serviços que poderiam fazer parte de um ambiente de Service Desk / Infraestrutura de TI.

Durante o laboratório são praticados:

- Criação e gerenciamento de containers
- Imagens Docker
- Port Mapping
- Docker Volumes
- Bind Mounts
- Docker Networks
- Comunicação entre containers
- DNS interno do Docker
- Docker Compose
- Persistência de dados
- Troubleshooting

---

## 🏗️ Arquitetura atual

```text
                    Docker Host
                         |
                  itsd-network
                         |
                         v
                    itsd-nginx
                         |
                    Nginx :80
                         |
                         v
                 itsd-nginx-data

localhost:8080
      |
      v
itsd-nginx:80


🐳 Tecnologias utilizadas

- Docker
- Docker Compose
- Nginx
- Docker Volumes
- Docker Networks
- Linux containers
- Windows / PowerShell

📚 Etapas do laboratório

1. Container Nginx

Foi criado um container utilizando a imagem oficial do Nginx:
docker run -d --name itsd-nginx -p 8080:80 nginx

O container foi disponibilizado através da porta:
Host:      8080
Container: 80

A aplicação pode ser acessada através de:
http://localhost:8080

2. Docker Volume

Foi criado um volume persistente:
docker volume create itsd-nginx-data

O volume foi utilizado para armazenar o conteúdo servido pelo Nginx:
itsd-nginx-data
        |
        v
/usr/share/nginx/html

Verificação

docker volume ls
docker volume inspect itsd-nginx-data


3. Bind Mount

Também foi realizado um teste utilizando Bind Mount para demonstrar a diferença entre armazenamento persistente gerenciado pelo Docker e um diretório diretamente vinculado ao host.
Windows Host
     |
     v
nginx-bind
     |
     v
Container

4. Docker Network

Foi criada uma rede Docker personalizada:
docker network create itsd-network

A rede permite a comunicação entre os containers do laboratório.
docker network ls

5. Comunicação entre containers

Foi criado um segundo container para testar a comunicação dentro da rede:
network-teste
       |
       | Docker Network
       |
       v
itsd-nginx

Foi possível resolver o container Nginx pelo próprio nome:
ping -c 3 itsd-nginx

Resultado:
3 packets transmitted, 3 packets received
0% packet loss

Isso demonstra o funcionamento da resolução de nomes dentro da Docker Network.

6. Comunicação HTTP entre containers

A comunicação HTTP também foi validada utilizando:
wget -qO- http://itsd-nginx:80

Resultado:
<h1>IT Service Desk Lab</h1>
<p>Persistent Docker Volume</p>

Isso demonstra que um container consegue acessar um serviço de outro container através do nome do serviço/container e da porta interna.

⚙️ Docker Compose

A infraestrutura foi posteriormente convertida para Docker Compose.
Arquivo utilizado:
docker-compose.yml

O Compose foi configurado para utilizar a rede e o volume existentes:
volumes:
  itsd-nginx-data:
    external: true

networks:
  itsd-network:
    external: true

A configuração foi validada utilizando:
docker compose config

A infraestrutura pode ser iniciada utilizando:
docker compose up -d

E removida utilizando:
docker compose down

🔄 Persistência de dados

Foi realizado um teste de persistência utilizando:
docker compose down

O container foi removido, porém o volume permaneceu disponível:
docker volume ls

Em seguida, o container foi recriado:
docker compose up -d

Após a recriação, a aplicação continuou disponível em:
http://localhost:8080

Isso demonstra que os dados armazenados no Docker Volume não dependem do ciclo de vida do container.

🛠️ Troubleshooting

Durante a implementação do Docker Compose foram encontrados e corrigidos alguns erros de configuração.

Erro 1 — volume em vez de volumes
Erro:
services.nginx additional properties 'volume' not allowed

Causa
A propriedade volumes foi escrita incorretamente no singular:
volume:

Correção
volumes:

Erro 2 — Nome incorreto da Network
Erro:

service "nginx" refers to undefined network itsd-networks

Causa
O serviço estava utilizando o nome:
itsd-networks

enquanto a rede existente se chamava:
itsd-network
Correção

O nome foi padronizado:
networks:
  - itsd-network

  📸 Evidências do laboratório

Os principais testes realizados durante o laboratório incluem:

Docker Compose
Validação da configuração antes da execução.

Container Nginx
Container iniciado através do Docker Compose.

Persistência
Aplicação funcionando após a remoção e recriação do container.

Network
Container conectado à rede personalizada itsd-network.

🚧 Próximas etapas

O laboratório será evoluído para uma arquitetura com múltiplos serviços:

                       IT Service Desk Lab
                               |
                         Docker Compose
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
            Nginx           Backend         PostgreSQL
              |                |                |
              +----------------+----------------+
                               |
                        itsd-network
                               |
                         Persistent Data

Próximas implementações:

- Backend
- PostgreSQL
- Comunicação Backend → PostgreSQL
- Variáveis de ambiente
- Healthchecks
- Dependências entre serviços
- Persistência do banco de dados
- Troubleshooting de múltiplos containers
- Documentação completa da arquitetura