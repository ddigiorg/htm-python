// HTM.hpp

#ifndef HTM_H
#define HTM_H

#include "compute/Constructs.hpp"

namespace htm {
	class HTM {
	private:

		// user set
		int _numInputsX;
		int _numInputsY;
		int _apothemReceptFieldX;
		int _apothemReceptFieldY;
		int _numColumnsX;
		int _numColumnsY;
		int _numCellsPerColumn;
		int _numSegmentsPerCell;
		int _numSynapsesPerSegment;
		int _pSynapseThreshold;
		int _bSynapseThreshold;

		// calculated
		int _numInputs;
		int _numReceptField;
		int _numColumns;
		int _numPSynapsesPerColumn;
		int _numPSynapses;

		int _intSize;

		cl::Kernel _initColReceptFieldKernel;

		cl::Buffer _pSynapseConnections;
		cl::Buffer _pSynapsePermanences;
		cl::Buffer _columnStates;

		cl::NDRange _globalNDRange;

	public:
		HTM();
		void initLayer3b( compute::Constructs &c );
		void initColReceptField( compute::Constructs &c );

	};
}
#endif
