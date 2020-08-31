import math
import numpy as np
import cv2
import random
class imageShape: # Se crea la clase imageShape
    def __init__(self,width,height): #Constructor definición
        self.width = width
        self.height = height
        self.im_generada = 0 #Bandera para indicar cuando se ha generado imagen
        self.num_alea = 4 #Número que indica que figura generar
    def generateShape(self):
        self.shape = np.zeros((self.height, self.width, 3), np.uint8) # Generación de imagen negra de una resolución determinada por el usuario
        self.im_generada = 1 #Bandera en 1 , indicando que ya hay imagen generada
        coordenada_centro = (int(self.width / 2), int(self.height / 2)) # Con el fin de centrar todas las figuras se calcula la coordenada central
        self.num_alea = random.randint(0,3) # Se genera un número entre 0 y 3 con el fin de indicar que figura se generara
        if self.num_alea == 0:  # Si el número es 0 se genera un triangulo
            lado = int(min(self.width, self.height)/2) # Medida de cada lado del Triangulo Equilatero
            m_lado = int(lado/2) #Esto permitira centrar el triangulo
            altura= int(math.sqrt(lado**2-m_lado**2))
            m_altura = int(altura/2) #Se necesita calcular la altura para poder dibujar correcetamente el triangulo
            pt1 = (coordenada_centro[0]-m_lado,coordenada_centro[1]+m_altura )
            pt2 = (coordenada_centro[0]+m_lado,coordenada_centro[1]+m_altura )
            pt3 = (coordenada_centro[0],coordenada_centro[1]-m_altura ) # Se establecen los tres vértices
            triangle_cnt = np.array([pt1, pt2, pt3])  # Se juntan en un arreglo
            cv2.drawContours(self.shape, [triangle_cnt], 0, (255, 255, 0), -1) # Se dibuja el contorno sobre los tres vértices y se rellena de color Cyan
        if self.num_alea == 1: # Si el número es 1 se genera un Cuadrado
            lado = int(min(self.width,self.height)/2) #Medida de cada lado
            m_lado =int(lado/2)
            pt1 = (coordenada_centro[0], coordenada_centro[1] - m_lado)
            pt2 = (coordenada_centro[0]-m_lado, coordenada_centro[1]  )
            pt3 = (coordenada_centro[0]+m_lado, coordenada_centro[1] )
            pt4 = (coordenada_centro[0], coordenada_centro[1] + m_lado) #Ubicación de los 4 vértices
            square_cnt = np.array([pt1, pt2, pt4,pt3])
            cv2.drawContours(self.shape, [square_cnt], 0, (255, 255, 0), -1) # Se dibuja el contorno sobre los cuatro vértices y se rellena de color Cyan
        if self.num_alea == 2: # Si el número es 2 se genera un Rectangulo
            lado_horizontal = int(self.width/2) #Medida de lados horizontales del rectangulo
            lado_vertical   = int(self.height/2) #Medida de lados verticales del rectangulo
            m_lado_horizontal = int(lado_horizontal / 2)
            m_lado_vertical = int(lado_vertical / 2) #m_lado permite ubicar de forma centrada la figura
            pt1 = (coordenada_centro[0]-m_lado_vertical, coordenada_centro[1]-m_lado_horizontal)
            pt2 = (coordenada_centro[0]+m_lado_vertical,coordenada_centro[1]-m_lado_horizontal)
            pt3 = (coordenada_centro[0]-m_lado_vertical, coordenada_centro[1]+m_lado_horizontal)
            pt4 = (coordenada_centro[0]+m_lado_vertical, coordenada_centro[1]+m_lado_horizontal)
            rectangle_cnt = np.array([pt1, pt2, pt4, pt3])
            cv2.drawContours(self.shape, [rectangle_cnt], 0, (255, 255, 0), -1) # Se dibuja el contorno sobre los cuatro vértices y se rellena de color Cyan
        if self.num_alea == 3: # Si el número es 3 se genera un Circulo
            radio = int(min(self.width, self.height)/4)
            cv2.circle(self.shape, coordenada_centro, radio, (255, 255, 0), -1) # Se dibuja el circulo y se rellena con color Cyan
    def showShape(self): # Permite visualizar la imagen durante 5 segundos, si no hay imagen se muestra una totalmente negra durante 5 segundos
        if self.im_generada==1:
            cv2.imshow("Image", self.shape)
            cv2.waitKey(5000)
            self.im_generada == 0
        else:
            self.shape = np.zeros((self.height, self.width, 3), np.uint8)
            cv2.imshow("Image", self.shape)
            cv2.waitKey(5000)
    def getShape(self): # Se obtiene un string, este indica que figura se genero previamente (Triangulo, Cuadrado, Rectangulo o Circulo)
        if self.num_alea == 0:
            string= "La figura es un Triangulo"
        if self.num_alea == 1:
            string= "La figura es un Cuadrado"
        if self.num_alea == 2:
            string= "La figura es un Rectangulo"
        if self.num_alea == 3:
            string= "La figura es un Circulo"
        if self.num_alea >3:
            string = "Figura no definida"
        return self.shape,string
    def whatShape(self,imagen_e): # Permite identificar que figura se genero
        image_gray = cv2.cvtColor(imagen_e, cv2.COLOR_BGR2GRAY) # Se convierte a escala de grises la imagen
        ret, Ibw_shapes = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #Se umbraliza por medio de OTSU
        cnts, hierarchy = cv2.findContours(Ibw_shapes, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE) # Se encuentran todos los contornos
        epsilon = 0.01 * cv2.arcLength(cnts[0], True)
        approx = cv2.approxPolyDP(cnts[0], epsilon, True) # Aproxima el contorno a otro con menos vértices
        x, y, w, h = cv2.boundingRect(approx)  # Permite obtener los puntos de cada vértice, el ancho y alto del contorno
        if len(approx) == 3: # Si los vértices son 3 significara que la figura encontrada es un circulo
            string = "La figura es un Triangulo"
        if len(approx) == 4: # Si los vértices son 4 significara que la figura encontrada es un cuadrado o un rectangulo
            aspect_ratio = float(w) / h # Entonces se saca la relación entre el ancho y alto del contorno, si es diferente de uno sera un rectangulo
            if aspect_ratio == 1:
                string = "La figura es un Cuadrado"
            else:
                string = "La figura es un Rectangulo" #Puede ocurrir que la imagen generada sea cuadrada, para este caso el reconocimiento del rectangulo puede no coincidir
        if len(approx) > 10:
            string = "La figura es un Circulo"
        return string

