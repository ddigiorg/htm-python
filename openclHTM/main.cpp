// main.cpp

#include "compute/Constructs.hpp"

#include "htm/HTM.hpp"

int main() {

	compute::Constructs c;

	c.init( compute::Constructs::_gpu, "htm/htm.cl" );
//	c.displayInfo();

	htm::HTM h;

	h.initLayer3b( c );

	return 0;
}
