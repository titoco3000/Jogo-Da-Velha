import cv2
import time
import numpy

#variaveis não reiniciadas
emJogo = True
camera_port = 0
fotosCount = 0;
img_name = "fotos/image"



'''
aqui estão armazenadas as coordenadas do jogo da velha (visto da posição da garra)
		1 2 3
		4 5 6
		7 8 9
'''
def Coordenadas(width, height, id):
	if id==1:
		return(0,0)
	elif id==2:
		return( int(width/3), 0)
	elif id==3:
		return(int(2*(width/3)), 0)
	elif id==4:
		return(0, int(width/3) )
	elif id==5:
		return(int(width/3), int(width/3))
	elif id==6:
		return(2*int(width/3), int(width/3))
	elif id==7:
		return(0,2*int(width/3))
	elif id==8:
		return(int(width/3), 2*int(width/3) )
	elif id==9:
		return(2*int(width/3), 2*int(width/3))

#valores a serem comparados
class ValoresBase():
	Branco = 868241
	Vermelho = 609398
	Preto = 594508

#retorna a imagem a ser analizada
def TakePhoto():
	camera = cv2.VideoCapture(camera_port)	

	return_value, image = camera.read()

	#se não tem camera
	if not return_value:
		print("no camera here")

		#retorna uma imagem de teste
		return cv2.imread('default_image.png')

	#corta a imagem
	crop_img = image[175:423, 197:446]

	#salva a imagem(opcional)
	#cv2.imwrite( img_name + ".png", crop_img)

	camera.release()

	return crop_img

def Calibrar():
	image = TakePhoto()
	grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	height, width = grayImage.shape

	#vermelho(1)
	y , x = Coordenadas(width, height, 1)

	trecho = grayImage[x: int(x+width/3) , y: int(y+height/3)]


	ValoresBase.Vermelho = trecho.sum().item()

	#branco(2)
	y , x = Coordenadas(width, height, 2)

	trecho = grayImage[x: int(x+width/3) , y: int(y+height/3)]

	ValoresBase.Branco = trecho.sum().item()

	#Preto(3)
	y , x = Coordenadas(width, height, 3)

	trecho = grayImage[x: int(x+width/3) , y: int(y+height/3)]


	ValoresBase.Preto = trecho.sum().item()

	print( "V: " + str(ValoresBase.Vermelho) + " B: " + str(ValoresBase.Branco) + " P: "+str(ValoresBase.Preto))


#retorna o valor do trecho id de img: preto -1, branco 0, vermelho 1
def AnalisarTrecho(id, img):

	trecho = RetornaTrecho(id, img)
	
	#imprime o "quão claro" é o trecho
	clareza = trecho.sum()	
	''' valores base
	branco   - 868241
	vermelho - 609398
	preto    - 594508
	'''
	if clareza < ValoresBase.Vermelho:
		#pode ser preto ou vermelho
		diffPreto = abs(clareza - ValoresBase.Preto)
		diffVermelho = abs(clareza - ValoresBase.Vermelho)
		if diffPreto < diffVermelho:
			#peça é preta
			return -1
		else:
			#peça é vermelha
			return 1
	else:
		#pode ser branco ou vermelho
		diffBranco = abs( clareza - ValoresBase.Branco)
		diffVermelho = abs(clareza - ValoresBase.Vermelho)
		if diffBranco < diffVermelho:
			return 0
		else:
			return 1

def RetornaTrecho(id, img):
	#tamanho da imagem
	height, width, channels = img.shape

	#coordenada do trecho a analisar
	y , x = Coordenadas(width, height, id)

	#separa apenas esse trecho
	return img[x: int(x+width/3) , y: int(y+height/3)]

	#demonstra o trecho (opcional)
	'''
	#upScale
	scale_percent = 220 # percent of original size
	width = int(trecho.shape[1] * scale_percent / 100)
	height = int(trecho.shape[0] * scale_percent / 100)
	dim = (width, height)
	resized = cv2.resize(trecho, dim, interpolation = cv2.INTER_AREA)
	#revela a imagem
	cv2.imshow("window", resized)
	'''

def SalvarTrecho(id):
	global fotosCount
	image = TakePhoto()
	trecho = RetornaTrecho(id, image)
	cv2.imwrite( img_name + str(fotosCount) + ".jpg", trecho)
	fotosCount += 1
	print("imagem salva")

#retorna a lista com analise
def Analisar():
	image = TakePhoto()

	#passa para cinza
	grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#exibe a imagem(opcional)
	cv2.imshow("window", grayImage)

	retorno = []

	#analisa as 9 partes
	for n in range(1,10):
		retorno.append(AnalisarTrecho(n, grayImage))

	print(retorno)
	return retorno
	

#cada partida é um loop aqui
while emJogo:
	cv2.namedWindow("window")
	cv2.moveWindow("window", 0,0)
	
		

	#o loop, para esperar teclas
	while True:
		k= cv2.waitKey(1)

		#sair do programa
		if k%256 == 27:
			emJogo = False
			print("esc")
			break
		elif k%256 == 114:
			print("R")
			break
		#fazer a analise
		elif k%256 == 32:
			print("space")
			Analisar()
		elif k%256 == 99:
			print("c")
			Calibrar()
		elif k%256 == 115:
			print("s")
			SalvarTrecho(1)

	cv2.destroyAllWindows()

	
