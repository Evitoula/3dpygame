import sys
import math
import random
import time

from OpenGL.GL  import *
from OpenGL.GLU import *

import pygame
from pygame.locals import *

# Colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


# Sound #Χατχηπαναγιωτιδου
pygame.mixer.init()

crash_sound = pygame.mixer.Sound("crash_sound.wav")

pygame.mixer.music.load('bg_music.wav')
pygame.mixer.music.play(-1)

# Font
pygame.font.init()


class Light(object):
    enabled = False
    colors = [(0.5, 0.5, 0.5), (1.,0.5,0.5,1.),
            (0.5,1.,0.5,1.), (0.5,0.5,1.,.1,)]

    def __init__(self, light_id, position):
        self.light_id = light_id
        self.position = position
        self.current_color = 0 #current color index from the array

    def render(self):
        light_id = self.light_id
        color = Light.colors[self.current_color]
        glLightfv(light_id, GL_POSITION, self.position)
        glLightfv(light_id, GL_DIFFUSE, color)
        glLightfv(light_id, GL_CONSTANT_ATTENUATION, 0.1)
        glLightfv(light_id, GL_LINEAR_ATTENUATION, 0.05)

    def switch_color(self):
        self.current_color += 1  #next color
        self.current_color %= len(Light.colors) # wrap-arround

    def enable(self):
        if not Light.enabled:
            glEnable(GL_LIGHTING)
            Light.enabled = True
        glEnable(self.light_id)

class Cube(object):
    sides = ((0,1,2,3), (3,2,7,6), (6,7,5,4),
             (4,5,1,0), (1,5,7,2), (4,0,3,6))

    edges = (
            (0,1),
            (0,3),
            (0,4),
            (2,1),
            (2,3),
            (2,7),
            (6,3),
            (6,4),
            (6,7),
            (5,1),
            (5,4),
            (5,7),
    )
    
    #save position/color/vertex coortinates
    def __init__(self, position, size, color):
        self.position = position
        self.color = color
        x,y,z = map(lambda i: i/2, size)

        self.vertices = (
            (x,-y,-z), (x,y,-z),
            (-x,y,-z), (-x, -y, -z),
            (x,-y,z), (x,y,z),
            (-x,-y, z), (-x, y,z)
        )

        
    #we add a render function for this object
    def render(self):
        glPushMatrix()
        glTranslatef(*self.position)

        glBegin(GL_QUADS) 
        for side in Cube.sides:            
            for v in side:
                glVertex3fv(self.vertices[v])
        glEnd()
        glPopMatrix()


class Sphere(object):
        slices=40
        stacks=40

        def __init__(self,radius,position,color):
            self.radius= radius
            self.position=position
            self.color = color
            #We have to create a quadratic object first
            #This is used to create basic 3D shapes.
            #This pointer is used to set various properties like orientation, position, size
            self.quadratic = gluNewQuadric()
        
        def render(self):
            glPushMatrix()
            glTranslatef(*self.position)
            glMaterialfv(GL_FRONT, GL_DIFFUSE, self.color)
            gluSphere(self.quadratic, self.radius, Sphere.slices, Sphere. stacks)
            glPopMatrix()


        
#we add the Block class which inherits from the Cube
class Block(Cube):
    color = (1, 0, 0)
    speed = 0.01

    def __init__(self, position, size):
        #cube: position, size, color
        super().__init__(position, (size, 1, 1), Block.color)
        self.size=size

    #the update simply movs the block towards the player by updating its z coordinate
    def update(self,dt):
        x,y,z = self.position
        z += Block.speed * dt
        self.position = x, y, z

#Χλιαρα
class Game_Over:
    def __init__(self, width = 800, height = 600):
        self.width= width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Game Over")
        self.background = (10,10,50)
        
    def run(self):
        running= True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False

    
            self.screen.fill(self.background)
            self.display()
            pygame.display.flip()


