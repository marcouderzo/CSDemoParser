#ifndef GLOBALPLAYERINFO_H
#define GLOBALPLAYERINFO_H

// Player Identity Info
extern unsigned long long targetPlayerSteamID;
extern int userID;
extern int entityID;

// Player Entity-Event Info
extern float mouseCoordX;
extern float mouseCoordY;

extern float playerPositionX;
extern float playerPositionY;
extern float playerPositionZ;

extern float playerVelocityX;
extern float playerVelocityY;
extern float playerVelocityZ;

extern bool isPlayerCrouched;


// Tick count
extern int currentTick;

#endif
