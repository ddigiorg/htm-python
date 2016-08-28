# g_model.py

class Square( object ):
	def __init__( self, idxX, idxY, startX, startY, size, spacing, data ):
		self.idxX = idxX
		self.idxX = idxY
		self.size = size

		self.mesh = [ 0, size, 0, 0, size, 0, size, size, 0, size, size, 0 ]

		self.position = [ startX + idxX * ( size + spacing ),
                          startY + idxY * ( size + spacing ) ]

		self.color = [ 0.2, 0.2, 0.2 ]

		self.data = data

class Assembly( object ):
	def __init__( self, polygons, dataType ):
		self.polygons = polygons
		self.dataType = dataType
