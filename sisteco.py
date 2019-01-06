import random
import time
import matplotlib.pyplot as plt

archivos = []
def menu():
    #Muestra el menu principal y usando input se pide al usuario que ingrese la opcion que desea ejecutar
    option = 0
    while option == 0:
        print('Menu Principal')
        print('Opciones:')
        print('1) Encriptar')
        print('2) Pruebas de rendimiento')
        print('3) Salir')
        user_input = input('Ingrese el numero de la opcion que desea ejecutar: ')
        if user_input=="3":
            #se retorna y finaliza el programa
            return 0
        elif user_input=="1":
            llave = getKey()
            plainText = input("Ingrese texto a codificar: ")
            bloques = recibirBloques()
            llaveAscii = stringToAscii(llave)        	
            
            textoAscii = stringToAscii(plainText)
            start_time = time.time()
            cifBloque = cifradoEnBloque(textoAscii, llaveAscii, bloques)
            descBloque = descifradoEnBloque(cifBloque, llaveAscii, bloques)
            print("Palabra descifrada: "+ asciiToString(descBloque))
            exec_time = (time.time() - start_time)
            print("Tiempo de cifrado: %s segundos" % exec_time)
            throughput = bloques/(time.time() - start_time)
            print("Throughput: %s" % throughput)
        elif user_input == "2":
            rendimiento()
        else:
            print('Ingrese una opcion correcta')
            
    return
 
def rendimiento():
	key = randomWord(32)
	word = randomWord(64)
	print("Llave a utilizar: %s" % key)
	print("Palabra a encriptar: %s" % word)
	llaveAscii = stringToAscii(key)        	
	textoAscii = stringToAscii(word)
	sizeBloques = [1,4,8,16]
	tiempos = []
	throughputs = []
	for size in sizeBloques:
		start_time = time.time()
		cifBloque = cifradoEnBloque(textoAscii, llaveAscii, size)
		exec_time = (time.time() - start_time)
		throughput = size/(time.time() - start_time)
		print("Tiempo de cifrado (tamaño " + str(size) + "): %s segundos" % exec_time)
		print("Throughput (tamaño " + str(size) + "): %s" % throughput)
		tiempos.append(exec_time)
		throughputs.append(throughput)

	graficar("Tiempo de ejecucion encriptacion","Tamaño de bloque", "Tiempo [s]", sizeBloques, tiempos)
	graficar("Throughput encriptacion", "Tamaño de bloque", "Throughput", sizeBloques, throughputs)

def graficar(title,xlabel,ylabel,x,y):
	print("Mostrando grafico...")
	plt.title(title)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
	plt.plot(x,y,"-")
	plt.show()

	

def second_menu(archivos):
	textoCifrado = []
	textoDescifrado = []
	for i in archivos:
		key, tamanio = getKey()
		llave = stringToAscii(key)
		print(i)
		print("uwu")
		#print(i.read())
		texto = i.readlines()
		for j in range(0, len(texto)):
			texto[j] = texto[j].strip('\n\r\0')
		print(texto)
		#print("owo")
		textoCifrado +=cifrado(stringToAscii(texto[0]), llave)
		print("archivo completo cifrado: ")
		print(asciiToString(textoCifrado))
		textoDescifrado +=descifrar(textoCifrado, llave)
		print("archivo completo descifrado")
		print(asciiToString(textoDescifrado))
		
	
#Entradas: recibe texto plano y llave
#Funcionamiento: cifra el texto plano utilizando la funcion codificar(), luego lo codificar en dos ciclos utilizando porciones de la llave, finalmente lo vuelve a codificar
#Salidas: retorna el resultado de la ultima codificacion	
def cifrado(plainText, key):
	contador = 0
	offset = 0
	codificado = []
	iteraciones = 0
	arreglo = []
	plainText2 = plainText[:]
	codificado = codificar(plainText2, key, 0) #se codifica el texto con la llave original
	contador = 0
	corrimiento = 1
	keys = []
	iteraciones = len(key)/2
	while contador < iteraciones:
		newKey = key[offset:corrimiento*2]#se particiona la clave en bloques de 2
		keys.append(list(newKey))
		codificado = codificar(codificado, newKey, 0)#se vuelve a cifrar pero con la llave parcial, que consiste en 2 elementos de la llave original
		offset+=2
		contador+=1
		corrimiento+=1
	contador = 0
	offset = 0
	corrimiento = 0
	codificado = codificado[::-1]#se invierte el texto cifrado
	for llaveParcial in keys:
		codificado = codificar(codificado, llaveParcial, 0)#se vuelve a cifrar con porciones de las llaves
	codificado = codificar(codificado+arreglo,key,0)#se cifra una ultima vez con la llave original
	return codificado
	
