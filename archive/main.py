import array
a = array.array('B', [0]*4)
a[1] = 1

https://pythonprogramming.net/multiple-opengl-cubes/

https://www.youtube.com/watch?v=R4n4NyDG2hI&ab_channel=sentdex

import time
import htm
import plotHTM

region = htm.HTM()
plot = plotHTM.PlotHTM()

cellIndeces = region.CellIndices()
plot.updatePlotIndices(cellIndeces, 'w')
plot.draw()
time.sleep(2)
plot.updatePlotIndices(cellIndeces, 'b')
plot.draw()
