import paho.mqtt.client as paho
import paho.mqtt.client as mqtt
import logging
import time
import random
import threading #Concurrencia con hilos
import sys 
import os 
#from mqttTestSubscription import *
from brokerData import* #Informacion de la conexion

'''
Ejemplo de cliente MQTT: gateway de red de sensores
'''
LOG_FILENAME = 'mqtt.log'
os.remove("mqtt.log")

#Configuracion inicial de logging
logging.basicConfig(
    level = logging.INFO, 
    format = '[%(levelname)s] (%(processName)-10s) %(message)s'
    )
      
#Tiempo de espera entre lectura y envio de dato de sensores a broker (en segundos)


#mensaje de alive cada 2 segundos
'''
def alive(ALIVE_PERIOD):
  # se envia un menaje cada 2 segundos indicando que sigue conectado
    client.publish(SUBS_comandos2 , tramaALIV, qos = 0,retain = False)
    time.sleep(ALIVE_PERIOD)
'''
def play():
    os.system('aplay audio_s.wap')

#Handler en caso suceda la conexion con el broker MQTT
def on_connect(client, userdata, flags, rc): 
    client.subscribe([SUBS_comandos,SUBS_usuario,SUBS_sala1,SUBS_sala2,SUBS_audio])

#Handler en caso se publique satisfactoriamente en el broker MQTT

def on_publish(client, userdata, mid): 
    publishText = "Publicacion satisfactoria"
    logging.debug( str(publishText) )


def on_message(client, userdata, msg):
    #Se muestra en pantalla informacion que ha llegado
    if SUBS_comandos2 == str(msg.topic):
        archivo = open('audio_s.wap', 'wb')
        archivo.write(msg.payload)
        hil ()
    else:
        logging.info("Ha llegado el mensaje al topic: " + str(msg.topic))
        logging.info("El contenido del mensaje es: " + str(msg.payload))
        #Y se almacena en el log
        filename= 'mqtt.log'
        archivo = open(filename,'a') #Abrir para SOBREESCRIBIR el archivo existente
        archivo.write(str(msg.topic) +  '-> ' + str(msg.payload) +'\n')
        archivo.close()


logging.info("Cliente MQTT con paho-mqtt") #Mensaje en consola

'''
Config. inicial del cliente MQTT
'''
client = paho.Client(clean_session=True) #Nueva instancia de cliente
client.on_connect = on_connect #Se configura la funcion "Handler" cuando suceda la conexion
client.on_publish = on_publish #Se configura la funcion "Handler" que se activa al publicar algo
client.on_message = on_message #Se configura la funcion "Handler" que se activa al llegar un mensaje a un topic subscrito
client.username_pw_set(MQTT_USER, MQTT_PASS) #Credenciales requeridas por el broker
client.connect(host=MQTT_HOST, port = MQTT_PORT) #Conectar al servidor remoto


client.loop_start()


#hilo alive

def hil ():
    t1 = threading.Thread (name = 'verificacion',
                                target = play,
                                daemon = True
                                )

    t1.start()
    t1.join()

#Loop principal: leer los datos de los sensores y enviarlos al broker en los topics adecuados cada cierto tiempo
try:
    while True:
        print('1. Enviar texto')
        print('2. Enviar mensaje de voz')
        print('3. Salir')
        x = input('-:')
    #vemos que hacción hacer y a quien enviarlo
        #enviar mensaje 
        if x == '1' :  #usurio 1
            print('a. Enviar a usuario')
            print('b. Enviar a sala')
            t = input('-:')
            if t == 'a':
                print('1. 201612625')
                print('2. ---')
                t = input('-:')
                if x == '1' :
                    t = input('escriba el texto:  ')
                    trama = user_t + SEPARADOR + t.encode() #codifica el mensaje 
                    #enviamos el mensaje
                    client.publish(topic_user2, trama, qos = 0,retain = False)
                else:
                    t = 0
                    x= 0
            if t == 'b':
                print('1. 24S15')
                print('2. 24S11')
                t = input('-:')
                if x == '1' :
                    t = input('escriba el texto:  ')
                    trama = user_t + SEPARADOR + t.encode() #codifica el mensaje 
                    #enviamos el mensaje
                    client.publish(topic_sala1 , trama, qos = 0,retain = False)
                if x == '2' :
                    t = input('escriba el texto:  ')
                    trama = user_t + SEPARADOR + t.encode() #codifica el mensaje 
                    #enviamos el mensaje
                    client.publish(topic_sala2, trama, qos = 0,retain = False)
        if x == '2':
            print('elija la duración del audio')
            t = int(input('-:'))
            os.system('arecord -d {!r} -f U8 -r 8000 audio_p.wap'.format(t))
            f = open("audio_p.wap", "rb")
            imagestring = f.read()
            f.close()
            trama_audio = bytearray(imagestring)
            print('Enviar a')
            print('1. sala')
            print('2. usuario')
            x = input('-:')
            if x == '1' :   
                print('Enviar a')
                print('1. sala1')
                print('2. usala2')
                t = input('-:')
                if t == '1':
                    client.publish(PUBL_audios_sal1,trama_audio , qos = 0,retain = False)
                if t == '2':
                    client.publish(PUBL_audios_sal2,trama_audio , qos = 0,retain = False)
            if x == '2':
                client.publish(PUBL_audios_us,trama_audio , qos = 0,retain = False)
             
        if x == '3':
            logging.warning("Desconectando del broker MQTT...")
            client.loop_stop()
            #if t1.isAlive():
             #   t1._stop()
            break
        else:
            print('numero incorrecto')
except KeyboardInterrupt:
    logging.warning("Desconectando del broker MQTT...")
    client.loop_stop()
    #if t1.isAlive():
     #   t1._stop()

finally:
    client.disconnect()
    logging.info("Se ha desconectado del broker. Saliendo...")