#http://gamedev.stackexchange.com/questions/9085/opengl-stack-overflow-if-i-do-stack-underflow-if-i-dont
#https://gist.github.com/deepankarsharma/3494203
#http://stackoverflow.com/questions/11125827/how-to-use-glbufferdata-in-pyopengl
#https://www.youtube.com/watch?v=KIeExgOcmv0&ab_channel=thecplusplusguy

import numpy
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo

SCREEN_SIZE = (800, 600)

def main():

##    vbo = glGenBuffers(1)
##    glBindBuffer(GL_ARRAY_BUFFER, vbo)
##    a = [0,2,-4,-2,-2,-4,2,-2,-4]
##    glBufferData(GL_ARRAY_BUFFER, a, GL_STATIC_DRAW)

    my_data = numpy.array( [0,2,-4,-2,-2,-4,2,-2,-4], 'f')
    my_vbo = vbo.VBO( my_data )

    my_vbo.bind()
    glVertexPointer( my_vbo )
    my_vbo.unbind()
    
    pygame.init()
    display = SCREEN_SIZE
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -10.0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #glDrawArrays(GL_TRIANGLES, 0, 3)
        
        pygame.display.flip()
        pygame.time.wait(10)

main()
