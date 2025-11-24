import pygame
import Constantes

class personaje():
    def __init__(self, x, y, idle_frames, walk_frames, jump_frames, crouch_frames, attack_frames):
        self.flip = False
        
        #imagen de la animacion que se esta mostrando actualmente
        self.idle_frames = idle_frames 
        self.walk_frames = walk_frames
        self.jump_frames = jump_frames
        self.crouch_frames = crouch_frames
        self.attack_frames = attack_frames
    
        
        
        #Estado incial
        self.state = "idle"

        #Animacion
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        

        #imagen inicial
        self.image = self.idle_frames[0]

        #Hitbox del personaje
        self.rect = self.image.get_rect(center=(x, y))

        #variables fisica
        self.vel_y = 0   #velocidad vertical
        self.gravedad = 0.6   # fuerza de gravedad
        self.fuerza_salto = -15 #impulso de salto
        self.en_suelo = False  #detectr si esta en el suelo
        self.agachado = False

        #Ataque
        self.atacando = False
        self.hitbox_ataque = None # Se creara temporalmente el area de daño
        self.ultimo_ataque = 0
        self.attack_cooldown = 500

        #Vida jugador
        self.vida = 100
        self.invulnerable = False
        self.invul_timer = 0
        self.invul_cooldown = 600

      

        #
        # Sistema de daño del jugador
        #
    def recibir_daño(self, cantidad):
     if not self.invulnerable:
      self.vida -= cantidad
      print(f"jugador recibió {cantidad} de daño. Vida restante: {self.vida}")

                #activar invencibilidad temporal
      self.invulnerable = True
      self.invul_timer = pygame.time.get_ticks()


    def update_invulnerabilidad(self):
        """Controla el tiempo de invencibilidad despues de recibir daño"""
        if self.invulnerable:
            if pygame.time.get_ticks() - self.invul_timer >= self.invul_cooldown:
                self.invulnerable = False




        

        #
        #movimiento
        #

    def movimiento(self, delta_x):

        #no moverse mientras ataca
        if self.atacando:
            delta_x = 0
       
       #flip de la imagen
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        
        #movimeinto
        if not self.agachado:
            self.rect.x += delta_x

        #limites laterales
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Constantes.ANCHO_VENTANA:
            self.rect.right = Constantes.ANCHO_VENTANA

        #Gravedad real
        
        self.vel_y += self.gravedad  # aplicar gravedad cada frame

        #velocidad maxima de caida
        if self.vel_y > 12:
            self.vel_y = 12

        # mover verticalmente con velocidad de gravedad
        self.rect.y += self.vel_y
        
        #colision con suelo
        SUELO_Y = 923

        if self.rect.bottom > SUELO_Y:
           self.rect.bottom = SUELO_Y
           self.vel_y = 0
           self.en_suelo = True
        else:
            self.en_suelo = False

        
        #Cambio estado de animacion
        if not self.atacando:
           if self.agachado and self.en_suelo:
            self.state = "crouch"
           elif not self.en_suelo:
            self.state = "jump"
           else: 
              if delta_x == 0:
                self.state = "idle"
              else:
                self.state = "walk"


        #Salto real

    def saltar(self):
        if self.en_suelo and not self.agachado and not self.atacando:
            self.vel_y = self.fuerza_salto
            self.en_suelo = False
            self.state = "jump"
            self.frame_index = 0    #Reinicia la animacion del salto


        #
        # Ataque
        #
    def atacar(self):
        tiempo_actual = pygame.time.get_ticks()

        if tiempo_actual - self.ultimo_ataque < self.attack_cooldown:
            return
        
        if not self.atacando:     # para que no se repita el bucle
            self.atacando = True
            self.state = "attack"
            self.frame_index = 0
            self.hitbox_ataque = None # Se crea en los frames corrrectos
            self.ultimo_ataque = tiempo_actual

         
        #
        #update
        #

    
    def update(self):
        cooldown_animacion = 80

        #elegir la lista correcta segun el estado
        if self.state == "idle":
            frames = self.idle_frames
        elif self.state == "walk":
            frames = self.walk_frames
        elif self.state == "jump":
            frames = self.jump_frames
        elif self.state == "attack":
             frames = self.attack_frames

                #Crear hitbox de ataque en frames especificos
             if 1 <= int(self.frame_index) <= 3:
                 ancho = 80
                 alto = 60

                 if not self.flip:   #mirando derecha
                     self.hitbox_ataque = pygame.Rect(self.rect.right, self.rect.centery - 30, ancho, alto)
                 else:    #mirando izquierda
                     self.hitbox_ataque = pygame.Rect(self.rect.left - ancho, self.rect.centery - 30, ancho, alto)
             else:
                 self.hitbox_ataque = None

            # Fin del ataque
             if self.frame_index >= len(frames) - 1:
                self.atacando = False
                self.state = "idle"
             
             
        elif self.state == "crouch":    
            #si el jugador acaba de agacharse se reproduce la animacion completa
             if self.frame_index < len(self.crouch_frames) - 1:
                frames = self.crouch_frames

             else:
                self.image = self.crouch_frames[-1]
                return

        # Avance animacion
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index += 0.8
            self.update_time = pygame.time.get_ticks()

        # Reiniciar animacion
        if self.frame_index >= len(frames):
            if self.state == "jump":
                self.frame_index = len(frames) - 1  # En salto quedarse en el ultimo frame
            else:
              self.frame_index = 0

        #poner la imagen correcta
        self.image = frames[int(self.frame_index)]

        #
        #Dibujar
        #


    def dibujar(self, ventana):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        ventana.blit(imagen_flip, self.rect)
        #pygame.draw.rect(ventana, Constantes.COLOR_PERSONAJE, self.forma, width = 1)