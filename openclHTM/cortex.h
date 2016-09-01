// cortex.h

#ifndef CORTEX_H
#define CORTEX_H

#include <stdio.h>

#define MAX_NUM_SYNAPSES 1
#define MAX_NUM_DENDRITES 1
#define MAX_NUM_NEURONS 1
#define MAX_NUM_COLUMNS 1

typedef struct synapse_s {
	int connection;
	int permanence;
} synapse_t;

typedef struct dendrite_s {
	synapse_t synapses[MAX_NUM_SYNAPSES];
} dendrite_t;

typedef struct neuron_s {
	dendrite_t dendrites[MAX_NUM_DENDRITES];
} neuron_t;

typedef struct column_s {
	neuron_t neurons[MAX_NUM_NEURONS];
	dendrite_t dendrite;
} column_t;

typedef struct layer3b_s {
	column_t columns[MAX_NUM_COLUMNS];
} layer3b_t;

void initLayer3b();

#endif
