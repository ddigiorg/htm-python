import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as plt3d
import matplotlib.animation as animation

class PlotHTM:
    def __init__(self):
        fig = plt.figure()
        self.ax = plt3d.Axes3D(fig)
        #self.ax = fig.add_subplot(111, projection='3d')

        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.set_zlabel('Z Label')

    def updatePlotIndices(self, indices, color):
        x1, y1, z1 = zip(*indices)
        self.ax.scatter(x1, y1, z1, c=color)
   
    def show(self):
        plt = AnimatedScatter()
        plt.show()
