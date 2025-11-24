import pygame
import Constantes
from enemy_ai import EnemyAI

class enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, escala = 2):
        super().__init__()

        # IA 
        self.ai = EnemyAI(speed = 2, detection_range=250, flee_range=0)

        #----Animaciones--------
        self.animaciones = {
            "idle": [],
            "walk": [],
            "attack": [],
            "dead": []
        }

        self.cargar_animaciones(escala)

        self.estado = "idle"
        self.frame = 0
        self.time_acc = 0
        self.frame_rate = 0.15    #Aqui va la velocidad de la animacion

        self.image = self.animaciones["idle"][0]
        self.rect = self.image.get_rect(center=(x, y))


       #Fisicas
        self.vel_y = 0
        self.gravedad = 0.6
        self.en_suelo = False
        
        #Estado
        self.vida = 100
        self.vivo = True
        self.atacando = False

        # Guardar posición del jugador
        self.objetivo_x = x
        self.objetivo_y = y

         # Control de daño
        self.puede_dañar = True   # evita golpear muchas veces por frame
        self.cooldown_golpe = 0.5 # segundos entre golpes
        self.tiempo_ultimo_golpe = 0

    
    
    def cargar_animaciones(self, escala):


        def cargar_lista(ruta, cantidad):
            lista = []
            for i in range(cantidad):
                img = pygame.image.load(ruta.format(i))
                w,h = img.get_width(), img.get_height()
                img = pygame.transform.scale(img, (int(w* escala), int(h * escala)))
                lista.append(img)
            return lista
        
        #Rutas
        self.animaciones["idle"] = cargar_lista("Assets//Images//Characters//Enemies//Idle_enemy//Golem_{}_idle.png", 8)
        self.animaciones["walk"] = cargar_lista("Assets//Images//Characters//Enemies//walk_enemy//Golem_{}_walk.png", 10)
        self.animaciones["attack"] = cargar_lista("Assets//Images//Characters//Enemies//Attack_enemy//Golem_{}_attack.png", 11)
        self.animaciones["dead"] = cargar_lista("Assets//Images//Characters//Enemies//Die_enemy//Golem_{}_die.png", 12)

    def animar(self, dt):
        lista = self.animaciones[self.estado]

        self.time_acc += dt
        if self.time_acc >= self.frame_rate:
            self.time_acc = 0
            self.frame += 1

            if self.frame >= len(lista):
                if self.estado == "dead":
                    self.frame = len(lista) - 1
                else:
                    self.frame = 0

        self.image = pygame.transform.flip(lista[self.frame], self.flip, False)


    def aplicar_gravedad(self):

        if not self.vivo:
            return
        
        #aumentar velocidad vertical
        self.vel_y += self.gravedad

        #limitar velocidad maxima
        if self.vel_y > 12:
            self.vel_y = 12
        
        #mover vertical
        self.rect.y += self.vel_y

        #Colision con suelo
        SUELO_Y = Constantes.ALTO_VENTANA - 75

        if self.rect.bottom > SUELO_Y:
            self.rect.bottom = SUELO_Y
            self.vel_y = 0
            self.en_suelo = True
        else:
            self.en_suelo = False

    def get_hitbox_ataque(self):
        if self.estado != "attack":
            return None
        
        ancho = 90
        alto = 80

        if self.rect.centerx <= self.objetivo_x:  # jugador a la derecha
            return pygame.Rect(self.rect.right, self.rect.centery - 40, ancho, alto)
        else:                                      # jugador a la izquierda
            return pygame.Rect(self.rect.left - ancho, self.rect.centery - 40, ancho, alto)

    def atacar(self):
        self.atacando = True
        self.estado = "attack"
        self.frame = 0
        self.puede_dañar = True



    def recibir_daño(self, cantidad):
        if not self.vivo:
            return
        
        self.vida -= cantidad
        print(f"Enemigo recibió {cantidad} de daño. Vida restante: {self.vida}")

        if self.vida <= 0:
            self.vivo = False
            self.estado = "dead"
            self.frame = 0
            print("Enemigo derrotado.")

    def update(self, jugador, dt):
        
        # guardar posicion real del jugador
        self.objetivo_x = jugador.rect.centerx
        self.objetivo_y = jugador.rect.centery

        if not self.vivo:
            self.estado = "dead"
            self.animar(dt)
            return
        
        # Voltear sprite según posición del jugador
        if self.objetivo_x < self.rect.centerx:
            self.flip = True       # mira a la izquierda
        else:
            self.flip = False 
        
       
        self.aplicar_gravedad()

        #ia movimiento
        self.ai.update(self, (self.objetivo_x, self.objetivo_y))

        # Si está cerca del jugador → atacar automáticamente
        dist = abs(self.rect.centerx - self.objetivo_x)
        if dist < 120 and not self.atacando:
            self.atacar()

        #Estados
        if self.atacando:
            self.estado = "attack"
        elif getattr(self.ai, "dx" , 0) != 0:
            self.estado = "walk"
        else:
            self.estado = "idle"

        self.animar(dt)

        # Sistema de daño al jugador
        if self.estado == "attack":
            hitbox = self.get_hitbox_ataque()

            if hitbox:

                #
                print("Hitbox:", hitbox)
                print("jugador:", jugador.rect)
                # cooldown del enemigo
                tiempo_actual = pygame.time.get_ticks()

                if tiempo_actual - self.tiempo_ultimo_golpe >= self.cooldown_golpe * 1000:
                  self.tiempo_ultimo_golpe = tiempo_actual

                  # si toca al jugador lo daña
                  if jugador.rect.colliderect(hitbox):
                       jugador.recibir_daño(10)  # daño que quieras


    def dibujar(self, ventana):
            ventana.blit(self.image, self.rect)