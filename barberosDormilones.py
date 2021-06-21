from threading import Thread, Lock, Event, Semaphore
import time, random

mutex = Semaphore(1)
waitingCoustumers = []
asientos = 3
clientes = []

class Cliente: 
    def __init__(self,name):
        self.name = name

class Barber:
    barberWorking = Event() #creamos un evento que se encargara de monitorear la actividad del barbero

    def durmiendo(self):
        self.barberWorking.wait() #se bloquea hasta que una bandera interna se active
    
    def despierto(self):
        self.barberWorking.set() #se activa la bandera interna y se inicia
    
    def cortandoCabello(self,cliente):
        self.barberWorking.clear() #el barbero está ocupado

        print("Cortandole el cabello al cliente: {0}".format(cliente.name)) 
        tiempoDecorte = random.randrange(5,15) #el tiempo puede variar entre 5  15 segundos entre cada corte
        time.sleep(tiempoDecorte)
        
        print(">>>{0} se terminó de cortar el cabello".format(cliente.name))

barbero = Barber() #creamos una instancia del babrero

def Cortandocabello():
    while True:
        mutex.acquire()

        if len(waitingCoustumers) > 0:
            c = waitingCoustumers[0]
            del waitingCoustumers[0]
            mutex.release()
            barbero.cortandoCabello(c)
        else:
            mutex.release()
            print("El barbero está durmiendo")
            barbero.durmiendo()
            print("Barbero se despertó")

def clienteNuevo(cliente):
    mutex.acquire()
    print(">>El cliente: {0} llego a la barberia".format(cliente.name))

    if len(waitingCoustumers) == asientos:
        print('-El cuarto de espera ya está lleno, {0} se retira de la barberia'.format(cliente.name))
        mutex.release()
    else:
        print('>>>{0} se sentó en el cuarto de espera'.format(cliente.name))
        waitingCoustumers.append(cliente)
        mutex.release()
        barbero.despierto()

def comenzadoATrabajar():
    hilo = Thread(target = Cortandocabello)
    hilo.start()


def generaNombres():
    archivo = open("nombres.txt","r") #modificar la dirección en caso de ser necesario
    nombres = archivo.readlines()    
    valores = random.randrange(30)
    for i in range(valores):
        nombre = nombres[random.randrange(900)]
        nombreLmp = nombre.replace("\n","")
        clientes.append(Cliente(nombreLmp))


if __name__ == '__main__':
    print("La barbería ah abierto")
    generaNombres()
    comenzadoATrabajar()

    while len(clientes) > 0:
        c = clientes.pop()
        #Nuevo cliente entra a la barbershop
        clienteNuevo(c)
        time.sleep(random.randrange(3,7))


