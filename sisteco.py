import numpy as np
from numpy import sin, linspace, pi
import random

archivos = []
#ord(char) = ascii value
#unichar(ascii value) = char
alfabeto = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","ñ","o","p","q","r","s","t","u","v","w","x","y","z"]

def menu():
    #Muestra el menu principal y usando input se pide al usuario que ingrese la opcion que desea ejecutar
    option = 0
    while option == 0:
        print('Menu Principal')
        print('Opciones:')
        print('1) Ingresar nombre de archivo de texto plano')
        print('2) Salir')
        user_input = input('Ingrese el numero de la opcion que desea ejecutar: ')
        if user_input=="2":
            #se retorna y finaliza el programa
            return 0
        elif user_input=="1":
            #se pide ingresar un nombre de archivo
            error = 1
            while error == 1:
                input_nombre = input('Ingrese nombre del archivo de texto plano: ')
                #la apertura se realiza inicialmente en un try-except, para evitar que el programa se caiga
                #en caso de que el archivo no pueda ser abierto
                try:
                    open(input_nombre, 'rb')
                    error = 0
                except FileNotFoundError:
                    error = 1       
                    print('nombre de archivo no existente o fuera de directorio')
            #llamado a funcion que abre un archivo verificado y retorna datos de este
            textoPlano = open(input_nombre, 'r')
            archivos.append(textoPlano)
            option = second_menu(archivos)
            
        else:
            print('Ingrese una opcion correcta')
            
    return
 
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
		textoCifrado +=cifrado(stringToAscii(texto[0]), llave, alfabeto)
		print("archivo completo cifrado: ")
		print(asciiToString(textoCifrado))
		textoDescifrado +=descifrar(textoCifrado, llave, alfabeto)
		print("archivo completo descifrado")
		print(asciiToString(textoDescifrado))
		
	
	
def cifrado(plainText, key, alfabeto):
	#print("CIFRADO:...")
	contador = 0
	offset = 0
	codificado = []
	keys = []
	iteraciones = 0
	arreglo = []
	plainText2 = plainText[:]
	#print("largo texto plano: ")
	print(len(plainText2))
	if len(plainText2)%2 != 0:
		plainText2.append(ord(random.choice(alfabeto)))
		paridad = 0
	else:
		paridad = 1
		#print("DENTRO CIFRADO")
	iteraciones = len(plainText2)/2
	codificado = codificar(plainText2, key, 0, alfabeto)
	contador = contador + 1
	while contador < iteraciones:
		#print("WHILE CIFRADO OWO")
		newKey = codificado[offset:contador*2]
		#print("NUEVA LLAVE :")
		#print(newKey)
		codificado = codificar(codificado, newKey, 0, alfabeto)
		keys = keys + newKey
		offset+=2
		contador+=1
		
	#codificado = codificar(plainText, key, 0, alfabeto)
	#if len(key)< len(plainText):
	#	newKey = codificado[len(codificado)-len(key):]
	#else: 
#		newKey = key[:]
#	print("TEXTO CODIFICADO ITERACION 1: ")
#	print(asciiToString(codificado))
#	print("LLAVE NUEVA: ")
#	print(newKey)
#	print(len(newKey))
#	print("#######")
#	codificado2 = codificar(codificado, newKey, 0, alfabeto)
#	print("TEXTO CODIFICADO ITERACION 2: ")
#	print(asciiToString(codificado2+newKey))
#	print(codificado+newKey)
#	print("//////////////")
	arreglo.append(iteraciones)
	arreglo.append(paridad)
	codificado = codificar(codificado+keys+arreglo,key,0,alfabeto)

	#print(codificado)
	#print(asciiToString(codificado))
	#print("UNION CODIFICADO + KEYS")
	#print(asciiToString(codificado+keys))
	#print(codificado+keys+arreglo)
	return codificado
	
