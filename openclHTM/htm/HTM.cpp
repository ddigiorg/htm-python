// HTM.cpp

#include "HTM.hpp"
#include <iostream>

using namespace htm;

HTM::HTM() {
	_numColumnsX = 5;
	_numColumnsY = 5;
	_numReceptFieldX = 2;
	_numReceptFieldY = 2;
}

void HTM::initLayer3b( compute::Constructs &c ) {

	int intSize = sizeof(int);

	int numColumns;
	int numPSynapsesPerColumn;
	int numPSynapses;

	numColumns = _numColumnsX * _numColumnsY;
 	numPSynapsesPerColumn = _numReceptFieldX * _numReceptFieldY;
	numPSynapses = numColumns * numPSynapsesPerColumn;

//	std::cout << "numColumns: " << numColumns << std::endl;
//	std::cout << "numSynapsesPerColumn: " << numPSynapsesPerColumn << std::endl;
//	std::cout << "numPSynapsesColumns: " << numPSynapses << std::endl;

	try {	
		_pSynapseConnections = cl::Buffer( c.getContext(), CL_MEM_READ_WRITE, numPSynapses * intSize );
		_pSynapsePermanences = cl::Buffer( c.getContext(), CL_MEM_READ_WRITE, numPSynapses * intSize );
		_columnStates = cl::Buffer( c.getContext(), CL_MEM_READ_WRITE, numColumns * intSize );

//		c.getQueue().enqueueFillBuffer( pSynapseConnections,  );
	}
	catch( cl::Error error) {
		std::cout << error.what() << " : " << error.err() << std::endl;
	}
}

void HTM::initReceptiveFields( compute::Constructs &c ) {
		_initLayer3bKernel = cl::Kernel( c.getProgram(), "initLayer3b" );

		_initLayer3bKernel.setArg( 0, _numColumnsX );
		_initLayer3bKernel.setArg( 1, _numColumnsY );

		c.getQueue().enqueueTask( _initLayer3bKernel );
		c.getQueue().finish();

}
