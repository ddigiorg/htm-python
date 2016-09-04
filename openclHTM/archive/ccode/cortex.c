// cortex.c

#include "cortex.h"

void initLayer3b() {
	layer3b_t layer3b;

	int c;
	for(c = 0; c < MAX_NUM_COLUMNS; c++){
		layer3b.columns[c].pDendrite.synapses[0].connection = 1;
	}

	int test;
	test = layer3b.columns[0].pDendrite.synapses[0].connection;
	printf("%d\n", test);

	int n;
	n = sizeof(layer3b);
	printf("%d\n", n);
}

//void initReceptiveFields(){
//	
//}