#Entradas: texto plano y llave original
#Funcionamiento: implementa un cifrado vigenere utilizando como alfabeto numeros del 0 al 127 que pertenecen a la codificacion ascii
#Salidas: texto cifrado
def codificar(plainText, key, offset):
	codificado = plainText[:]
	newKey = []
	contador = 0
	for cont in range(0, len(plainText)):#se inicia un ciclo que recorre todo el texto plano
		if contador == len(key):
			contador = 0#si ya se recorrio la llave completamente, se vuelve al inicio de esta
		if codificado[cont]+key[contador]>=127:
			codificado[cont] = (codificado[cont] + key[contador])%(127)#se suma la llave en la posicion "cont" con el texto plano en la posicion "cont"
			newKey.append(codificado[cont])
			contador +=1
		else:
			codificado[cont] = (codificado[cont] + key[contador])+1#se suma la llave en la posicion "cont" con el texto plano en la posicion "cont"
			newKey.append((codificado[cont]))
			contador+=1
	return codificado
#Entradas: Texto cifrado y llave original
#Funcionamiento: sigue el mismo algoritmo que la funcion cifrado(), pero a la inversa
#Salidas: texto descifrado
def descifrar(cipherText, key):
	cipherText = decodificar(cipherText,key,0)#se decodifica el texto utilizando la llave original
	offset = 0
	iteraciones = len(key)/2
	contador = 0
	offset = 0
	decodificado = []
	keys = []
	arreglo = []
	decodificado = cipherText[:]
	keys = key
	offset = len(keys)
	while contador < int(iteraciones):
		newKey = keys[offset-2:offset]#se recorre la llave de 2 en 2
		offset -= 2
		contador += 1
		decodificado = decodificar(decodificado, newKey, 0)#utilizando estas llaves parciales, se decodifica
	offset = len(keys)
	contador = 0
	decodificadoR = decodificado[::-1]#se invierte el sentido del texto parcial decodificado
	while contador < int(iteraciones):#se repite proceso anterior con llaves parciales
		newKey = keys[offset-2:offset]
		offset -= 2
		contador += 1
		decodificadoR = decodificar(decodificadoR, newKey, 0)
	decodificadoR = decodificar(decodificadoR, key, 0)#se decodifica una ultima vez con llave original
	return decodificadoR
	
#Entradas: texto cifrado y llave original
#Funcionamiento: se decodifica el vigenere simple implementado en funcion codificar
#Salidas: texto decodificado
def decodificar(cipherText, key, offset):
	decodificado = cipherText[:]
	newKey = []
	contador = 0
	if(len(key)<1):
		return decodificado
	if offset*len(key)>=len(decodificado):
		return decodificado
	for cont in range(0, len(decodificado)):
		if cont+offset*len(key)>=len(decodificado):
			return decodificado
		if contador== len(key):
			contador = 0
		if decodificado[cont]-key[contador]>=0:
			newKey.append(decodificado[cont])
			decodificado[cont] = (decodificado[cont] - key[contador]-1)%(128)
			contador+=1
		else:
			newKey.append(decodificado[cont])
			decodificado[cont] = (decodificado[cont] - key[contador]+128-1)%128
			contador+=1
	offset+=1
	return decodificado

def stringToNumber(string, alfabeto):
	asciiArray = []
	for char in string:
		asciiArray.append(alfabeto.index(char))
	return asciiArray
def numberToString(numberArray, alfabeto):
	string = ''.join(alfabeto[element] for element in numberArray)
	return string
#Entradas: recibe un string
#Funcionamiento: recorre el string y cada elemento lo transforma a su numero ascii correspondiente
#Salida: arreglo de int entre 0 y 127
def stringToAscii(string):
	asciiArray = []
	for char in string:
		asciiArray.append(ord(char))
	return asciiArray
#Entradas: arreglo de int con numeros entre 0 y 127
#Funcionamiento: recorre arreglo de int y lo transforma a un string utilizando codificacion ascii
#Salida: string ascii
def asciiToString(asciiArray):
	string = ''
	string = ''.join(chr(int(element)) for element in asciiArray)
	return string
	
