"""
Stuff I learned:

After reading NuPIC's Connections.py, I agree with the principles of their approach
to structuring data.

The special attribute __slots__ allows you to explicitly state in your code which 
instance attributes you expect your object instances to have, with the expected results:
    + faster attribute access.
    + potential space savings in memory.
http://stackoverflow.com/questions/472000/usage-of-slots


"""


class Synapse(object):
	
	__slots__ = 

	def __init__(self):

		
