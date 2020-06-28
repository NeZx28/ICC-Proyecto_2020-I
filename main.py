import pygame
import random

# inicializacion y ventana
pygame.init()
Ancho = 840
Alto = 480
screen = pygame.display.set_mode((Ancho, Alto))

# Fondo y musica
fondo = pygame.image.load("3613223.jpg")
pygame.mixer.music.load("Blooming Villain.mp3") # el volumen esta alto
pygame.mixer.music.play(-1)

# Titulo e icono de ventana
pygame.display.set_caption("Título tentativo")  # escriban sus ideas en el chat
icon = pygame.image.load("player.jpg")
pygame.display.set_icon(icon)

# Inicializar jugador
ship1_img = pygame.image.load("millennium-falcon.png")
playerX = Ancho//4
playerY = Alto - 80
cambio_X = 0
def player(x, y):
    screen.blit(ship1_img, (x, y))

# Enemigos
e1_img = []
e1_X = []
e1_Y = []
e1_cambioX = []
e1_cambioY = []
e1_cantidad = 6
aux = random.randint(0, 150)
for x in range(e1_cantidad):
    e1_img.append(pygame.image.load("2.jpg"))
    if x == 0:
        e1_X.append(Ancho//10)
    else:
        e1_X.append(e1_X[0]+70*x)
    e1_Y.append(aux)
    e1_cambioX.append(1)
    e1_cambioY.append(65)
def e1(x, y, i):
    screen.blit(e1_img[i], (x, y))
# falta añadir mas enemigos

# laser 1
laser1_img = pygame.image.load("laser.png")
laser1_X = 0
laser1_Y = 410
laser1_cambioX = 0
laser1_cambioY = 3
laser1_estado = "Listo"
def usar_laser1(x, y):
    global laser1_estado
    laser1_estado = "Disparar"
    screen.blit(laser1_img, (x+16, y+10))
# quizas añadir otro laser, o reducir el intervalo de disparo

# colision
def golpe(enemigoX, enemigoY, proyectilX, proyectilY):  # me parece que es posible mejorar el sistema de impacto
    distancia = (((enemigoX - proyectilX)**2)+((enemigoY - proyectilY)**2))**(1/2)  # diferencia entre
    if distancia < 20:
        return True
    else:
        return False

# puntaje
puntaje = 0
texto = pygame.font.SysFont("comicsans", 30)
texto_X = 20
texto_Y = 20
def mostrar_puntaje(x, y):
    puntos = texto.render("Puntos: " + str(puntaje), True, (255, 210, 20))
    screen.blit(puntos, (x, y))

# vidas
vida = 5
v_texto = pygame.font.SysFont("comicsans", 30)
vidas_X = 40
vidas_Y = 40
def mostrar_vidas(x, y):
    vidas = v_texto.render("Vidas: " + str(vida), True, (255,210, 20))
    screen.blit(vidas, (x, y))
# arreglar las vidas con el game over

# fin de juego
fin = pygame.font.SysFont("comicsans", 50 )
def fin_juego():
    mensaje = fin.render("GAME OVER", True, (255, 255, 255))
    screen.blit(mensaje, (Ancho//2 - 170, Alto//2 - 60))

# game execution
menu = True
titulo = pygame.font.SysFont("comicsans", 50)
while menu:
    screen.blit(fondo, (0, 0))  # fondo de carga
    marca_titulo = titulo.render("Haz clic para empezar...", 1, (255, 255, 255))    # corregir titulo en pantalla de menu
    screen.blit(marca_titulo, (Ancho//2 - (marca_titulo.get_width()//2), 50))
    # menu inicial aparece en negro

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu = False
        if event.type == pygame.MOUSEBUTTONDOWN:    # hacer clic para empezar
            ejecucion = True
            while ejecucion:
                screen.blit(fondo, (0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Exit
                        quit()

                    if event.type == pygame.KEYDOWN:  # Presionar tecla:
                        if event.key == pygame.K_LEFT:  # Mover a la izquierda en el plano
                            cambio_X = -5
                        if event.key == pygame.K_RIGHT:  # Mover a la derecha en el plano
                            cambio_X = 5

                        # verificar si se presiona space y se puede disparar
                        if event.key == pygame.K_SPACE and laser1_estado == "Listo":
                            laser1_X = playerX
                            usar_laser1(laser1_X, laser1_Y)

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:   # detener movimiento
                            cambio_X = 0

                # movimiento en el eje X del jugador
                playerX += cambio_X

                # border limits para el jugador
                if playerX <= 0:
                    playerX = 0
                elif playerX >= 776:
                    playerX = 776

                for i in range(e1_cantidad):
                    # movimiento en el eje X de los enemigos
                    e1_X[i] += e1_cambioX[i]
                    # restringir el movimiento de enemigo 1
                    if e1_X[i] <= 0:
                        e1_cambioX[i] = 1
                        e1_Y[i] += e1_cambioY[i] #
                    elif e1_X[i] >= 776:
                        e1_cambioX[i] = -1
                        e1_Y[i] += e1_cambioY[i]

                    #
                    if e1_Y[i] >= 370 and vida == 0:
                        for j in range(e1_cantidad):
                            e1_Y[j] = 4000
                        fin_juego()
                    elif e1_Y[i] >= 370 and vida > 0:
                        vida -= 1

                    # colision
                    colision = golpe(e1_X[i], e1_Y[i], laser1_X, laser1_Y)
                    if colision:
                        laser1_Y = 410
                        laser1_estado = "Listo"
                        puntaje += 1
                        e1_X[i] = random.randint(0, Ancho - 80)
                        e1_Y[i] = random.randint(0, Ancho // 5)

                    e1(e1_X[i], e1_Y[i], i)  # enemy1 spawn

                # laser 1
                if laser1_Y <= 0:
                    laser1_Y = playerY
                    laser1_estado = "Listo"
                # Disparar laser 1
                if laser1_estado == "Disparar":
                    usar_laser1(laser1_X, laser1_Y)
                    laser1_Y -= laser1_cambioY

                player(playerX, playerY)  # player spawn

                mostrar_puntaje(texto_X, texto_Y)
                mostrar_vidas(vidas_X, vidas_Y)

                pygame.display.update()
