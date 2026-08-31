# Troubleshooting 01 — Nginx Bind Mount

## Problema

Após criar um container Nginx utilizando um Bind Mount, a página personalizada não era exibida.
Nginx continuava exibindo "Welcome to nginx!"

Em vez da página:

> IT Service Desk Lab - Bind Mount

o navegador continuava exibindo a página padrão:

> Welcome to nginx!

## Investigação

Foi utilizado o comando:

docker inspect itsd-nginx-bind

Causa:
Destination configurado como /user/share/nginx/html

Correção:
Alterado para /usr/share/nginx/html



Resultado:
Bind Mount funcionando corretamente.
