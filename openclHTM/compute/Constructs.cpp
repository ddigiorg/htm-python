// Constructs.cpp

#include "Constructs.hpp"

#include <fstream>
#include <iostream>

using namespace compute;

bool Constructs::init( DeviceType type, const std::string &sourceName ) {

	try {
		// Get platforms and retrieve first occourance
		std::vector<cl::Platform> platforms;
		cl::Platform::get( &platforms );
		_platform = platforms[0];

		// Get devices and store first occourance
		std::vector<cl::Device> devices;
		switch( type ) {
		case _cpu:
			_platform.getDevices( CL_DEVICE_TYPE_CPU, &devices );
			break;
		case _gpu:
			_platform.getDevices( CL_DEVICE_TYPE_GPU, &devices );
			break;
		case _all:
			_platform.getDevices( CL_DEVICE_TYPE_ALL, &devices );
			break;
		}

		_device = devices[0];

		// Create context.   Using default properties so possibly wont work on Apple or Windows?
		_context = cl::Context( _device );

		// Create comamnd queue
		_queue = cl::CommandQueue( _context, _device );

		// Create program from source in the file
		std::ifstream sourceFile( sourceName.c_str() );
		std::string sourceCode( std::istreambuf_iterator<char>(sourceFile),
                                (std::istreambuf_iterator<char>()) );
		cl::Program::Sources source( 1, std::make_pair( sourceCode.c_str(), sourceCode.length() + 1 ) );
		_program = cl::Program( _context, source );
		sourceFile.close();

		// Compile source
		_program.build( devices );

		return true;
	}

	catch( cl::Error error ) {
		std::cout << error.what() << " : " << error.err() << std::endl;
		return false;
	}
}

void Constructs::displayInfo() {
	std::cout << "Platform: " << _platform.getInfo<CL_PLATFORM_NAME>() << std::endl;
	std::cout << "Device Name: " << _device.getInfo<CL_DEVICE_NAME>() << std::endl;
	std::cout << "Device Global Memory Size: " << _device.getInfo<CL_DEVICE_GLOBAL_MEM_SIZE>() << " Bytes" << std::endl;
}