def codificar(plainText, key, offset, alfabeto):
	#print("CODIFICANDO: ")
	codificado = plainText[:]
	newKey = []
	for cont in range(0, len(key)):
		#plainText[cont+offset*len(key)] = (plainText[cont+offset*len(key)] + key[cont])%(128) #cambiar para codificar cualquier ascii 128
		print(codificado)
		if cont+offset*len(key)>=len(codificado):
			#print("retornando...")
			#print(codificado)
			return codificado
		#print("PAR DE LETRAS: " + alfabeto[plainText[cont+offset*len(key)]]+ " - " + alfabeto[key[cont]]+ " a reemplazar: " +alfabeto[(plainText[cont+offset*len(key)] + key[cont])%(26)])
		if codificado[cont+offset*len(key)]+key[cont]>=127:
			#print("PAR DE NUMEROS: " + str(codificado[cont+offset*len(key)]+1) + " - "+ str(key[cont]+1)+ " a reemplazar: " + str((codificado[cont+offset*len(key)] + key[cont])%(26)+1))
			codificado[cont+offset*len(key)] = (codificado[cont+offset*len(key)] + key[cont])%(127)
			newKey.append(codificado[cont+offset*len(key)])
		else:
			#print("PAR DE NUMEROS: " + str(codificado[cont+offset*len(key)]+1) + " - "+ str(key[cont]+1)+ " a reemplazar: " + str((codificado[cont+offset*len(key)]+1 + key[cont]+1)))
			codificado[cont+offset*len(key)] = (codificado[cont+offset*len(key)] + key[cont])+1
			newKey.append((codificado[cont+offset*len(key)]))
	#print(codificado)
	#print(asciiToString(codificado))
	#print("############")
	#print("NUEVA LLAVE: ")
	#print(newKey)
	#print("#############")
	return codificar(codificado, newKey[::-1], offset+1, alfabeto)

def descifrar(cipherText, key, alfabeto):
	#print("DESCIFRADO:...")
	cipherText = decodificar(cipherText,key,0,alfabeto)
	if cipherText[-1] == 0:
		paridad = 0
	else:
		paridad = 1
	cipherText.pop(-1)
	offset = 0
	iteraciones = cipherText[-1]
	contador = 1
	offset = 0
	decodificado = []
	keys = []
	arreglo = []
	print(iteraciones)
	decodificado = cipherText[offset:len(cipherText)-int(iteraciones)*2+1]
	keys = cipherText[len(cipherText)-int(iteraciones)*2+1:len(cipherText)-1]
	offset = len(keys)
	if len(decodificado)%2 == 0:
		print("TEXTO CIFRADO A DESCIFRAR: ")
		print(decodificado)
		print("777777777777777777777777777777777")
		print("LLAVES: ")
		print(keys)
		print("$$$$$$$$$$$$$$$$$$$")
		while contador < int(iteraciones):
			newKey = keys[offset-2:offset]
			offset -= 2
			contador += 1
			#print("WHILE DECODIFICAR: ")
			#print("LLAVE A APLICAR: ")
			#print(newKey)
			#print("###############")
			decodificado = decodificar(decodificado, newKey, 0, alfabeto)
		#print("DECODIFICACION CASI FINAL: ")
		#print(decodificado)
		#print(asciiToString(decodificado))
		#print("UWU")
		decodificado = decodificar(decodificado, key, 0, alfabeto)
		
	#newKey = cipherText[len(cipherText)-len(key):]
	#print("NUEVA LLAVE: ")
	#print(newKey)
	#print(asciiToString(newKey))
	#print("&&&&&&&&&&&&&&")
	#decodificado = decodificar(cipherText[0:len(cipherText)-len(key)], newKey, 0, alfabeto)
	#print("TEXTO DECODIFICADO ITERACION 1: ")
	#print(asciiToString(decodificado))
	#print("LLAVE NUEVA: ")
	#print(newKey)
	#print(len(newKey))
	#print("#######")
	#decodificado2 = decodificar(decodificado, key, 0, alfabeto)
	#print("TEXTO CODIFICADO ITERACION 2: ")
	#print(asciiToString(decodificado2))
	#print("//////////////")
	#return decodificado2

	if paridad == 0:
		decodificado.pop(-1)
		print("DECODIFICACION FINAL: ")
	print(decodificado)
	print(asciiToString(decodificado))
	return decodificado
	

def decodificar(cipherText, key, offset, alfabeto):
	#print("DECODIFICANDO: ")
	decodificado = cipherText[:]
	newKey = []
	for cont in range(0, len(key)):
		#plainText[cont+offset*len(key)] = (plainText[cont+offset*len(key)] + key[cont])%(128) #cambiar para codificar cualquier ascii 128
		if cont+offset*len(key)>=len(decodificado):
			return decodificado
		#print("PAR DE LETRAS: " + alfabeto[plainText[cont+offset*len(key)]]+ " - " + alfabeto[key[cont]]+ " a reemplazar: " +alfabeto[(plainText[cont+offset*len(key)] + key[cont])%(26)])
		if decodificado[cont+offset*len(key)]-key[cont]>=0:
			#print("MAYOR QUE 0, PAR DE NUMEROS: " + str(decodificado[cont+offset*len(key)]+1) + " - "+ str(key[cont]+1)+ " a reemplazar: " + str((decodificado[cont+offset*len(key)] - key[cont])%(26)-1))
			newKey.append(decodificado[cont+offset*len(key)])
			decodificado[cont+offset*len(key)] = (decodificado[cont+offset*len(key)] - key[cont]-1)%(128)
		else:
			#print("MENOR QUE 0, PAR DE NUMEROS: " + str(decodificado[cont+offset*len(key)]+1) + " - "+ str(key[cont]+1)+ " a reemplazar: " + str((decodificado[cont+offset*len(key)]+1 - key[cont]+27-1)))
			newKey.append(decodificado[cont+offset*len(key)])
			decodificado[cont+offset*len(key)] = (decodificado[cont+offset*len(key)] - key[cont]+128-1)%128
	#print(asciiToString(decodificado))
	#print("######")
	#print("nueva llave: ")
	#print(newKey)
	return decodificar(decodificado, newKey[::-1], offset+1, alfabeto)
	

