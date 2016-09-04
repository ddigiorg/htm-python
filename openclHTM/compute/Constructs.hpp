// Constructs.hpp

#ifndef CONSTRUCTS_H
#define CONSTRUCTS_H

#define __CL_ENABLE_EXCEPTIONS

#include <CL/cl.hpp>

namespace compute {
	class Constructs {
	private:
		cl::Platform _platform;
		cl::Device _device;
		cl::Context _context;
		cl::CommandQueue _queue;
		cl::Program _program;

	public:
		enum DeviceType { _cpu, _gpu, _all };
		bool init( DeviceType type, const std::string &sourceName );
		void displayInfo();

		cl::Platform& getPlatform() { return _platform;	}
		cl::Device& getDevice() { return _device; }
		cl::Context& getContext() { return _context; }
		cl::CommandQueue& getQueue() { return _queue; }
		cl::Program& getProgram() { return _program; }
	};
}
#endif