class App(object):
    def __init__(self, width=800, height=600):
        self.title= '3d Ball Game' 
        self.fps=60
        self.width= width
        self.height=height
        self.angle=0
        self.distance=20
        self.game_over = False
        self.random_dt = 0
        self.blocks = []
        self.light = Light(GL_LIGHT0, (0,15,-25,1))
        self.player= Sphere(1, position=(0,0,0), color= red)
        self.ground = Cube(position=(0,-1,-20), size=(16,1,60), color=(1,1,1,1))
        
        #Show Timer and Image on Game Over Screen  #Χλιαρα
        self.start_time = 0
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        self.screen = pygame.display.set_mode((width, height))
        self.image = pygame.image.load("_game_over_.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.font = pygame.font.SysFont("Verdana", 35)
        self.text = self.font.render(f"Τime: {self.elapsed_time:.2f} seconds", True, (255,255,255))
        self.screen.blit(self.text, (100, 0))
       

    def start(self):
        pygame.init()
        pygame.display.set_mode((self.width, self.height), OPENGL | DOUBLEBUF)
        pygame.display.set_caption(self.title)
        #enable GL capabilities
        #=>depth comparions and update depth buffer
        glEnable(GL_DEPTH_TEST)
        #=>enables lighting
        glEnable(GL_LIGHTING)
        #=>enables light constant 0 (up to 8 can be used)
        glEnable(GL_LIGHT0)

        glEnable(GL_DEPTH_TEST)
        self.light.enable()
        glClearColor(.1,.1,.1,.1) 
        glMatrixMode(GL_PROJECTION)
        aspect = self.width / self.height
        gluPerspective(40.,aspect, 1., 40.)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_CULL_FACE)
               
        clock=pygame.time.Clock()
        while True:
            dt= clock.tick(self.fps)
            self.process_input(dt)
            #changing the name to main_loop
            self.main_loop()

    #create the main loop 
    def main_loop(self):

        # BackGround Music
        pygame.mixer.music.load('bg_music.wav')
        pygame.mixer.music.play(-1)
        # Timer
        start_time = time.time()
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.game_over:
                    self.display()
                    dt = clock.tick(self.fps)
                    
                    for block in self.blocks:
                        block.update(dt)
                    self.clear_past_blocks()
                    self.add_random_block(dt)
                    self.check_collisions()
                    self.process_input(dt)

    
    #compare the boundaries of the closed blocks with the extremes of the sphere.
    #the sphere is mall so if one the extremes is between right/left boundaries is a collision
    def check_collisions(self):
        #return to the blocks only these whose z position is between 0 and 1
        start_time = 0
        blocks = filter(lambda x: 0<x.position[2]<1, self.blocks)
        x=self.player.position[0]
        r=self.player.radius
        for block in blocks:
            x1= block.position[0]
            s=block.size / 2
            if x1-s < x-r < x1+s or x1-s < x +r < x1+s:
                self.game_over = True
                pygame.mixer.Sound.play(crash_sound)
                pygame.mixer.music.stop()
                end_time = time.time()
                elapsed_time = end_time - start_time
                print("Game Over!")
                Game_Over()
                self.screen.blit(self.image, self.image.get_rect())
                self.screen.blit(self.text, (100, 0))
                pygame.display.flip()
                

    def add_random_block(self, dt):
        self.random_dt +=dt
        if self.random_dt >= 800:
            r=random.random()
            if r < 0.1:
                self.random_dt=0
                self.generate_block(r)

   
    def generate_block(self, r):
        size= 7 if r < 0.03 else 5
        offset = random.choice([-4,0,4])
        position=(offset, 0, -40)
        mynewblock=Block( position, size)
        self.blocks.append(mynewblock)

    
    def clear_past_blocks(self):
        #extract the blocks with the given condition
        blocks = filter(lambda x: x.position[2] > 5, self.blocks)
        for block in blocks:
            self.blocks.remove(block)
            del block

    def process_input(self, dt):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
                if event.key == K_F1:
                    self.light.switch_color()

        pressed = pygame.key.get_pressed()
        #Session05:
        x, y, z = self.player.position
        
        if pressed[K_LEFT]:
            x -= 0.01 * dt

        if pressed[K_RIGHT]:
            x += 0.01 * dt

        #the player cannot move outside of the line
        x = max(min(x, 7), -7)
        self.player.position=(x,y,z)


    def display(self):
      
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(  0, 10, 10,
                    0, 0, -5,
                    0, 1, 0)
        self.light.render()
        for block in self.blocks:
            block.render()
        self.player.render()
        self.ground.render()
        pygame.display.flip()


    def quit(self):
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    app = App()
    app.start()
    g_o = Game_Over(400,300)
    g_o.run()
