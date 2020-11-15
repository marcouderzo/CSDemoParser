# CSDemoParser
CS:GO Demo Parser based on the official demoinfogo - Cybersecurity Project @ UniPD

## How To Use

### Building demoinfogo on Windows

In order to build demoinfogo on Windows, follow these steps:

1. Download [protobuf-2.5.0.zip](https://github.com/google/protobuf/releases/download/v2.5.0/protobuf-2.5.0.zip) and extract it into the `demoinfogo` folder. This creates the folder `demoinfogo/protobuf-2.5.0`.
2. Download the Protobuf compiler [protoc-2.5.0.zip](https://github.com/google/protobuf/releases/download/v2.5.0/protoc-2.5.0-win32.zip) and extract it into the `demoinfogo/protoc-2.5.0-win32` folder.
3. Open `demoinfogo/protobuf-2.5.0/vsprojects/protobuf.sln` in Microsoft Visual Studio 2017. Allow Visual Studio to convert the projects.
4. Build the *Release* configuration of `libprotobuf`. Building any other projects is not required.
5. Open `demoinfogo/demoinfogo.vcxproj` in Microsoft Visual Studio 2017. Building the Release configuration creates the binary `demoinfogo/demoinfogo.exe`
