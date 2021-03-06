//====== Copyright (c) 2014, Valve Corporation, All rights reserved. ========//
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
#include "demofilepropdecode.h"

#include "google/protobuf/descriptor.h"
#include "google/protobuf/reflection_ops.h"
#include "google/protobuf/descriptor.pb.h"

#include "generated_proto/cstrike15_usermessages_public.pb.h"
#include "generated_proto/netmessages_public.pb.h"

#include "GlobalPlayerInfo.h"




// in demofiledump.cpp
extern const CSVCMsg_SendTable::sendprop_t *GetSendPropByIndex( uint32 uClass, uint32 uIndex );


int Int_Decode( CBitRead &entityBitBuffer, const CSVCMsg_SendTable::sendprop_t *pSendProp )
{
	int flags = pSendProp->flags();

	if ( flags & SPROP_VARINT )
	{
		if ( flags & SPROP_UNSIGNED )
		{
			return (int)entityBitBuffer.ReadVarInt32();
		}
		else
		{
			return entityBitBuffer.ReadSignedVarInt32();
		}
	}
	else
	{
		if ( flags & SPROP_UNSIGNED )
		{
			return entityBitBuffer.ReadUBitLong( pSendProp->num_bits() );
		}
		else
		{
			return entityBitBuffer.ReadSBitLong( pSendProp->num_bits() );
		}
	}
}

// Look for special flags like SPROP_COORD, SPROP_NOSCALE, and SPROP_NORMAL and
// decode if they're there. Fills in fVal and returns true if it decodes anything.
static inline bool DecodeSpecialFloat( CBitRead &entityBitBuffer, const CSVCMsg_SendTable::sendprop_t *pSendProp, float &fVal )
{
	int flags = pSendProp->flags();

	if ( flags & SPROP_COORD )
	{
		fVal = entityBitBuffer.ReadBitCoord();
		return true;
	}
	else if ( flags & SPROP_COORD_MP )
	{
		fVal = entityBitBuffer.ReadBitCoordMP( kCW_None );
		return true;
	}
	else if ( flags & SPROP_COORD_MP_LOWPRECISION )
	{
		fVal = entityBitBuffer.ReadBitCoordMP( kCW_LowPrecision );
		return true;
	}
	else if ( flags & SPROP_COORD_MP_INTEGRAL )
	{
		fVal = entityBitBuffer.ReadBitCoordMP( kCW_Integral );
		return true;
	}
	else if ( flags & SPROP_NOSCALE )
	{
		fVal = entityBitBuffer.ReadBitFloat();
		return true;
	}
	else if ( flags & SPROP_NORMAL )
	{
		fVal = entityBitBuffer.ReadBitNormal();
		return true;
	}
	else if ( flags & SPROP_CELL_COORD )
	{
		fVal = entityBitBuffer.ReadBitCellCoord( pSendProp->num_bits(), kCW_None );
		return true;
	}
	else if ( flags & SPROP_CELL_COORD_LOWPRECISION )
	{
		fVal = entityBitBuffer.ReadBitCellCoord( pSendProp->num_bits(), kCW_LowPrecision );
		return true;
	}
	else if ( flags & SPROP_CELL_COORD_INTEGRAL )
	{
		fVal = entityBitBuffer.ReadBitCellCoord( pSendProp->num_bits(), kCW_Integral );
		return true;
	}

	return false;
}

float Float_Decode( CBitRead &entityBitBuffer, const CSVCMsg_SendTable::sendprop_t *pSendProp )
{
	float fVal = 0.0f;
	unsigned long dwInterp;

	// Check for special flags..
	if( DecodeSpecialFloat( entityBitBuffer, pSendProp, fVal ) )
	{
		return fVal;
	}

	dwInterp = entityBitBuffer.ReadUBitLong( pSendProp->num_bits() );
	fVal = ( float )dwInterp / ( ( 1 << pSendProp->num_bits() ) - 1 );
	fVal = pSendProp->low_value() + (pSendProp->high_value() - pSendProp->low_value()) * fVal;
	return fVal;
}

void Vector_Decode( CBitRead &entityBitBuffer, const CSVCMsg_SendTable::sendprop_t *pSendProp, Vector &v )
{
	v.x = Float_Decode( entityBitBuffer, pSendProp );
	v.y = Float_Decode( entityBitBuffer, pSendProp );

	// Don't read in the third component for normals
	if ( ( pSendProp->flags() & SPROP_NORMAL ) == 0 )
	{
		v.z = Float_Decode( entityBitBuffer, pSendProp );
	}
	else
	{
		int signbit = entityBitBuffer.ReadOneBit();

		float v0v0v1v1 = v.x * v.x + v.y * v.y;
		if (v0v0v1v1 < 1.0f)
		{
			v.z = sqrtf( 1.0f - v0v0v1v1 );
		}
		else
		{
			v.z = 0.0f;
		}

		if (signbit)
		{
			v.z *= -1.0f;
		}
	}
}

