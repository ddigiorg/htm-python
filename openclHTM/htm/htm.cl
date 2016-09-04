// htm.cl

__kernel void initLayer3b( const int numColumns,
                           const int numColumnsY ) {

	size_t id = get_global_id(0);
	printf( "numColumnsX: %i\n", numColumnsX );
	printf( "numColumnsY: %i\n", numColumnsY );
}
