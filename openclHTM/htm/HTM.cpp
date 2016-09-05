// HTM.cpp

#include "HTM.hpp"
#include <iostream>

using namespace htm;

HTM::HTM() {
	_numInputsX = 5;
	_numInputsY = 5;
	_apothemReceptFieldX = 2;
	_apothemReceptFieldY = 2;
	_numColumnsX = 5;
	_numColumnsY = 5;	

	_numColumns = _numColumnsX * _numColumnsY;
 	_numPSynapsesPerColumn = ( _apothemReceptFieldX + 1 ) * ( _apothemReceptFieldY + 1 );
	_numPSynapses = _numColumns * _numPSynapsesPerColumn;

	_intSize = sizeof(int);

	_globalNDRange = cl::NDRange( _numColumns );
}

void HTM::initLayer3b( compute::Constructs &c ) {
	try {	
		_pSynapseConnections = cl::Buffer( c.getContext(), CL_MEM_READ_WRITE, _numPSynapses * _intSize );
		_pSynapsePermanences = cl::Buffer( c.getContext(), CL_MEM_READ_WRITE, _numPSynapses * _intSize );
		_columnStates = cl::Buffer( c.getContext(), CL_MEM_READ_WRITE, _numColumns * _intSize );
	}

	catch( cl::Error error) {
		std::cout << error.what() << " : " << error.err() << std::endl;
	}
}

void HTM::initColReceptField( compute::Constructs &c ) {

	try {
		_initColReceptFieldKernel = cl::Kernel( c.getProgram(), "initColReceptField" );

		_initColReceptFieldKernel.setArg( 0, _numInputsX );
		_initColReceptFieldKernel.setArg( 1, _numInputsY );
		_initColReceptFieldKernel.setArg( 2, _apothemReceptFieldX );
		_initColReceptFieldKernel.setArg( 3, _apothemReceptFieldY );
		_initColReceptFieldKernel.setArg( 4, _numColumnsX );
		_initColReceptFieldKernel.setArg( 5, _numColumnsY );
		_initColReceptFieldKernel.setArg( 6, _numPSynapsesPerColumn );
		_initColReceptFieldKernel.setArg( 7, _pSynapseConnections );

		int test[225];

		c.getQueue().enqueueNDRangeKernel( _initColReceptFieldKernel, cl::NullRange, _globalNDRange );
	    c.getQueue().enqueueReadBuffer( _pSynapseConnections,CL_TRUE, 0, 225 * _intSize, test );
		c.getQueue().finish();

		for(int i = 0; i < 225; i++) {
			std::cout << test[i] << " ";
		}
		std::cout << std::endl;

	}
	catch( cl::Error error) {
		std::cout << error.what() << " : " << error.err() << std::endl;
	}

}