void VectorXY_Decode( CBitRead &entityBitBuffer, const CSVCMsg_SendTable::sendprop_t *pSendProp, Vector &v )
{
	v.x = Float_Decode( entityBitBuffer, pSendProp );
	v.y = Float_Decode( entityBitBuffer, pSendProp );
}

const char *String_Decode( CBitRead &entityBitBuffer, const CSVCMsg_SendTable::sendprop_t *pSendProp )
{
	// Read it in.
	int len = entityBitBuffer.ReadUBitLong( DT_MAX_STRING_BITS );

	char *tempStr = new char[ len + 1 ];

	if ( len >= DT_MAX_STRING_BUFFERSIZE )
	{
		//printf( "String_Decode( %s ) invalid length (%d)\n", pSendProp->var_name().c_str(), len );
		len = DT_MAX_STRING_BUFFERSIZE - 1;
	}

	entityBitBuffer.ReadBits( tempStr, len*8 );
	tempStr[len] = 0;

	return tempStr;
}

int64 Int64_Decode( CBitRead &entityBitBuffer, const CSVCMsg_SendTable::sendprop_t *pSendProp )
{
	if ( pSendProp->flags() & SPROP_VARINT )
	{
		if ( pSendProp->flags() & SPROP_UNSIGNED )
		{
			return (int64)entityBitBuffer.ReadVarInt64();
		}
		else
		{
			return entityBitBuffer.ReadSignedVarInt64();
		}
	}
	else
	{
		uint32 highInt = 0;
		uint32 lowInt = 0;
		bool bNeg = false;
		if( !(pSendProp->flags() & SPROP_UNSIGNED) )
		{
			bNeg = entityBitBuffer.ReadOneBit() != 0;
			lowInt = entityBitBuffer.ReadUBitLong( 32 );
			highInt = entityBitBuffer.ReadUBitLong( pSendProp->num_bits() - 32 - 1 );
		}
		else
		{
			lowInt = entityBitBuffer.ReadUBitLong( 32 );
			highInt = entityBitBuffer.ReadUBitLong( pSendProp->num_bits() - 32 );
		}

		int64 temp;

		uint32 *pInt = (uint32*)&temp;
		*pInt++ = lowInt;
		*pInt = highInt;

		if ( bNeg )
		{
			temp = -temp;
		}

		return temp;
	}
}

Prop_t *Array_Decode( CBitRead &entityBitBuffer, FlattenedPropEntry *pFlattenedProp, int nNumElements, uint32 uClass, int nFieldIndex, bool bQuiet )
{
	int maxElements = nNumElements;
	int numBits = 1;
	while ( (maxElements >>= 1) != 0 )
	{
		numBits++;
	}

	int nElements = entityBitBuffer.ReadUBitLong( numBits );

	Prop_t *pResult = NULL;
	pResult = new Prop_t[ nElements ];

	if ( !bQuiet )
	{
		//printf( "array with %d elements of %d max\n", nElements, nNumElements );
	}

	for ( int i = 0; i < nElements; i++ )
	{
		FlattenedPropEntry temp( pFlattenedProp->m_arrayElementProp, NULL );
		Prop_t *pElementResult = DecodeProp( entityBitBuffer, &temp, uClass, nFieldIndex, bQuiet );
		pResult[ i ] = *pElementResult;
		delete pElementResult;
		pResult[ i ].m_nNumElements = nElements - i;
	}

	return pResult;
}