#Funcionamiento: pide una llave al usuario que no sea mayor a 64 caracteres, si es menor a 64 caracteres se rellena con letras al azar
#Salida: String de llave de 64 caracteres
def getKey():
	largo = 0
	while largo == 0 or largo > 64:
		key = input("Ingrese key que desee usar (cualquier cadena de caracteres ascii entre 1 a 64 de longitud): ")
		largo = len(key)
	word = randomWord(64-largo)
	print(key+word)
	return key+word
#Entradas: recibe dos string y ademas un identificador tipo
#Funcionamiento: segun "tipo" distingue si se le ingresa una llave o un texto cifrado, alcula la diferencia entre ambos
#Salida: retorna un contador y el porcentaje de diferencia
def analizarDif(key1, key2, tipo):
	contador = 0
	largo = 0
	if len(key1) > len(key2):
		largo = len(key2)
	else:
		largo = len(key1)
	for i in range(0, largo):
			if key1[i] != key2[i]:
				contador = contador + 1
	pDiferencia = 100*contador/largo
	if tipo == 2:
		return contador
	elif tipo == 1:
		return contador
	else:
		return contador, pDiferencia
#Entrada: dos textos planos, dos llaves y dos textos cifrados
#Funcionamiento: calcula la avalancha entre dos textos cifrados provenientes de textos planos distintos
#Salida: imprime por pantalla si se cumple o no avalancha
def avalancha(plainText1, plainText2, key1, key2, cifrado1, cifrado2):
	contador = 0
	if plainText1 == plainText2 and (key1 == key2):#si todo es igual, no se cumplira avalancha por lo tanto se retorna
		print("Textos planos y llaves son iguales")
		return
	elif plainText1 == plainText2 and key1 != key2:
		print("Textos planos iguales, llaves son distintas")#reconoce que las llaves son diferentes
		diferenciaKeys = analizarDif(key1, key2, 2)#calcula la diferencia entre las llaves
		diferenciaCifrado, pCifrado = analizarDif(cifrado1, cifrado2, 3)#calcula la diferencia entre los textos cifrados resultantes de las llaves
		if pCifrado >= 50.0:
			print("Se cumple avalancha")
		else: 
			print("No se cumple avalancha")
	elif plainText1 != plainText2 and key1 == key2:#llaves iguales pero textos planos distintos
		print("Textos planos distintos, llaves iguales")#se repiten pasos de caso anterior
		diferenciaTextos = analizarDif(plainText1, plainText2, 1)
		diferenciaCifrado, pCifrado = analizarDif(cifrado1, cifrado2, 3)
		if pCifrado >= 50.0:
			print("Se cumple avalancha")
		else: 
			print("No se cumple avalancha")
	else:
		print("Llave y textos son distintos")#caso en que tanto llaves y textos planos son distintos
		diferenciaTextos = analizarDif(plainText1, plainText2, 1)#se repiten pasos de casos anteriores
		diferenciaKeys = analizarDif(key1, key2, 2)
		diferenciaCifrado, pCifrado = analizarDif(cifrado1, cifrado2, 3)
		if pCifrado >= 50.0:
			print("Se cumple avalancha")
		else: 
			print("No se cumple avalancha")
	return 0;
#Entrada: tamaño
#Funcionamiento: en el rango del tamaño ingresado, crea una palabra con strings aleatorios 
#salida: palabra aleatoria
def randomWord(size):
	line = ''
	for c in range(size):

		randomChar = chr(random.randint(33,126))
		line += randomChar
	return line

#Funcionamiento: crea un archivo de prueba con "x" lineas, se utiliza para calcular la avalancha average del algoritmo de cifrado
#Salida: se escriben "x" lineas en el archivo de prueba
def crearArchivoPrueba():
	print("Creando archivo de prueba...")
	archivoPrueba = open('texto.test','w')
	for i in range(100):
		lineSize = random.randint(10,50)
		line = randomWord(lineSize)
		if i < 99:
			line += '\n'
		archivoPrueba.write(line)
	archivoPrueba.close()

