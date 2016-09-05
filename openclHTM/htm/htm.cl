// htm.cl

__kernel void initColReceptField(
    const int numInputsX,
    const int numInputsY,
    const int apothemReceptFieldX,
    const int apothemReceptFieldY,
    const int numColumnsX,
    const int numColumnsY,
    const int numPSynapsesPerColumn,
    __global __read_write int *pSynapseConnections ) {

	int idxColumn;
	int idxColumnX;
	int idxColumnY;
	int idxPS;
	int startX;
	int startY;
	int endX;
	int endY;

	idxColumn = get_global_id(0);
	idxColumnX = idxColumn % numColumnsX;
	idxColumnY = idxColumn / numColumnsX;

	startX = idxColumnX - (apothemReceptFieldX - 1);
	startY = idxColumnY - (apothemReceptFieldY - 1);

	endX = idxColumnX + (apothemReceptFieldX - 1);
	endY = idxColumnY + (apothemReceptFieldY - 1);

	idxPS = 0;
	for(int y = startY; y <= endY; y++ ) {
		for(int x = startX; x <= endX; x++ ) {
			if( startX < 0 || startY < 0 || endX > numInputsX || endY > numInputsY ) {
				pSynapseConnections[idxPS + numPSynapsesPerColumn * idxColumn] = -1;
			}
			else {
				pSynapseConnections[idxPS + numPSynapsesPerColumn * idxColumn] = x + numInputsX * y;
			}
			idxPS++;
		}	
	}

//	printf( "col: %i endX: %i endY: %i \n", idxColumn, endX, endY );
}