Prop_t *DecodeProp( CBitRead &entityBitBuffer, FlattenedPropEntry *pFlattenedProp, uint32 uClass, int nFieldIndex, bool bQuiet )
{
		const CSVCMsg_SendTable::sendprop_t *pSendProp = pFlattenedProp->m_prop;

		Prop_t *pResult = NULL;
		if (pSendProp->type() != DPT_Array && pSendProp->type() != DPT_DataTable)
		{
			pResult = new Prop_t((SendPropType_t)(pSendProp->type()));
		}

		if (!bQuiet)
		{
			//printf("Field: %d, %s = ", nFieldIndex, pSendProp->var_name().c_str());
		}
		switch (pSendProp->type())
		{
		case DPT_Int:
			pResult->m_value.m_int = Int_Decode(entityBitBuffer, pSendProp);
			break;
		case DPT_Float:
			pResult->m_value.m_float = Float_Decode(entityBitBuffer, pSendProp);
			break;
		case DPT_Vector:
			Vector_Decode(entityBitBuffer, pSendProp, pResult->m_value.m_vector);
			break;
		case DPT_VectorXY:
			VectorXY_Decode(entityBitBuffer, pSendProp, pResult->m_value.m_vector);
			break;
		case DPT_String:
			pResult->m_value.m_pString = String_Decode(entityBitBuffer, pSendProp);
			break;
		case DPT_Array:
			pResult = Array_Decode(entityBitBuffer, pFlattenedProp, pSendProp->num_elements(), uClass, nFieldIndex, bQuiet);
			break;
		case DPT_DataTable:
			break;
		case DPT_Int64:
			pResult->m_value.m_int64 = Int64_Decode(entityBitBuffer, pSendProp);
			break;
		}
		if (!bQuiet)
		{
			//pResult->Print();
		}
	return pResult;
}

