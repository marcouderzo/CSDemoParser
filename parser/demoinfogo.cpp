//====== Copyright (c) 2012, Valve Corporation, All rights reserved. ========//
//
// Redistribution and use in source and binary forms, with or without 
// modification, are permitted provided that the following conditions are met:
//
// Redistributions of source code must retain the above copyright notice, this
// list of conditions and the following disclaimer.
// Redistributions in binary form must reproduce the above copyright notice, 
// this list of conditions and the following disclaimer in the documentation 
// and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF 
// THE POSSIBILITY OF SUCH DAMAGE.
//===========================================================================//

#include "demofiledump.h"

#include "GlobalPlayerInfo.h"

// these settings cause it to output nothing
bool g_bDumpGameEvents = false;
bool g_bSupressFootstepEvents = true;
bool g_bShowExtraPlayerInfoInGameEvents = false;
bool g_bDumpDeaths = false;
bool g_bSupressWarmupDeaths = true;
bool g_bDumpStringTables = false;
bool g_bDumpDataTables = false;
bool g_bDumpPacketEntities = false;
bool g_bDumpNetMessages = false;

int __cdecl main( int argc, char *argv[] )
{
	CDemoFileDump DemoFileDump;

	std::string s = argv[1];
	targetPlayerSteamID = stoull(s);

	printf("Parsing Player with SteamID: %llu \n", targetPlayerSteamID);

	int nFileArgument = 2;

		g_bDumpGameEvents = true;
		g_bSupressFootstepEvents = true;
		g_bShowExtraPlayerInfoInGameEvents = true;
		g_bDumpDeaths = true;
		g_bSupressWarmupDeaths = true;
		g_bDumpStringTables = true;
		g_bDumpDataTables = false;
		g_bDumpPacketEntities = true;
		g_bDumpNetMessages = true;


	if( DemoFileDump.Open( argv[ nFileArgument ] ) )
	{
		
		std::string file = argv[nFileArgument];

		size_t lastSlash = file.find_last_of('/');
		file.erase(0,lastSlash+1);

		size_t lastDot = file.find_last_of('.');
		file.erase(lastDot, lastDot+3);
		
		file = "logs/" + file + ".txt";
		freopen(file.c_str(), "w", stdout); // redirect all stdout to a file
		DemoFileDump.DoDump();
		fclose(stdout); //keeping this?
	}

	if (entityID == -1 || userID == -1)
	{
		exit(2);
	}

	return 1;
}




