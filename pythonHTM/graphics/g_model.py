# g_model.py

class Square( object ):
	def __init__( self, idxX, idxY, startX, startY, spacingX, spacingY, size, data ):
		self.idxX = idxX
		self.idxY = idxY
		self.size = size

		self.mesh = [ 0, size, 0, 0, size, 0, size, size, 0, size, size, 0 ]

		self.position = [ startX + idxX * ( size + spacingX ),
                          startY + idxY * ( size + spacingY ) ]

		self.color = [ 0.2, 0.2, 0.2 ]

		self.data = data

class Assembly( object ):
	def __init__( self, polygons, dataType ):
		self.polygons = polygons
		self.dataType = dataType
