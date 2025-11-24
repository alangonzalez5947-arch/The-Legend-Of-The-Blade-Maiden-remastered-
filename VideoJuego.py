import pygame
from Personaje import personaje 
import Constantes #importar las constantes del juego
from Enemigo import enemigo


def iniciar_juego():
 pygame.init()


ventana = pygame.display.set_mode((Constantes.ANCHO_VENTANA, Constantes.ALTO_VENTANA), pygame.FULLSCREEN)


pantalla_ancho = ventana.get_width()
pantalla_alto = ventana.get_height()

fondo = pygame.image.load("Assets//Images//Background//Background_image.png")
fondo = pygame.transform.scale(fondo, (Constantes.ANCHO_VENTANA, Constantes.ALTO_VENTANA))
    

#crear el suelo 
suelo_altura = 126

  #grosor del suelo
suelo_y = pantalla_alto - suelo_altura
suelo = pygame.Rect(0, suelo_y, pantalla_ancho, suelo_altura)


pygame.display.set_caption("Juego Perron")

def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, size = (w*scale, h*scale))
    return nueva_imagen

animaciones_walk = []
for i in range(7):
    img = pygame.image.load(f"Assets//Images//Characters//Player//Walking_{i}.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones_walk.append(img)

animaciones_idle = []
for i in range(4):
    img = pygame.image.load(f"Assets//Images//Characters//Player//Idle//Idle_KG_{i}.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones_idle.append(img)

animaciones_jump = []
for i in range(6):
    img = pygame.image.load(f"Assets//Images//Characters//Player//Jump//Jump_KG_{i}.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones_jump.append(img)

animaciones_crouch = []
for i in range(3):
    img = pygame.image.load(f"Assets//Images//Characters//Player//Crouching//Crouching_KG_{i}.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones_crouch.append(img)

animaciones_attack = []
for i in range(6):
    img = pygame.image.load(f"Assets//Images//Characters//Player//Ataque principal//Attack_KG_{i}.png")
    img = escalar_img(img, Constantes.SCALA_PERSONAJE)
    animaciones_attack.append(img)


jugador = personaje(500, 500, animaciones_idle, animaciones_walk, animaciones_jump, animaciones_crouch, animaciones_attack)
enemigo = enemigo(300, 500, escala=5)





#definir las variables de movimiento del jugador
mover_izquierda = False
mover_derecha = False

#Controla los Frames
reloj = pygame.time.Clock()
run = True


while run == True:
    #Que vaya a 60 FPS
    reloj.tick(Constantes.FPS)

    #calcular dt
    dt = reloj.get_time() / 1000
    
    ventana.blit(fondo, (0,0))

    

    #Calcular movimiento de jugador
    delta_x = 0


    if mover_derecha == True:
        delta_x = Constantes.VELOCIDAD
    if mover_izquierda == True:
        delta_x = -Constantes.VELOCIDAD


    
    keys = pygame.key.get_pressed()
    jugador.agachado = keys[pygame.K_s]


    

      #mover al jugador
    jugador.movimiento(delta_x)

    #va despues del jugador.movimiento
    jugador.update()

    if jugador.hitbox_ataque and enemigo.vivo:
        if jugador.hitbox_ataque.colliderect(enemigo.rect):
            enemigo.recibir_daño(10)
    
    jugador.dibujar(ventana)

    enemigo.update(jugador, dt)



    # Hitbox de ataque del enemigo
    hitbox_enemigo = enemigo.get_hitbox_ataque()

    if hitbox_enemigo and hitbox_enemigo.colliderect(jugador.rect):
        jugador.recibir_daño(10)
      
    enemigo.dibujar(ventana)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
               mover_derecha = True

            if event.key == pygame.K_SPACE:
                jugador.saltar()

            if event.key == pygame.K_j:
                jugador.atacar()
            
            if event.key == pygame.K_ESCAPE:
                run = False

            
        #Para cuando se suelte la tecla 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
               mover_derecha = False
            

    pygame.draw.rect(ventana, (120, 70, 20), suelo)
    pygame.display.update()

pygame.quit()

if __name__ == "__main__":
    iniciar_juego()