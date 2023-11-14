# TP2-SDN

Trabajo Practico 2 de Introduccion a Sistemas Distribuidos

# Pasos

1) git clone https://github.com/noxrepo/pox.git
2) Ejecutar:  python3 pox/pox.py forwarding.l2_learning 

# Comando para ejectuar la topologia personalizada
## Ejecutar en otra terminal:

n = cantidad de switches (tiene que ser mayor a 1)

### Ejecucion sin xterm

sudo mn --custom example.py --topo mytopo,n --mac --arp --switch ovsk --controller remote

### Ejecucion con xterm

sudo mn --custom example.py --topo mytopo,n --mac --arp -x --switch ovsk --controller remote

# Notion
[TP2](https://mis-notas.notion.site/TP2-0c7f3987e3324e289050206e3edb01a4?pvs=4)
