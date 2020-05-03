#!/bin/python 
# @author: [ Paulino Bermúdez R.]
# @Description: Script de conexión automática al Router CSR-1000v.
# Para obtener información del mismo.

# NOTA: NO SE SI PUEDA CONFIGURAR LOE MÉTODOS QUE FALTAN MAÑANA, ASI QUE QUEDA:
#   - métodos de la clase conectaRouter.
#   - probar el script
#   - Ver la información de los archivos YANG.
#   - Redacción del archivo

# Librerias importadas
import os, sys, json, xml.dom.minidom ,paramiko, requests,tabulate, urllib3, time 
from netmiko import ConnectHandler
#from ncclient import manager
# Limpio pantalla del sistema
os.system('clear')
os.system('cls')
# Desactivamos las alarmas de warning del SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class inicia:
    conectaRouter(ip,user,key)
class conectaRouter:
    # Definimos los métodos para obtener la información del router
    # Método inicial para las credenciales.
    def __init__(self,ip,user,passw, masterurl):
        self.host = ip
        self.user = user 
        self.passw = passw
        print()
        print("Verificación de configuración \n")
        
        # Otra de las opciones es con la instalación de YANGEXPLORER: https://github.com/CiscoDevNet/yang-explorer
        ssh = paramiko.SSHClient()
        ssh.connect(self.host, port=22, username = self.user, password = self.passw)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        stdin,stdout, stderr = ssh.exec_command('show platform yang-management process')
        output = stdout.readlines()
        #type(output)
        print("\n".join(output))

        self.masterurl = "https://"+self.host+"/resconf/data/ietf-interfaces:interfaces/"
        
    # Método para ver las interfaces de red.
    def view_interfaces():
        print("Interfaces de red. \n")
        # Comando de consola para ver las interfaces de red
        stdin,stdout, stderr = ssh.exec_command("show ip interface brief")
        output = stdout.readlines()
        print("\n".join(output))

    # Método para crear una interfaz nueva
    def new_interface(self):
        print("Nueva interfaz de red.")
        # Pedimos los datos necesarios:
        # 1- Tipo de interfaz
        # 2- Nombre de la interfaz
        # 3- IP
        # 4- Máscara de red
        # 5- Descripción de la nueva interfaz
        while True:
            # URL de conexión al Router
            url = masterurl
            # print("La URL a la que voy a consultar es: ",url, "\n")
            # Pedimos los datos de la nueva interfaz
            tipo = input("¿Qué tipo de interfaz es? (Loopback, FastEthernet,...) ")
            name = input("¿Qué nombre asigno a la nueva interfaz? ")
            ip = input("¿Qué IP assigno a la interfaz? ")
            mask = input("¿Qué máscara de red tiene la interfaz? ")
            add = input("¿Añadimos algo de descripción? (Y/N) - Sino, añado una por default: ")
            add.lower
            if add == 'Y':
                description = input("¡Cuéntame! ¿Qué descripción añado? ")
            else:
                description = "Interfaz: {:2}-{:2}/{:2}".format(name,ip,mask)
                print("Descripción por defaut: {:2}".format(description))
            # Creamos la nueva interfaz
            conecta = url+"/interface="+name
            print("\n URL a la que nos conectamos es: {:2}".format(conecta)+"\n\n")
            
            m = manager.connect(
                host=self.host,
                port=830,
                username=self.user,
                password = self.passw,
                hostkey_verify = False 
            )

            netconf_reply = manager.get_config(source="running")
            #print(netconf_reply)

            # QUEDA FEO PERO FEO FEO - PERO FUNCIONA
            netconf_data ='<config> \n \t <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"> \n',2*"\t","<interface> \n", 3*"\t"," <{:2}> \n".format(tipo),4*"\t","<name>{:2}</name> \n".format(name),4*"\t","<description>{:2}</description> \n".format(description),4*"\t","<ip> \n",5*"\t","<address> \n",6*"\t","<primary> \n",7*"\t","<address>{:2}</address> \n".format(ip),7*"\t","<mask>{:2}</mask> \n".format(mask),6*"\t","</primary> \n",5*"\t","</address> \n",4*"\t","</ip> \n",3*"\t"," <{:2}> \n".format(tipo),2*"\t","</interface> \n","\t </native> \n","</config> \n"
            
            netconf_reply = m.edit_config(target="running", config = netconf_data)
            print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

    # Método para borrar una interfaz de red del router.
    def delete_interface(self):
        print("Borrar interfaz de red.")
        # Pasos:
        # 1 - Solicito la interfaz que quiero borrar
        # 2 - Creo la cabecera del archivo o headers
        # 3 - Inicio sesion con las credenciales de usuario
        # 4 - Genero la conexión para borrar la interfaz 
        # 5 - Muestro por pantalla el resultado
        
        # URL 
        laborro = input("¿Qué interfaz borro? ")
        url = self.masterurl+"interface={}".format(laborro)
        # header 
        headers = {
            "Accept":"application/yang-data+json",
            "Content-Tpe":"application/yang-data+json"
        }
        # Authentication credentiales
        basic_auth = (self.user, self.passw)
        # Generate connexion
        respuesta = requests.delete(url, auth= basic_auth, headers = headers, verify = False)
        response_json = respuesta.json()
        print(json.dumps(response_json, indent = 2))
    
    # Método para ver la tabla de rutas.
    def table_route(self):
        print("Crear tabla de rutas")
        print("Ver ORIGEN - DESTINO -  INTERFAZ DE SALIDA - ")

    # Método para ver archivos yang Cisco
    def yang_files(self):
        print("Menú de archivos YANG que ver/configurar.")

