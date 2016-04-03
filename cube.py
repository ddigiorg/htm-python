from OpenGL.GL import *
from OpenGL.GLU import *

color_dict = {
    'r': (1,0,0),
    'g': (0,1,0),
    'b': (0,0,1),
    'w': (1,1,1)
    }

class Cube:
    def __init__(self):    
        self.position = (0,0,0)
        
        self.color = color_dict['w']
        
        self.vertices = (
            ( 1, -1, -1),
            ( 1,  1, -1),
            (-1,  1, -1),
            (-1, -1, -1),
            ( 1, -1,  1),
            ( 1,  1,  1),
            (-1, -1,  1),
            (-1,  1,  1)
            )

        self.edges = (
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
            (5,7)    
                )

        self.surfaces = (
            (0,1,2,3),
            (3,2,7,6),
            (6,7,5,4),
            (4,5,1,0),
            (1,5,7,2),
            (4,0,3,6)
            )

    def setPosition(self, position):
        self.position = position
        new_vertices = []
        for vertex in self.vertices:
            new_vertices.append( (
                vertex[0] + position[0],
                vertex[1] + position[1],
                vertex[2] + position[2]
                ) )

        self.vertices = new_vertices

    def setColor(self, color):
        self.color = color_dict[color]

    def getPosition(self):
        return self.position

    def getColor(self):
        return self.color

    def getVertices(self):
        return self.vertices

    def getSurfaces(self):
        return self.surfaces