#Funcionamiento: se lee el archivo creado por crearArchivoPrueba, se generan llaves iguales. En cada iteracion se crea una copia de la linea leida por el archivo, se cambia al azar solo un elemento
#y se cifra, luego a los dos resultados se le calcula la avalancha y el valor resultante se acumula
#finalmente, en base al acumulador de avalanchas se obtiene un average
#Salidas: porcentaje de avalancha average y contador de cifrados-descifrados correctos
def averageAvalancha():
	archivo = open("texto.test","r")
	keySize = 64
	key = randomWord(keySize)
	keyAscii = stringToAscii(key)
	tamBloques = [1, 2, 4, 8, 16]
	i = 0
	contador = 0
	porcentajeDifAcum = 0
	for linea in archivo:
		i+=1
		linea = linea.replace('\n','')
		textoAscii1 = stringToAscii(linea)
		b = random.choice(tamBloques)
		textoCifrado1 = cifradoEnBloque(textoAscii1, keyAscii, b)
		lineaAvalancha = list(linea)
		pos = random.randint(0,len(lineaAvalancha)-1)
		lineaAvalancha = ''.join(lineaAvalancha)
		textoAscii2 = stringToAscii(lineaAvalancha)
		textoAscii2[pos] = random.randint(0,127)
		textoCifrado2 = cifradoEnBloque(textoAscii2, keyAscii, b)
		descifrado = descifradoEnBloque(textoCifrado1, keyAscii, b)
		descifrado2 = descifradoEnBloque(textoCifrado2, keyAscii, b)
		if descifrado == textoAscii1:
			contador+=1
		if descifrado2 == textoAscii2:
			contador+=1
		cont, porcentajeDif = analizarDif(textoCifrado1[:len(textoCifrado1)-1],textoCifrado2[:len(textoCifrado1)-1],3)
		porcentajeDifAcum += porcentajeDif
	averageDif = porcentajeDifAcum/i
	return averageDif, contador
#Funcionamiento: mismo caso que el anterior, pero esta vez se cambia un caracter al azar de la llave, dejando el texto leido en el archivo sin modificar
def averageAvalanchaKey():
	archivo = open("texto.test","r")
	keySize = 64
	contador = 0
	tamBloques = [1, 2, 4, 8, 16]
	key = randomWord(keySize)
	keyAscii = stringToAscii(key)
	keyAvalancha = list(key)
	pos =random.randint(0,len(keyAvalancha)-1)
	
	keyAvalancha = ''.join(keyAvalancha)
	keyAvalanchaAscii = stringToAscii(keyAvalancha)
	keyAvalanchaAscii[pos] = random.randint(0,127)
	i = 0
	porcentajeDifAcum = 0
	for linea in archivo:
		i+=1
		linea = linea.replace('\n','')
		textoAscii1 = stringToAscii(linea)
		b = random.choice(tamBloques)
		textoCifrado1 = cifradoEnBloque(textoAscii1, keyAscii, b)
		textoCifrado2 = cifradoEnBloque(textoAscii1, keyAvalanchaAscii, b)
		descifrado = descifradoEnBloque(textoCifrado1, keyAscii, b)
		descifrado2 = descifradoEnBloque(textoCifrado2, keyAvalanchaAscii, b)
		if descifrado == textoAscii1:
			contador+=1
		if descifrado2 == textoAscii1:
			contador+=1
		cont, porcentajeDif = analizarDif(textoCifrado1,textoCifrado2,3)
		porcentajeDifAcum += porcentajeDif
	averageDif = porcentajeDifAcum/i
	return averageDif, contador
#Funcionamiento: recibe un tamaño de bloques para el algoritmo de descifrado que debe ser ingresado por el usuario
#Salida: tamaño de bloques 
def recibirBloques():
	tamBloques = 0
	while True:
		tamBloques = input("Ingrese el tamaño de bloques con el cual desee codificar (1, 4, 8 o 16): ")
		try:
			tamBloques = int(tamBloques)
		except:
			print("Ingrese solo numeros")
		 
		if tamBloques == 1 or tamBloques == 4 or tamBloques == 8 or tamBloques ==16:
			return tamBloques
#Entradas: dos listas
#Funcionamiento: recorre ambas listas que deben ser de igual tamaño y las suma
#Salida: lista nueva con resultado de la suma
def sumarListas(listaA, listaB):
	suma = []
	if len(listaA) != len(listaB):
		print("Error")
		return 0
	else: 
		for i in range(0, len(listaA)):
			suma.append((int(listaA[i])+int(listaB[i]))%128)
	return suma
#Entrada: dos listas
#Funcionamiento: recorre ambas listas que deben ser de igual tamaño y las resta
#Salida: lista nueva con resultado de resta
def restarListas(listaA, listaB):
	resta = []
	if len(listaA) != len(listaB):
		print("Error")
		return 0
	else: 
		for i in range(0, len(listaA)):
			if listaA[i]-listaB[i]>=0:
				resta.append((listaA[i] - listaB[i])%(128))
			else:
				resta.append((listaA[i] - listaB[i]+128)%128)
	return resta
	
def rotar(lista, x):
  return lista[-x % len(lista):] + lista[:-x % len(lista)]
