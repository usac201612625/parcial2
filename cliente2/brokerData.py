#Parametros de conexion
#"157.245.82.242"
MQTT_HOST = "167.71.243.238" #GDTA DIRECCION DEL BROKER
MQTT_PORT = 1883 #GDTA PUERTO DEL BROKER

#MQTT_USER = "pr24" 
#MQTT_PASS = "Patito!#2020"
MQTT_USER = "proyectos" #GDTA NOMBRE DE USUARIO 
MQTT_PASS = "proyectos980" #GDTA CONTRASEÑA
arch = 'Archivos.tex' #GDTA ARCHIVO CON LOS USUARIOS: CARNET Y SUS SALAS

#Credenciales
def read(a): #SMC FUNCION QUE LEE LOS USUARIOS Y LAS SALAS, DEVUELVE ESOS DATOS
    LISTADO = a
    datos = []
    archivo = open(LISTADO, 'r')
    registro = archivo.readlines()
    for i in range(len(registro)):
        datos.append(registro[i].replace('\n', '') ) 
    archivo.close()
    return datos
datos = read(arch) #GDTA SE GUARDA EN DATOS LOS NO.CARNETS Y LAS SALAS
usuario = datos[1]
sala1= datos[3]
sala2= datos[4] 


#comaistrondos
FTR = b'\x03'       #SMC audio INSTRUCCION 
ALIVE = b'\x04'     #SMC alive INSTRUCCION 
ACK = b'\x05'       #SMC ACK  ACEPTADO
#OK = b'\x06'        
#NO = b'\x07'
SEPARADOR = b'$'   #SMC CARACTER QUE SEPARA LOS DATOS DEL TOPIC
#destinos o topics de subscripcion
qos = 0     #SMC NIVEL DE QUALITY OF SERVICE
user1 = 201612625   #titus
user2 = 201612146   #sebas
user1_t = b'201612146'   #titus
user_t =datos[1].encode()  #sebas
GRUPO = 24       #SMC NO.GRUPO
test = ('test',qos) #SMC TEST DE PRUEBA
#SMC SE ORDENAN LOS MENSAJES Y TOPICS mensaje
topic_user2 = 'usuarios/'+str(GRUPO)+'/'+str(user2)
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
SUBS_usuario2 = ('usuarios/'+str(GRUPO)+'/'+str(user2), qos)
SUBS_sala1 = ('salas/'+ str(GRUPO)+'/'+sala1, qos)
SUBS_sala2 = ('salas/'+ str(GRUPO)+'/'+sala2, qos)
#tramas de comandos
trama_ACK = ACK+user_t

#GDTA SE ARMAN LAS TRAMAS DE audio
PUBL_audios_us =  'audios/'+str(GRUPO)+'/'+str(user2)
PUBL_audios_sal1= 'audios/'+str(GRUPO)+'/'+str(sala1)
PUBL_audios_sal2= 'audios/'+str(GRUPO)+'/'+str(sala2)

#SMC class comandos (object): CLASE COMANDO SE REPRESENTA EL TAMAÑO 
#DEL DATO A ENVIAR, CON LA CARACTERÍSTICA DE ENVIAR EL ALIVE POR EL HILO
class comandos(object):
    def __init__(self, data = []):
        self.data = list(data)

    #SMC La "longitud" del objeto, es en realidad representado
    #SMC por la cantidad de datos de su lista principal
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
    #SMC Representacion cuando se invoca el objeto sin casting a STRING.
    def __repr__(self):
        return self.__str__()

