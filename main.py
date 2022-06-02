from threading import Thread, Lock, Event
import time, random

mutex = Lock()# para que no se pueda acceder a la barberia mientras se esta cortando el pelo

#Interval in seconds
customerIntervalMin = 5
customerIntervalMax = 15
haircutDurationMin = 3
haircutDurationMax = 15

class BarberShop:
	waitingCustomers = []

	def __init__(self, barber, numberOfSeats):
		self.barber = barber
		self.numberOfSeats = numberOfSeats
		print ('BarberShop iniciado con {0} sitios'.format(numberOfSeats))
		print ('Mínimo intervalo de Clientes {0}'.format(customerIntervalMin))
		print ('Máximo intervalo de Clientes {0}'.format(customerIntervalMax))
		print ('Tiempo mínimo de corte de pelo {0}'.format(haircutDurationMin))
		print ('Tiempo máximo de corte de pelo {0}'.format(customerIntervalMax))
		print ('---------------------------------------')

	def openShop(self):
		print ('La barbería se está abriendo')
		workingThread = Thread(target = self.barberGoToWork)#declaramos un hilo para que el barbero trabaje
		workingThread.start()#iniciamos el hilo del barbero

	def barberGoToWork(self):
		while True:
			mutex.acquire()#bloqueamos hasta que suceda el release

			if len(self.waitingCustomers) > 0:
				c = self.waitingCustomers[0]#cogemos al primer cliente y lo eliminamos de la lista
				del self.waitingCustomers[0]
				mutex.release()
				self.barber.cutHair(c)#hacemos que el barbero le corte el pelo al cliente escogido
			else:
				mutex.release()
				print ('Aaah, terminado, yendo a dormir')
				barber.sleep()
				print ('El barbero se ha despertado')

	def enterBarberShop(self, customer):
		mutex.acquire()
		print ('>> {0} entró en la tienda y está buscando un sitio'.format(customer.name))

		if len(self.waitingCustomers) == self.numberOfSeats:
			print ('La sala de espera está llena, {0} se va a marchar.'.format(customer.name))
			mutex.release()
		else:
			print ('{0} se ha sentado en la sala de espera'.format(customer.name))
			self.waitingCustomers.append(c)
			mutex.release()
			barber.wakeUp()#Despertamos al barbero

class Customer:
	def __init__(self, name):
		self.name = name#Creamos un Cliente que solo necesita su nombre

class Barber:
	barberWorkingEvent = Event()#El barbero se crea un evento que es cuando está trabajando

	def sleep(self):
		self.barberWorkingEvent.wait()#Definimos que si se duerme entonces el evento se para

	def wakeUp(self):
		self.barberWorkingEvent.set()#Definimos que si se despierta entonces el evento se activa

	def cutHair(self, customer):
		#Set barber as busy
		self.barberWorkingEvent.clear()#Se limpia el evento

		print ('A {0} le están cortando el pelo'.format(customer.name))

		randomHairCuttingTime = random.randrange(haircutDurationMin, haircutDurationMax+1)
		time.sleep(randomHairCuttingTime)#ponemos un tiempo aleatorio que tardará en cortar el pelo
		print ('{0} ha terminado'.format(customer.name))


if __name__ == '__main__':
	customers = []
	customers.append(Customer('Sara'))
	customers.append(Customer('Carlota'))
	customers.append(Customer('María'))
	customers.append(Customer('Alex'))
	customers.append(Customer('Andrea'))
	customers.append(Customer('Javi'))
	customers.append(Customer('Raúl'))
	customers.append(Customer('Rubén'))
	customers.append(Customer('Lorenzo'))
	customers.append(Customer('David'))
	customers.append(Customer('Pepe'))
	customers.append(Customer('Pedro'))
	customers.append(Customer('Paco'))
	customers.append(Customer('Juan'))
	customers.append(Customer('Tomas'))
	customers.append(Customer('Lara'))
	customers.append(Customer('Ana'))

	barber = Barber()

	barberShop = BarberShop(barber, numberOfSeats=1)
	barberShop.openShop()

	while len(customers) > 0:
		c = customers.pop()#Cogemos un cliente y lo eliminamos de la lista
		#New customer enters the barbershop
		barberShop.enterBarberShop(c)#el cliente c entra a la barbería
		customerInterval = random.randrange(customerIntervalMin,customerIntervalMax+1)
		time.sleep(customerInterval)
