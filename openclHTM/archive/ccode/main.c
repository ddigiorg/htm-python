// main.c

//#include <stdio.h>

// Device: GeForce GTX 750 Ti
// Hardware version: OpenCL 1.2 CUDA
// Software version: 367.35n 
// OpenCL C version: OpenCL C 1.2 
// Parallel compute units: 5

// https://www.fixstars.com/en/opencl/book/OpenCLProgrammingBook/basic-program-flow/

#include "cortex.h"

#define NUM_INPUTS_X (5)
#define NUM_INPUTS_Y (5)
#define NUM_INPUTS (NUM_INPUTS_X * NUM_INPUTS_Y)

void printArray(int *array, size_t size) {

	int i;
	for(i = 0; i < size; i++ ){
		printf("%i ", array[i]);
	}
	printf("\n");

}

int main(){

	int inputs[NUM_INPUTS] = {1, 1, 1, 0, 0,
                              0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0};

	printArray( &inputs[0], NUM_INPUTS);//sizeof(inputs) / sizeof(inputs[0]) );

	initLayer3b();

	return 0;
}