def stringToNumber(string, alfabeto):
	asciiArray = []
	for char in string:
		asciiArray.append(alfabeto.index(char))
	#print("Llave en ascii: ")
	#print(asciiArray)
	return asciiArray
def numberToString(numberArray, alfabeto):
	string = ''.join(alfabeto[element] for element in numberArray)
	return string

def stringToAscii(string):
	asciiArray = []
	for char in string:
		asciiArray.append(ord(char))
	#print("Llave en ascii: ")
	#print(asciiArray)
	return asciiArray

def asciiToString(asciiArray):
	string = ''
	string = ''.join(chr(int(element)) for element in asciiArray)
	#print("ascii array como string: ")
	#print(string)
	return string
	
	
def getKey():
	largo = 0
	while largo == 0 or largo > 256:
		key = input("Ingrese key que desee usar (cualquier cadena de caracteres ascii entre 1 a 256 de longitud): ")
		largo = len(key)
	print(key)
	return key, largo
	

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
		print("Llave 2 se diferencia de Llave 1 en un " +str(pDiferencia)+ "% y "+ str(contador) +" caracteres")
		return contador
	elif tipo == 1:
		print("Texto 2 se diferencia de Texto 1 en un " +str(pDiferencia)+ "% y "+ str(contador) +" caracteres")
		return contador
	else:
		print("Texto Cifrado 2 se diferencia de Texto Cifrado 1 en un " +str(pDiferencia)+ "% y "+ str(contador) +" caracteres")
		return contador, pDiferencia

def avalancha(plainText1, plainText2, key1, key2, cifrado1, cifrado2):
	contador = 0
	if plainText1 == plainText2 and (key1 == key2):
		print("Textos planos y llaves son iguales")
		return
	elif plainText1 == plainText2 and key1 != key2:
		print("Textos planos iguales, llaves son distintas")
		diferenciaKeys = analizarDif(key1, key2, 2)
		diferenciaCifrado, pCifrado = analizarDif(cifrado1, cifrado2, 3)
		if pCifrado >= 50.0:
			print("Se cumple avalancha")
		else: 
			print("No se cumple avalancha")
	elif plainText1 != plainText2 and key1 == key2:
		print("Textos planos distintos, llaves iguales")
		diferenciaTextos = analizarDif(plainText1, plainText2, 1)
		diferenciaCifrado, pCifrado = analizarDif(cifrado1, cifrado2, 3)
		if pCifrado >= 50.0:
			print("Se cumple avalancha")
		else: 
			print("No se cumple avalancha")
	else:
		print("Llave y textos son distintos")
		diferenciaTextos = analizarDif(plainText1, plainText2, 1)
		diferenciaKeys = analizarDif(key1, key2, 2)
		diferenciaCifrado, pCifrado = analizarDif(cifrado1, cifrado2, 3)
		if pCifrado >= 50.0:
			print("Se cumple avalancha")
		else: 
			print("No se cumple avalancha")
	return 0;

def randomWord(size):
	line = ''
	for c in range(size):
		line += random.choice(alfabeto)
	return line

def crearArchivoPrueba():
	print("Creando archivo de prueba...")
	archivoPrueba = open('texto.test','w')
	for i in range(1000):
		lineSize = random.randint(5,25)*2
		line = randomWord(lineSize)
		if i < 999:
			line += '\n'
		archivoPrueba.write(line)

	
	

def averageAvalancha():
	archivo = open("texto.test","r")
	keySize = 16
	key = randomWord(keySize)
	keyAscii = stringToAscii(key)
	i = 0
	porcentajeDifAcum = 0
	for linea in archivo:
		i+=1
		linea = linea.replace('\n','')
		textoAscii1 = stringToAscii(linea)
		textoCifrado1 = cifrado(textoAscii1,keyAscii,alfabeto)
		lineaAvalancha = list(linea)
		lineaAvalancha[0] = random.choice(alfabeto)
		lineaAvalancha = ''.join(lineaAvalancha)
		print("Texto a comparar: " + linea +" "+ lineaAvalancha)
		textoAscii2 = stringToAscii(lineaAvalancha)
		textoCifrado2 = cifrado(textoAscii2,keyAscii,alfabeto)
		print("Textos cifrados: "+ str(textoCifrado1) + " " + str(textoCifrado2))
		cont, porcentajeDif = analizarDif(textoCifrado1,textoCifrado2,3)
		porcentajeDifAcum += porcentajeDif
	print("i:" + str(i))
	averageDif = porcentajeDifAcum/i
	return averageDif