#Funcion de cifrado principal que se encarga de llamar a las otras dos funciones de cifrado
#Entradas: texto plano, llave y tamaño de bloques
#Funcionamiento: Verifica que el texto plano sea dividible en bloques del tamaño determinado, si no lo es entonces agrega caracteres aleatorios
#Divide el texto plano en bloques y cifra utilizando la funcion cifrado, ademas utiliza modo de operacion CBC, por lo que el resultado de un cifrado se suma el bloque siguiente
#este proceso se repite pero con el texto cifrado parcial invertido
#agrega un numero que indica cuandos digitos se tuvieron que agregar para que el texto fuera divisible
#se cifra para enmascarar el numero agregado
#se retorna texto cifrado final
def cifradoEnBloque(plainText, key, tamBloques):
	alfabeto = []
	newPlainText = plainText[:]
	contador = 0
	textoCifrado = []
	offset = 0
	identificador = 0
	aux = []
	while len(newPlainText)%tamBloques != 0:#se agregan elementos hasta que el texto sea divisible en bloques del tamaño determinado
		newPlainText.append(random.randint(0,127))
		identificador += 1
	iteraciones = int(len(newPlainText)/tamBloques)
	suma = [0]*tamBloques
	while contador < iteraciones:
		
		bloque = newPlainText[contador*tamBloques:(contador+1)*tamBloques]#se obtiene el bloque que sera cifrado en esta iteracion
		bloque = sumarListas(bloque, suma)#se le suma un vector que inicialmente se encuentra lleno de ceros
		suma=cifrado(bloque, key)#se cifra el resultado de la suma
		textoCifrado+=suma#se concatena al texto cifrado parcial
		contador+=1
	contador = 0#se reinician variables
	suma = [0]*tamBloques
	textoCifrado2 = textoCifrado[::-1]#se invierte texto cifrado parcial
	resultado = []
	while contador < iteraciones:#se repite proceso anterior pero con texto cifrado parcial invertido
		bloque = textoCifrado2[contador*tamBloques:(contador+1)*tamBloques]
		bloque = sumarListas(bloque, suma)
		suma=cifrado(bloque, key)
		resultado+=suma
		contador+=1
	resultado.append(identificador)#se agrega identificador de caracteres agregados
	resultado = cifrado(resultado, key)#se cifra una ultima vez
	return resultado
#Funcion principal de descifrado en bloques, llama a decodificar y a descifrar
#Entradas: texto cifrado, llave original y tamaño de bloques
#Funcionamiento: sigue el mismo proceso que cifradoEnBloques pero a la inversa
#Salida: texto descifrado igual al texto plano original
def descifradoEnBloque(cipherText, key, tamBloques):
	contador = 0
	newCipherText = descifrar(cipherText, key)
	suma = [0]*tamBloques
	identificador = newCipherText.pop(-1)
	iteraciones = int(len(newCipherText)/tamBloques)
	descifrado = []
	for contador in range(0, iteraciones):
		bloque = newCipherText[contador*tamBloques:(contador+1)*tamBloques]
		d = descifrar(bloque, key)
		resta = restarListas(d, suma)
		descifrado += resta 
		suma = bloque
	suma = [0]*tamBloques
	descifrado=descifrado[::-1]
	descifrado2= []
	for contador in range(0, iteraciones):
		bloque = descifrado[contador*tamBloques:(contador+1)*tamBloques]
		d = descifrar(bloque, key)
		resta = restarListas(d, suma)
		descifrado2 += resta 
		suma = bloque
	while identificador > 0:
		descifrado2.pop(-1)
		identificador-=1
	return descifrado2

###################INICIO PROGRAMA PRINCIPAL########################
#solo falta mejorar el menu y calcular la ecuacion que sale en el informe, todo lo demas esta listo uwu, casi todo lo que esta de aca hacia abajo hay que borrarlo para la version final y dejar el menu nomas
####################################################################

crearArchivoPrueba()
averageDifWord, cifradosCorrectos = averageAvalancha()	
averageDifKey, cifradosCorrectos2 = averageAvalanchaKey()
print("El porcentaje de diferencia promedio de los textos cifrados (cambiando texto) es de: " + str(averageDifWord) + "%")
print("El porcentaje de diferencia promedio de los textos cifrados (cambiando llave) es de: " + str(averageDifKey) + "%")
print("numero de cifrados correctos cambiando textos es: " +str(cifradosCorrectos))	
print("numero de cifrados correctos cambiando key es: " +str(cifradosCorrectos2))		
menu()
