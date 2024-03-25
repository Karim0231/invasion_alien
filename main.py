import pygame
import random
import math
from pygame import mixer

#Inicializar Pygame
pygame.init()

#Crear pantalla
pantalla = pygame.display.set_mode((800,600))

#Titulo e icono
pygame.display.set_caption("Invasión Espacial") #Titulo
icono = pygame.image.load("extra.png") #Icono
pygame.display.set_icon(icono)

#Agregar musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.1)
mixer.music.play(-1)

fondo = pygame.image.load("fondo.jpg")
ancho_fondo = 800
largo_fondo = 600
fondo_redimensional = pygame.transform.scale(fondo,(ancho_fondo,largo_fondo))

#Variables jugador
img_jugador = pygame.image.load("astronave.png")
jugador_x = 355 #(800/2) - ancho del jugador)
jugador_y = 520 #600 - largo del jugador
jugador_x_cambio = 0
ancho = 45
largo = 45
img_redimensional = pygame.transform.scale(img_jugador,(ancho,largo))

#Variables enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8
img_enemigo_principal = pygame.image.load("enemigo.png")
anchoe = 45
largoe = 45
img_eredimensional = pygame.transform.scale(img_enemigo_principal,(anchoe,largoe))

#Variables enemigo
for e in range(cantidad_enemigos):
    img_enemigo.append(img_eredimensional)
    enemigo_x.append(random.randint(0,755))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)

#variables bala
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 520
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False
anchob = 20
largob = 20
img_bredimensional = pygame.transform.scale(img_bala,(anchob,largob))

#Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

#Texto fianl del juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)

def texto_final():
    mi_funte_final = fuente_final.render("GAME OVER",True,(255,255,255))
    pantalla.blit(mi_funte_final, (240, 200))

#Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255,255,255))
    pantalla.blit(texto, (x,y))

#Funcion jugador
def jugador(x,y):
    pantalla.blit(img_redimensional, (x,y))

#Funcion enemigo
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene], (x,y))

#Funcion disparar bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bredimensional,(x + 16, y + 10))

#Funcion detectar colision
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2,2))
    if distancia < 27:
        return True
    else:
        return False

#Loop del juego
se_ejecuta= True
while se_ejecuta:
    #Color del fondo de pantalla
    #pantalla.fill((205,144,228))
    #Fondo de pantalla
    pantalla.blit(fondo_redimensional,(0,0))

    for evento in pygame.event.get():
        #Evento click a cerrar pestaña
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        #Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.3
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.3
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound('disparo.mp3')
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x,bala_y)
        
        #Evento levantar teclas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    #Modificar ubicacion jugador
    jugador_x += jugador_x_cambio

    #Mantener dentro de bordes jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 755:
        jugador_x = 755

    #Modificar ubicacion enemigo
    for e in range(cantidad_enemigos):
        # Fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]

    #Mantener dentro de bordes enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 755:
            enemigo_x_cambio[e] = -0.3
            enemigo_y[e] += enemigo_y_cambio[e]
        #Colision
        colison = hay_colision(enemigo_x[e],enemigo_y[e],bala_x,bala_y)
        if colison:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0,755)
            enemigo_y[e] = random.randint(50,200)

        enemigo(enemigo_x[e],enemigo_y[e], e)

    #Movimiento bala
    if bala_y <= -45:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x,jugador_y)
    mostrar_puntaje(texto_x,texto_y)

    #Actualizar
    pygame.display.update()