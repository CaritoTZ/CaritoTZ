import pygame, sys
from pygame.locals import *
import random
import string
from palabras_final import palabras

imagenes = []
idx_imagen = 0

palabra = ''
texto = ''
vidas = 0
letras_x_adivinar = set() 
abecedario = set() 
letras_adivinadas = set()  

#se inicializa la carga de las imagenes. Devuelve un nuevo rectángulo que cubre toda la superficie. 
# Este rectángulo siempre comenzará en 0, 0 con un ancho. y altura del mismo tamaño que la imagen.
def inicializar_imagenes():
    fondo0 = pygame.image.load("imagenes/ahorcado0.png").convert()
    fondo_rect0 = fondo0.get_rect()
    imagenes.append([fondo0, fondo_rect0])

    fondo1 = pygame.image.load("imagenes/ahorcado1.png").convert()
    fondo_rect1 = fondo1.get_rect()
    imagenes.append([fondo1, fondo_rect1])

    fondo2 = pygame.image.load("imagenes/ahorcado2.png").convert()
    fondo_rect2 = fondo2.get_rect()
    imagenes.append([fondo2, fondo_rect2])

    fondo3 = pygame.image.load("imagenes/ahorcado3.png").convert()
    fondo_rect3 = fondo3.get_rect()
    imagenes.append([fondo3, fondo_rect3])

    fondo4 = pygame.image.load("imagenes/ahorcado4.png").convert()
    fondo_rect4 = fondo4.get_rect()
    imagenes.append([fondo4, fondo_rect4])

    fondo5 = pygame.image.load("imagenes/ahorcado5.png").convert()
    fondo_rect5 = fondo5.get_rect()
    imagenes.append([fondo5, fondo_rect5])

    fondo6 = pygame.image.load("imagenes/ahorcado6.png").convert()
    fondo_rect6 = fondo6.get_rect()
    imagenes.append([fondo6, fondo_rect6])

    #funcion para el aleatorio de las palabras  
def obtener_palabra_valida(palabras):
    global palabra

    palabra = random.choice(palabras)

    # Si la palabra contiene un guión o un espacio,
    # seguira seleccionando una palabra al azar.
    while '_' in palabra or ' ' in palabra:
        palabra = random.choice(palabras)
    return palabra.upper()
    

def actualizar_palabra():
    global texto 
    # Estado actual de la palabra que el jugador debe adivinar (por ejemplo:  H - L A)
    lista_palabra = [letra if letra in letras_adivinadas else '_' for letra in palabra]
    texto = "Palabra:" + ' '.join(lista_palabra) # mostrar las letras separadas por un espacio.

#iniciar juego se ejecuta una vez
def iniciar_juego ():
    global letras_x_adivinar
    global abecedario
    global letras_adivinadas
    global vidas
    global palabra
    global idx_imagen

    idx_imagen = 0

    palabra = obtener_palabra_valida(palabras)
    letras_x_adivinar = set(palabra) #conjunto de letras de la palabra que deben ser adivinadas
    abecedario = set(string.ascii_uppercase) #conjunto de letras en el abecedario
    letras_adivinadas = set() #letras que el usuario ha adivinado durante el juego 
    actualizar_palabra()
    vidas = 6

def ahorcado(letra_usu):
    global vidas

    resultado = False
    #obtener respuesta del usuario mientras existen letras pendientes y al jugador le quedan vidas
    if len(letras_x_adivinar) >0 and vidas >0:
        
        #Si la letra escogida por el usuario está en el abecedario
        # y no está en el conjunto de letras que ya se han ingresado,
        # se añade la letra al conjunto de letras ingresadas.
        if letra_usu in abecedario - letras_adivinadas:
            letras_adivinadas.add(letra_usu)
            actualizar_palabra()
        # Si la letra está en la palabra, quitar la letra 
        # del conjunto de letras pendientes por adivinar.
            if letra_usu in letras_x_adivinar:
                letras_x_adivinar.remove(letra_usu)
                resultado = True
            #si la letra no esta en la palabra quitar una vida
            else:
                vidas = vidas -1
        #si la letra escogida x el usuario ya fue ingresada.
        elif letra_usu in letras_adivinadas:
             resultado = True
    return resultado
#El método isalpha() devuelve True si todos los caracteres 
# son letras del alfabeto
def es_valido (palabra):
    resultado = True
    for letra in palabra:
        if not letra.isalpha():
            resultado = False

    return resultado

pygame.init()

ROJO = (255, 0, 0)
#GRIS = (123, 125, 125 )
BLANCO = (255, 255, 255)
#AZUL = (0, 0, 255)
NEGRO = (0,0,0)
VERDE = (0,255,0)

dimensiones = [710, 500]
PANTALLA = pygame.display.set_mode(dimensiones)
myfont = pygame.font.SysFont('Comic Sans MS', 30)

#icono y titulo
pygame.display.set_caption("Ahorcado")
icono = pygame.image.load("imagenes/ahorc.png")
pygame.display.set_icon(icono)

#myimage = pygame.load.image('my_image.jpg').convert()
inicializar_imagenes()
iniciar_juego()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if vidas >0 and len(letras_x_adivinar) >0:
                letra = pygame.key.name(event.key).upper()
                if es_valido(letra):
                    if not ahorcado(letra):
                        idx_imagen +=1
            else:
                iniciar_juego()
    mensaje = ""
    color_mensaje = NEGRO
    if vidas == 0:
        mensaje = "PERDISTE! La palabra es: " + palabra 
        color_mensaje = ROJO
    if len(letras_x_adivinar) == 0:
        mensaje = "GANASTE!"
        color_mensaje = VERDE
    texto_ahorcado = myfont.render(texto, False, (NEGRO))
    texto_vidas = myfont.render("Cantidad de vidas restantes: " + str(vidas), False, (NEGRO))
    texto_letras_ingresadas = myfont.render("Letras ingresadas:" + ' '.join(letras_adivinadas), False, (NEGRO))
    PANTALLA.fill(BLANCO)
    PANTALLA.blit(imagenes[idx_imagen][0], imagenes[idx_imagen][1])
    PANTALLA.blit(texto_ahorcado,(0,250))
    PANTALLA.blit(texto_vidas,(0,300))
    PANTALLA.blit(texto_letras_ingresadas,(0,350))

    #pygame.display.flip()
    if mensaje != "":
        texto_mensaje = myfont.render(mensaje, False, (color_mensaje))
        PANTALLA.blit(texto_mensaje,(0,400))
        texto_continuar = myfont.render("Presione cualquier tecla para volver a jugar", False, (NEGRO))
        PANTALLA.blit(texto_continuar,(0,450))
    pygame.display.update()



















