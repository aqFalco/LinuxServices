#!/bin/python3
from os import system as s
import os.path
import time
import subprocess
import crypt

apti = "apt install -y "
Ans = "null"

s("cd /")
s("cd LinuxServices/")

while (Ans != "s"):
    s("clear")
    User = []
    Users = ""
    VerificarZero = ""
    VerificarRange = ""
    ComProxy = "null"
    IpMaquina = ""
    DefGateway = ""
    Dns = ""
    Dominio = ""
    Password = ""
    Range = ""
    NomeMaquina = ""
    while (IpMaquina == ""):
        s("clear")
        IpMaquina = input("Introduzir ip da maquina: ")
        VerificarZero = IpMaquina.split(".")
        if VerificarZero[3] == "0":
            IpMaquina = ""
            print("O IP DA MAQUINA NAO PODE SER 0(ESSE E O DE REDE)")
            time.sleep(1.3)
    while (ComProxy != "s" and ComProxy != "n"):
        s("clear")
        ComProxy = input("Está a usar proxy?       s/n: ")
    if ComProxy == "s":
        Proxy = input("Introduzir proxy (Exemplo: 172.16.10.251:8080): ")
    while (DefGateway == ""):
        s("clear")
        DefGateway = input("Introduzir ip Default Gateway: ")
    while (Dns == ""):
        s("clear")
        Dns = input("Introduzir ip DNS: ")
    while (Dominio == ""):
        s("clear")
        Dominio = input("Introduzir nome Dominio: ")
    while (Password == ""):
        s("clear")
        Password = input("Introduzir a palavra pass geral (para tudo): ")
    while (Range == ""):
        s("clear")
        Range = input("Introduzir Range de ip's  \n  Exemplo: <192.168.50.5 192.168.50.35>: ")
        VerificarRange = Range.split(".")
        if len(VerificarRange) != 7:
            print("Formato errado, introduza novamente.")
            time.sleep(1.3)
            Range = ""
    while (NomeMaquina == ""):
        s("clear")
        NomeMaquina = input("Introduzir Nome da maquina (root@<nome_aqui>): ")
    s("clear")
    time.sleep(0.3)
    Nusers = int(input("Introduza o numero de utilizadores: "))
    User = []
    i = 0
    while i < Nusers:
        s("clear")
        User.append(input("Coloque o nome do " + str(i+1) + " User: "))
        if User[i] != "":
            i+=1

    print("IP da maquina: " + IpMaquina)
    if ComProxy == "s":
        print("Proxy: " + Proxy)
    else:
        print("Sem Proxy")
    print("Default Gateway: " + DefGateway)
    print("DNS: " + Dns)
    print("Dominio: " + Dominio)
    print("Password: " + Password)
    print("Range: " + Range)
    print("Nome da maquina: " + NomeMaquina)
    for i in range(Nusers):
        if i != Nusers-1:
            Users = Users + User[i] + ", "
        else:
            Users += User[i]
    print("Users: " + Users)
    print()
    print("Esta informacao está correta?      s/n")
    Ans = input()

s("ip link set enp0s3 up")
s("ip link set enp0s8 down")
time.sleep(3)
s("apt update && apt upgrade -y")

while (os.path.isdir('/etc/dhcp/dhcpd') == False and os.path.isdir('/etc/bind') == False and os.path.isfile('/etc/asterisk') == False):
    for i in ["isc-dhcp-server", "bind9", "apache2", "asterisk", "default-jre", "mysql-server"]: #services to install
        s(apti + i)

#dhcp
Ip = IpMaquina.split(".")
IpRede = ""
for i in Ip:
    if i == Ip[3]:
        IpRede += "0"
    else:
        IpRede += i + "."

IpRedeArpa = ""
for i in [Ip[2], Ip[1], Ip[0], "in-addr.arpa"]:
    IpRedeArpa += i
    if i != "in-addr.arpa":
        IpRedeArpa += "."

file = "00-installer-config.yaml"
fin = open(file, "rt")
data = fin.read()
data = data.replace("ipmaquina", IpMaquina)
data = data.replace("defgate", DefGateway)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

s("mv 00-installer-config.yaml /etc/netplan/")
s("netplan apply")

file = "dhcpd.conf"
fin = open(file, "rt")
data = fin.read()
data = data.replace("dominio", Dominio)
data = data.replace("defgate", DefGateway)
data = data.replace("iprede", IpRede)
data = data.replace("rangedeips", Range)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

s("mv dhcpd.conf /etc/dhcp/")
s("mv isc-dhcp-server /etc/default/")

s("service isc-dhcp-server restart")

#firewall
s("ufw enable")
s("for i in 9090 9091 9095 9096 5222 7777 25 53 143 5060 80 ; do ufw allow $i ; done")

#bind9
file = "named.conf.local"
fin = open(file, "rt")
data = fin.read()
data = data.replace("dominio", Dominio)
data = data.replace("ipdaarpa", IpRedeArpa)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

s("mv named.conf.local /etc/bind/")

file = "forward.terceiradose.pt"
fin = open(file, "rt")
data = fin.read()
data = data.replace("dominio", Dominio)
data = data.replace("nomedamaquina", NomeMaquina)
data = data.replace("defgate", DefGateway)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

s("mv forward.terceiradose.pt forward." + Dominio)
s("mv forward." + Dominio + " /etc/bind/")