def averageAvalanchaKey():
	archivo = open("texto.test","r")
	keySize = 16
	key = randomWord(keySize)
	keyAscii = stringToAscii(key)
	keyAvalancha = list(key)
	keyAvalancha[-1] = random.choice(alfabeto)
	keyAvalancha = ''.join(keyAvalancha)
	keyAvalanchaAscii = stringToAscii(keyAvalancha)

	i = 0
	porcentajeDifAcum = 0
	for linea in archivo:
		i+=1
		linea = linea.replace('\n','')
		textoAscii1 = stringToAscii(linea)
		textoCifrado1 = cifrado(textoAscii1,keyAscii,alfabeto)
		
		textoCifrado2 = cifrado(textoAscii1,keyAvalanchaAscii,alfabeto)
		print("Textos cifrados: "+ str(textoCifrado1) + " " + str(textoCifrado2))
		cont, porcentajeDif = analizarDif(textoCifrado1,textoCifrado2,3)
		porcentajeDifAcum += porcentajeDif
	print("i:" + str(i))
	averageDif = porcentajeDifAcum/i
	print("keys: "+ key +" "+keyAvalancha)
	return averageDif



#crearArchivoPrueba()
#averageDifWord = averageAvalancha()	
#averageDifKey = averageAvalanchaKey()

#print("El porcentaje de diferencia promedio de los textos cifrados (cambiando texto) es de: " + str(averageDifWord) + "%")
#print("El porcentaje de diferencia promedio de los textos cifrados (cambiando llave) es de: " + str(averageDifKey) + "%")

		
llave, largo = getKey()
llave2, largo2 = getKey()
llaveAscii = stringToAscii(llave)
llaveAscii2 = stringToAscii(llave2)
#stringKey = asciiToString(llaveAscii)
plainText = input("Ingrese texto a codificar: ")
plainText22 = input("ingrese texto 2 a codificar: ")
textoAscii = stringToAscii(plainText)
print("----------------------")
print("Texto plano en ascii")
print(textoAscii)
print("Texto plano original transformado desde ascii")
print(asciiToString(textoAscii))
print("----------------------------------")
textoAscii2 = stringToAscii(plainText22)
plainText2 = stringToNumber(plainText, alfabeto)
llave2number = stringToNumber(llave2, alfabeto)
plainText222 = stringToNumber(plainText22, alfabeto)
numberArray = stringToNumber(llave, alfabeto)
textoCifrado = codificar(textoAscii, llaveAscii, 0, alfabeto)
textoCifrado2 = codificar(textoAscii2, llaveAscii2, 0, alfabeto)
print("texto cifrado 1: ")
print(asciiToString(textoCifrado))
print("////////////////////////")
print("texto cifrado 2: ")
print(asciiToString(textoCifrado2))
print("/////////////////////////") 
number_string = numberToString(numberArray, alfabeto)
print(asciiToString(textoCifrado))
textoDecodificado = decodificar(textoCifrado, llaveAscii, 0, alfabeto)
textoDecodificado2 = decodificar(textoCifrado2, llaveAscii2, 0, alfabeto)
print("texto descifrado 1: ")
print(asciiToString(textoDecodificado))
print("//////////")
print("texto descifrado 2: ")
print(asciiToString(textoDecodificado2))
print("////////")
avalancha(plainText2, plainText222, numberArray, llave2number, textoCifrado, textoCifrado2)
cifrado_texto1 = cifrado(textoAscii, llaveAscii, alfabeto)
cifrado_texto2 = cifrado(textoAscii2, llaveAscii2, alfabeto)
avalancha(plainText2, plainText222, numberArray, llave2number, cifrado_texto1, cifrado_texto2)
descifrado_texto1 = descifrar(cifrado_texto1, llaveAscii, alfabeto)
descifrado_texto2 = descifrar(cifrado_texto2, llaveAscii2, alfabeto)
if descifrado_texto1 == textoAscii and descifrado_texto2 == textoAscii2:
	print("$$$$$$$$$$$$$$$$$$$$$")
	print("CIFRADO-DESCIFRADO CORRECTO")
	print
	print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
else:
	print("CIFRADO INCORRECTO")
menu()