Prop_t *DecodePropWithEntity(CBitRead &entityBitBuffer, FlattenedPropEntry *pFlattenedProp, uint32 uClass, int nFieldIndex, bool bQuiet, void *pEntity)
{
	EntityEntry* Entity = static_cast<EntityEntry*>(pEntity);
	const CSVCMsg_SendTable::sendprop_t *pSendProp = pFlattenedProp->m_prop;

	bool hasToUpdate = false;

	Prop_t *pResult = NULL;

	if (pSendProp->type() != DPT_Array && pSendProp->type() != DPT_DataTable)
	{
		pResult = new Prop_t((SendPropType_t)(pSendProp->type()));
	}



	if ((pSendProp->var_name() == "m_vecVelocity[0]" ||
		pSendProp->var_name() == "m_vecVelocity[1]" ||
		pSendProp->var_name() == "m_vecVelocity[2]" ||
		pSendProp->var_name() == "m_vecOrigin" ||
		pSendProp->var_name() == "m_vecOrigin[2]" ||
		pSendProp->var_name() == "m_angEyeAngles[0]" ||
		pSendProp->var_name() == "m_angEyeAngles[1]" ||
		pSendProp->var_name() == "m_vecViewOffset[2]") && Entity->m_nEntity==entityID)
	{
		if (nFieldIndex != 16)
		{
			//printf("Field: %d, %s = ", nFieldIndex, pSendProp->var_name().c_str());
			hasToUpdate = true;
		}
	}
	switch (pSendProp->type())
	{
	case DPT_Int:
		pResult->m_value.m_int = Int_Decode(entityBitBuffer, pSendProp);
		//printf("[Type is DPT_Int, ");
		break;
	case DPT_Float:
		pResult->m_value.m_float = Float_Decode(entityBitBuffer, pSendProp);
		//printf("[Type is DPT_Float, value is %f", pResult->m_value.m_float);
		break;
	case DPT_Vector:
		Vector_Decode(entityBitBuffer, pSendProp, pResult->m_value.m_vector);
		//printf("[Type is DPT_Vector, ");
		break;
	case DPT_VectorXY:
		VectorXY_Decode(entityBitBuffer, pSendProp, pResult->m_value.m_vector);
		//printf("[Type is DPT_VectorXY, ");
		break;
	case DPT_String:
		pResult->m_value.m_pString = String_Decode(entityBitBuffer, pSendProp);
		//printf("[Type is DPT_String, ");
		break;
	case DPT_Array:
		pResult = Array_Decode(entityBitBuffer, pFlattenedProp, pSendProp->num_elements(), uClass, nFieldIndex, bQuiet);
		//printf("[Type is DPT_Array, ");
		break;
	case DPT_DataTable:
		break;
	case DPT_Int64:
		pResult->m_value.m_int64 = Int64_Decode(entityBitBuffer, pSendProp);
		//printf("[Type is DPT_Int64, ");
		break;
	}
	if (!bQuiet)
	{
		//pResult->Print();
	}





	/*
	// ------DEPRECATED------ m_vecViewOffset[2] is now part of Entity


	// GIVEN:
	//		FULL_STANDING: 64.062561f
	//		FULL_CROUCHED: 46.044968f

	// SOLUTION 1:

	if (isCrouchEvent)
	{
		if (pResult->m_value.m_float != 0.000000f) // if the value has already been initialized
		{
			if (pResult->m_value.m_float < 64.062561f && !isPlayerCrouched) 
			{ 
				isPlayerCrouched = true; 
				printf("Action %d player_crouch %f %f %f \n", currentTick, playerPositionX, playerPositionY, playerPositionZ);
			}
			else if (pResult->m_value.m_float == 64.062561f && isPlayerCrouched)
			{
				isPlayerCrouched = false;
			}

	
	// SOLUTION 2:
			
			/*  //correct but the output from the parser is uncertain.

					// OK: Action 128976 player_crouch_init 294.492950 653.842590 20.064556 63.311829
					// OK: Action 129000 player_crouch_full 294.492950 653.842590 20.064556 46.044968
					// NOPE: Action 129260 player_crouch_init 295.996918 654.045227 33.935287 46.044968        <------------------


			if (pResult->m_value.m_float == 64.062561f) {  //if back in standing state, the player is no longer crouched.
				isPlayerCrouched = false; //set crouched to false
				printf("PlayerStanding, setCrouchToFalse\n");
			}

			if (pResult->m_value.m_float < 64.062561f && !isPlayerCrouched) //if he is descending for the first time
			{
				printf("Action %d player_crouch_init %f %f %f %f\n", currentTick, playerPositionX, playerPositionY, playerPositionZ, pResult->m_value.m_float); // I print player_crouch_init
				isPlayerCrouched = true; // I state that the crouch event has started
			}
			else if (pResult->m_value.m_float == 46.044968f) // if reached full crouch state and the init was also called before, but not in the same function call (or else it wrongly will print both)
			{
				printf("Action %d player_crouch_full %f %f %f %f\n", currentTick, playerPositionX, playerPositionY, playerPositionZ, pResult->m_value.m_float); // I print player_crouch_full
				isPlayerCrouched = true;
			}
		}
	}
	*/

	
	if (hasToUpdate)
	{
		if (pSendProp->var_name() == "m_vecVelocity[0]")
		{
			//printf("X Velocity before assigning: %f \n", playerVelocityX);
			playerVelocityX = pResult->m_value.m_float;
			//printf("X Velocity after assigning: %f \n", playerVelocityX);
			//printf("X Velocity in pResult: %f \n", pResult->m_value.m_float);
			//printf("Used m_float 1 ] \n");
		}
		
		if (pSendProp->var_name() == "m_vecVelocity[1]")
		{
			//printf("Z Velocity in pResult: %f \n", pResult->m_value.m_float);
			//printf("Z Velocity before assigning: %f \n", playerVelocityZ);
			playerVelocityZ = pResult->m_value.m_float;
			//printf("Z Velocity after assigning: %f \n", playerVelocityZ);
			//printf("m_float: %f \n", pResult->m_value.m_float);

			//printf("Used m_float 2] \n");
		}

		if (pSendProp->var_name() == "m_vecVelocity[2]")
		{
			playerVelocityY = pResult->m_value.m_float;
			
			//printf("Used m_float 3] \n");
		}

		if (pSendProp->var_name() == "m_vecOrigin")
		{
			playerPositionX = pResult->m_value.m_vector.x;
			playerPositionY = pResult->m_value.m_vector.y;
			//printf("Used vector.x & vector.y ] \n");
		}
		if (pSendProp->var_name() == "m_vecOrigin[2]")
		{
			playerPositionZ = pResult->m_value.m_float;
			//printf("m_vector.z: %f \n", pResult->m_value.m_vector.z);
			//printf("m_value.m_vector %f \n", pResult->m_value.m_vector);
			//printf("m_float: %f \n", pResult->m_value.m_float);
			//printf("Set m_vecorigin2 ] \n");
		}
		if (pSendProp->var_name() == "m_angEyeAngles[0]")
		{
			mouseCoordY = pResult->m_value.m_float;
			//printf("Used m_float 4 ] \n");
		}
		if (pSendProp->var_name() == "m_angEyeAngles[1]")
		{
			mouseCoordX = pResult->m_value.m_float;
			//printf("Used m_float 5] \n");
		}

		if (pSendProp->var_name() == "m_angEyeAngles[1]")
		{
			mouseCoordX = pResult->m_value.m_float;
			//printf("Used m_float 5] \n");
		}

		if (pSendProp->var_name() == "m_vecViewOffset[2]") // crouching yOffset is dumped in Entity.
		{
			crouchStateYOffset = pResult->m_value.m_float;
		}
		

	}

	return pResult;
}