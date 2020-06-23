#Parametros de conexion
#"157.245.82.242"
MQTT_HOST = "167.71.243.238"
MQTT_PORT = 1883

#MQTT_USER = "pr24"
#MQTT_PASS = "Patito!#2020"
MQTT_USER = "proyectos"
MQTT_PASS = "proyectos980"
arch = 'Archivos.tex'

#Credenciales
#Se acostumbra solicitar al usuario que ingrese su user/pass
#no es buena practica dejar escritas en el codigo las credenciales
def read(a):
    LISTADO = a
    datos = []
    archivo = open(LISTADO, 'r')
    registro = archivo.readlines()
    for i in range(len(registro)):
        datos.append(registro[i].replace('\n', '') ) 
    archivo.close()
    return datos
datos = read(arch)
usuario = datos[1]
sala1= datos[3]
sala2= datos[4]


#comaistrondos
FTR = b'\x03'       #audio
ALIVE = b'\x04'     #alive
ACK = b'\x05'
#OK = b'\x06'
#NO = b'\x07'
SEPARADOR = b'$'
#destinos o topics de subscripcion
qos = 0
user1 = 201612625   #titus
user2 = 201612146   #sebas
user1_t = b'201612625'   #titus
user_t =datos[1].encode()  #sebas
GRUPO = 24
test = ('test',qos)
#mensaje
topic_user2 = 'usuarios/'+str(GRUPO)+'/'+str(user1)
#alive
topicComandos_alive = 'comandos/'+str(GRUPO)
tramaALIV = ALIVE+user1_t  
#salas
topic_sala1 = 'salas/'+str(GRUPO)+'/'+sala1
topic_sala2 = 'salas/'+str(GRUPO)+'/'+sala2
#subs
SUBS_comandos2 = 'audios/'+str(GRUPO)+'/'+str(usuario)
SUBS_comandos = ('comandos/'+str(GRUPO)+'/'+str(usuario), qos)
SUBS_audio = ('audios/'+str(GRUPO)+'/'+ str(usuario), qos)
SUBS_usuario = ('usuarios/'+str(GRUPO)+'/'+str(usuario), qos)
SUBS_usuario2 = ('usuarios/'+str(GRUPO)+'/'+str(user1), qos)
SUBS_sala1 = ('salas/'+ str(GRUPO)+'/'+sala1, qos)
SUBS_sala2 = ('salas/'+ str(GRUPO)+'/'+sala2, qos)
#tramas de comandos
trama_ACK = ACK+user_t

#audio
PUBL_audios_us =  'audios/'+str(GRUPO)+'/'+str(user1)
PUBL_audios_sal1= 'audios/'+str(GRUPO)+'/'+str(sala1)
PUBL_audios_sal2= 'audios/'+str(GRUPO)+'/'+str(sala2)




#class comandos (object):
class comandos(object):
    def __init__(self, data = []):
        self.data = list(data)

    #La "longitud" del objeto, es en realidad representado
    #por la cantidad de datos de su lista principal
    def __len__(self):
        return len(self.data)
    def __str__(self):
        return str(self.data)

    def comp (self,i,e):
        if  len(self.data) != i:
            e += 1
            i+=1
            if e <= 3:
                ALIVE_PERIOD = 0.1
                return ALIVE_PERIOD,i,e
        if len(self.data) ==i:
            ALIVE_PERIOD = 2
            return ALIVE_PERIOD,i,e
    #Representacion cuando se invoca el objeto sin casting a STRING.
    def __repr__(self):
        return self.__str__()

