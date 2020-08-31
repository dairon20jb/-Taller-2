from matplotlib import pyplot as plt
from  ImageShape import * # Importando
if __name__ == '__main__':
    print("Digite el ancho de la imagen deseada")
    ancho =int(input())
    print("Digite el alto de la imagen deseada")
    alto=int(input())
    Fig = imageShape(ancho,alto)  # Llamado clase
    Fig.generateShape()# Se genera la figura
    x,y=Fig.getShape() # Retorna la imagen y un string indicando que figura es
    figura = Fig.whatShape(x) # Se identifica por medio de contornos y umbralización que figura se genero previamente
    Fig.showShape() # Muestra la figura durante 5 segundos
    print(figura) # Imprime la figura que reconocio whatshape
    if y == figura: #Se verifica si la figura identifica se es correcta
        print("La clasificación es correcta")
    else:
        print("La clasificación es incorrecta")