file = "reverse.terceiradose.pt"
fin = open(file, "rt")
data = fin.read()
data = data.replace("dominio", Dominio)
data = data.replace("nomedamaquina", NomeMaquina)
data = data.replace("defgate", DefGateway)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

s("mv reverse.terceiradose.pt reverse." + Dominio)
s("mv reverse." + Dominio + " /etc/bind/")

s("service bind9 restart")

#apache2
file = "index.html"
fin = open(file, "rt")
data = fin.read()
data = data.replace("titulosite", "Trocar em /var/www/html/index.html")
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()


s("mv index.html /var/www/html/")
s("mv ImagemHtml.jpg /var/www/html/")
s("service apache2 restart")

#openfire
s("mysql -u root --skip-password -e \"create database openfire; CREATE USER 'admin'@'localhost' IDENTIFIED BY '" + Password + "'; grant all privileges on openfire.* to 'admin'@'localhost'; flush privileges;\"")
if ComProxy == "s":
    s('export "http_proxy=http://' + Proxy + '/')
    s('export "https_proxy=https://' + Proxy + '/')
Error = 0
while (os.path.isfile('/LinuxServices/openfire.deb') == False):
    s("ip link set enp0s8 up && ip link set enp0s3 down")
    s("ip link set enp0s3 up && ip link set enp0s8 down")
    time.sleep(5)
    s("wget https://igniterealtime.org/downloadServlet?filename=openfire/openfire_4.5.3_all.deb -O openfire.deb")
    Error+=1
    if Error>=5:
        s("clear")
        print("Ocurreu um erro a fazer o download do openfire.deb...")
        print("               Processo a Finalizar...")
        exit()
s("dpkg -i openfire.deb")
s("cd LinuxServices/")
s("mysql -u root --skip-password -e \"use openfire; source /usr/share/openfire/resources/database/openfire_mysql.slq;\"")
s("service openfire restart")

for i in range(Nusers):
    s('echo " " >> /etc/asterisk/sip.conf')
    s('echo "[' + User[i] + ']" >> /etc/asterisk/sip.conf') 
    s('echo "type=friend" >> /etc/asterisk/sip.conf')
    s('echo "port=5060" >> /etc/asterisk/sip.conf')
    s('echo "nat=yes" >> /etc/asterisk/sip.conf')
    s('echo "qualify=yes" >> /etc/asterisk/sip.conf')
    RegContext = str(i+1)
    RegContext = RegContext.zfill(3)
    s('echo "regcontext=' + RegContext + '" >> /etc/asterisk/sip.conf')
    s('echo "context=from-internal" >> /etc/asterisk/sip.conf')

for i in range(Nusers):
    s('echo " " >> /etc/asterisk/users.conf')
    s('echo "[' + User[i] + ']" >> /etc/asterisk/users.conf')
    s('echo "full name = ' + User[i] + '" >> /etc/asterisk/users.conf')
    s('echo "hassip = yes" >> /etc/asterisk/users.conf')
    s('echo "secret = ' + Password + '" >> /etc/asterisk/users.conf')
    s('echo "context = from-internal" >> /etc/asterisk/users.conf')
    s('echo "host = dynamic" >> /etc/asterisk/users.conf')

s('echo " " >> /etc/asterisk/extensions.conf')
s('echo "[from-internal]" >> /etc/asterisk/extensions.conf')
for i in range(Nusers): 
    RegContext = str(i+1)
    RegContext = RegContext.zfill(3)  
    s('echo "exten=>' + RegContext + ',1,Dial(SIP/' + User[i] + ',10)" >> /etc/asterisk/extensions.conf')
s('echo " " >> /etc/asterisk/extensions.conf')
All = "exten=>all,1,Dial("
for i in range(Nusers):
    if i == Nusers-1:
        All = All + "SIP/" + User[i] + ",10)"
    else:
        All = All + "SIP/" + User[i] + "&"
s('echo "' + All + '" >> /etc/asterisk/extensions.conf')
s("service asterisk restart")

s("apt remove -y postfix")
s("apt purge -y postfix")
s("export DEBIAN_FRONTEND=noninteractive")
s("DEBIAN_FRONTEND=noninteractive apt-get install Postfix")

file = "main.cf"
fin = open(file, "rt")
data = fin.read()
data = data.replace("dominio", Dominio)
data = data.replace("nomemaquina", NomeMaquina)
data = data.replace("iprede", IpRede)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

file = "config.dat"
fin = open(file, "rt")
data = fin.read()
data = data.replace("dominio", Dominio)
data = data.replace("nomemaquina", NomeMaquina)
data = data.replace("iprede", IpRede)
fin.close()
fin = open(file, "wt")
fin.write(data)
fin.close()

s("DEBIAN_FRONTEND=noninteractive " + apti + " courier-imap")
s(apti + " mailutils")
s("mv main.cf /etc/postfix")
s("mv config.dat /var/cache/debconf/config.dat")
time.sleep(1)
s("export DEBIAN_FRONTEND=noninteractive")
s("maildirmake /etc/skel/Maildir")
Password = crypt.crypt(Password)
for i in range(Nusers):
    UserAdicionado = User[i]
    subprocess.run(['useradd', '-m', '-p', Password, UserAdicionado ])

s("/etc/init.d/courier-imap restart")
s("/etc/init.d/courier-authdaemon restart")
s("/etc/init.d/postfix restart")

s("ip link set enp0s3 down")
s("ip link set enp0s8 up")

