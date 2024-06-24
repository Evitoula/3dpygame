
import pygame
import pygame.draw
import random 





from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *



# Initialize Pygame
pygame.init()

# Create a screen 
display_width = 800
display_height = 600
screen = pygame.display.set_mode((display_width,display_height))


# Set the title of the window
pygame.display.set_caption("My 3d Pygame")
clock = pygame.time.Clock()


# Background Image
bg_img = pygame.image.load('3d_game.jpg')
bg_img = pygame.transform.scale(bg_img,(display_width,display_height))

# Colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
purple = (255,0,255)
cyane = (0,255,255)

# Score
def score(count):
    font = pygame.font.SysFont(None, 20)
    text = font.render("Score: "+str(count), True, red)
    screen.blit(text,(0,0))

# High Score
def highscore(score):
    font = pygame.font.SysFont(None, 20)
    text = font.render("High Score: "+str(score), True, red)
    screen.blit(text,(700,0))    




#Run the game until the user closes the window
#running = True
#while running:
#    pygame.time.delay(100)  # Delay for smoother movement
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            running = False
#pygame.quit()##

#START MENU
def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        screen.blit(bg_img, (0, 0))
        font = pygame.font.SysFont ("Verdana", 55)
        text = font.render ("3D BALL GAME", True, cyane)
        text_rect = text.get_rect(center=(display_width/2, display_height/2))
        screen.blit (text, text_rect)

        button("START GAME",100,450,150,50,blue,blue,game_loop)
        button("EXIT",550,450,150,50,red,red,quitgame)

        pygame.display.update()
        clock.tick(15)


# Get High Score
def get_high_score():
    high_score = 0
 
    high_score_file = open("high_score.txt", "r")
    high_score = int(high_score_file.read())
    high_score_file.close()
 
    return high_score  

# Save High Score
def save_high_score(new_high_score):
    high_score_file = open("high_score.txt", "w")
    high_score_file.write(str(new_high_score))
    high_score_file.close()

# Buttons
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    font = pygame.font.SysFont ("Verdana", 20)
    text = font.render (msg, True, black)
    text_rect = text.get_rect(center=(x+(w/2), y+(h/2)))
    screen.blit (text, text_rect)

def quitgame():
    pygame.quit()
    quit()

def game_loop():
    
    # Define my object's position and velocity
    x = 50
    y = 50
    width = 40
    height = 60
    vel = 5

    # Ρυθμίσεις παραθύρου
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)

    

   
    # Ρυθμίσεις προβολής
    gluPerspective(45, (display_width / display_height), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
 
    vertices=((1, -1, -1),(1, 1, -1),(-1, 1, -1),(-1, -1, -1),(1, -1, 1),(1, 1, 1),(-1, -1, 1),(-1, 1, 1))
    edges =((0, 1),(0, 3),(0, 4),(2, 1),(2, 3),(2, 7),(6, 3),(6, 4),(6, 7),(5, 1),(5, 4),(5, 7))

    run = True
    while run:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
           x -= vel

        if keys[pygame.K_RIGHT]:
           x += vel

        if keys[pygame.K_UP]:
           y -= vel

        if keys[pygame.K_DOWN]:
           y += vel

        screen.fill(green)
        pygame.draw.rect(screen, (red), (x, y, width, height))   
        pygame.display.update()  

        # Add a camera to the Pygame window
        #camera = pygame.camera.Camera("/dev/video0", (640, 480))

        # Start the camera
        #camera.start()

        # Get an image from the camera
        #image = camera.get_image()
        #screen.blit(image, (0,0))
        #pygame.display.update()

#def DrawCuboid():
 #   glBegin(GL_LINES)
  #  for edge in cuboidEdges:
   #     for vertex in edge:
    #        glVertex3fv(cuboidVertices[vertex])
    #glEnd()

def draw_cube():
  glBegin(GL_LINES)
  for edge in edges:
    for vertex in edge:
            glVertex3fv(vertices[vertex])
  glEnd()


game_intro()
game_loop()
pygame.quit()
quit()








