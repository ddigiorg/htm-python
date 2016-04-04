import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

import cube as c

SCREEN_SIZE = (800, 600)
CAMERA_SPEED = 1.0
x_move = 0.0
y_move = 0.0
z_move = 0.0
    
def init():
    pygame.init()
    display = SCREEN_SIZE
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -50.0)    

def user_input():
    global x_move, y_move, z_move

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a: x_move =  CAMERA_SPEED
            if event.key == pygame.K_d: x_move = -CAMERA_SPEED
            if event.key == pygame.K_q: y_move =  CAMERA_SPEED
            if event.key == pygame.K_e: y_move = -CAMERA_SPEED
            if event.key == pygame.K_w: z_move =  CAMERA_SPEED
            if event.key == pygame.K_s: z_move = -CAMERA_SPEED
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a: x_move = 0.0
            if event.key == pygame.K_d: x_move = 0.0
            if event.key == pygame.K_q: y_move = 0.0
            if event.key == pygame.K_e: y_move = 0.0                
            if event.key == pygame.K_w: z_move = 0.0
            if event.key == pygame.K_s: z_move = 0.0
                
def draw(cubes):
    glBegin(GL_QUADS)
    for cube in cubes:
        glColor3fv(cube.getColor())
        for surface in cube.getSurfaces():    
            for vertex in surface:
                glVertex3fv(cube.getVertices()[vertex])
    glEnd()
        
##    glBegin(GL_LINES)
##    glColor3fv( (0,0,0) )
##    for edge in self.edges:
##        for vertex in edge:
##            glVertex3fv(self.vertices[vertex])
##    glEnd()

    pygame.display.flip()

def main():
    global x_move, y_move, z_move
    
    init()

    region_length = 20
    region_height = 5
    region_width  = 20
    cell_positions = []

    for l in range(region_length):
        for h in range(region_height):
            for w in range(region_width):
                cell_positions.append( (l*4, h*4, w*4) )
                   
    cubes = [ c.Cube() for i in cell_positions]

    for i in range(len(cell_positions)):
        cubes[i].setPosition(cell_positions[i])


    while True:
        user_input() 

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glTranslatef(x_move, y_move, z_move)
        #glRotatef(0, 0, 0, 0)

        draw(cubes)
       
        pygame.time.wait(10)

main()
