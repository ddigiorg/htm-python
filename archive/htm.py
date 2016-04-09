
class HTM:
    def __init__(self):
        columnLength = 10
        columnWidth = 10
        columnDepth = 10

        self.cellIndices = []

        for x in range(columnLength):
            for y in range(columnWidth):
                for z in range(columnDepth):
                    self.cellIndices.append([x,y,z])

    def CellIndices(self):
        return self.cellIndices
