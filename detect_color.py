import cv2
import numpy

import sys
sys.path.insert(0, 'C:/Users/titog/Documents/Programas/PythonProjects/Velha/tensorflow-for-poets-2/scripts')
import label_image

photoName = "analizada.jpg"

emJogo = True
camera_port = 1


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

def RetornarTrecho(id, foto):
	#height, width = foto.shape
	dimensions = foto.shape
	height = foto.shape[0]
	width = foto.shape[1]
	channels = foto.shape[2]

	#width, height = cv2.GetSize(foto)

	y , x = Coordenadas(width, height, id)

	return foto[x: int(x+width/3) , y: int(y+height/3)]


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

def CompararTrecho(img):
	output = []
	label_image.analisarIMG(img)


def Analisar():
	image = TakePhoto()
	#cv2.imshow("window", image )
	
	trecho = RetornarTrecho(2, image)

	cv2.imwrite( photoName,trecho)

	cv2.imshow("window", trecho )
	CompararTrecho(photoName)
	


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

	cv2.destroyAllWindows()

	

'''
python scripts/retrain.py --bottleneck_dir=tf_files/bottlenecks --how_many_training_steps=500 --model_dir=tf_files/models --output_graph=tf_files/retrained_graph.pb --output_labels=tf_files/retrained_labels.txx --image_dir=tf_files/Pieces
'''