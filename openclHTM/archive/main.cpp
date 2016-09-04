// main.cpp

// http://geosoft.no/development/cpppractice.html
// http://geosoft.no/development/cppstyle.html

#define __CL_ENABLE_EXCEPTIONS

#include <fstream>
#include <iostream>
#include <CL/cl.hpp>
#include <CL/opencl.h>

int main() {
	std::vector<cl::Platform> platforms;
	std::vector<cl::Device> devices;
	std::vector<cl::Kernel> kernels;

	try {
		// Create platform
		cl::Platform::get( &platforms );

		// Get device
		platforms[0].getDevices( CL_DEVICE_TYPE_GPU, &devices );

		std::cout << platforms[0].getInfo<CL_PLATFORM_NAME>() << std::endl;
		std::cout << devices[0].getInfo<CL_DEVICE_NAME>() << std::endl;

		// Create context
		cl::Context context( devices[0] );

		// Create command queue
		cl::CommandQueue queue( context, devices[0] );

		// Create program
		std::ifstream sourceFile( "htm.cl" );
		if( !sourceFile.is_open() ) {
			std::cout << "Could not open file: htm.cl" << std::endl;
			exit(1);
		}

		std::string sourceCode(
           std::istreambuf_iterator<char>(sourceFile),
           (std::istreambuf_iterator<char>()) );

		std::cout << sourceCode << std::endl;

		cl::Program::Sources source( 1, std::make_pair( sourceCode.c_str(), sourceCode.length() + 1  ) );

		cl::Program program(context, source);

		// Compile OpenCL source
		program.build( devices );

		// Load named kernel from OpenCL source
		cl::Kernel kernel( program, "poop");



		// Execute kernel
		queue.enqueueTask( kernel );

		// Wait for completion
		queue.finish();
		
	}

	catch(cl::Error error) {
		std::cout << error.what() << " : " << error.err() << "\n";
	}

	return 0;

}