def credencial():
    # Solicito los datos necesarios para realizar el menú correctamente
    # IP router
    ip = input("Introduzca la dirección IP del Router Cisco 1000v: ")
    puerto = int(input("Puerto de conexión: (En mi caso: 830, por default: 22) "))
    print("Credenciales para {:2}.".format(ip))
    # Usuario
    user = input ("Introduzca el usuario login del sistema: ")
    # Contraseña
    key = input ("Introduzca la contraseña de acceso: ")
    # Conexión SSH al Router.
    try:
        clienteSSH = ConnectHandler(device_type='cisco_ios', host=ip, port=puerto, username=user, password=key)
        clienteSSH.disconnect()
    except Exception as err:
        print("Imposible conectarse al Router con la IP: {:2} \nCompruebe los datos y vuelva a intentarlo de nuevo.".format(ip))
        sys.exit()

# Defino clase que se ejecuta en caso de seleccionar una opcion inexistente o inválida          
def default():
    print("OPCION INVÁLIDA! - Revise las opciones y vuelva a intentarlo")    
# Función para salir del programa    
def salir():
    os.system('clear')
    os.system('cls')
    print("Espero que mi trabajo te ayude en el tuyo. \n Adiós!")
    time.sleep(5)
    exit()
# Función principal
def main():
    # Solicitamos datos
    credencial
    opcion = input("""

        Hola y bienvenid@!

        Este es un script de ayuda para sacar información del Router Cisco Serie 1000.
        Las opciones de este script son:
            - Listado de interfaces con información relevante.
            - Creación de interfaces de red.
            - Borrar una interfaz de red.
            - Ver la tabla de rutas.
            - Peticiones a módulos YANG compatibles.
                - Configuración.
                - Obtener información del dispositivo.
        Para ver todos los ejercicios resueltos ver la carpeta  'Model Driven Programmability - DevNet20'

        [ Cuando esté list@ pulse ENTER para continuar.]
        ____________________________________________________________________________________
        @Author: Paulino E. Bermúdez
        - Cisco Netacad: https://www.netacad.com/
        - PUE: https://www.pue.es/
        @Versión: 2020.
    """)
    api = conectaRouter()
    # Creamos un diccionario para el menu de opciones
    opciones = {
        1:api.view_interfaces,
        2:api.new_interfaces,
        3:api.delete_interfaces,
        4:api.routing_table,
        5:api.get_peticion_yang,
        0:salir
    }

    while opcion != 0:
        os.system('clear')
        os.system('cls')
        print("""
        SCRIPT DE AYUDA OBTENER INFO. - Router Cisco 1000v

        Selecciones una de las opciones:
        +_________________________________________________+
        | 1- Ver interfaces red.                          |
        | 2- Crear nueva interfaz de red.                 |
        | 3- Borrar interfaz de red.                      |
        | 4- Ver tabla de rutas guardadas.                |
        | 5- Realizar solitudes a los archivos YANG.      |
        +_________________________________________________+
        | 0- Salir del programa.                          |
        +_________________________________________________+

        (*) Revisar.
        """)
        try:
            opcion = int(input("Escriba una opción: "))
        except:
            dict.get(opcion.default)()
# Ejecución de programa principal
if __name__ == "__main__":
    main()