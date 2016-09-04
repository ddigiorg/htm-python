// HTM.hpp

#ifndef HTM_H
#define HTM_H

#include "compute/Constructs.hpp"

namespace htm {
	class HTM {
	private:
		int _numInputsX;
		int _numInputsY;
		int _numReceptFieldX;
		int _numReceptFieldY;
		int _numColumnsX;
		int _numColumnsY;
		int _cellsPerColumn;
		int _segmentsPerCell;
		int _synapsesPerSegment;
		int _pSynapseThreshold;
		int _bSynapseThreshold;

		cl::Kernel _initLayer3bKernel;

		cl::Buffer _pSynapseConnections;
		cl::Buffer _pSynapsePermanences;
		cl::Buffer _columnStates;

	public:
		HTM();
		void initLayer3b( compute::Constructs &c );
		void initReceptiveFields( compute::Constructs &c );

	};
}
#endif
