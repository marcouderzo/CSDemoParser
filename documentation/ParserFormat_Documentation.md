# Parser Output Documentation

## Entites

The player entity is represented as follows:

*Entity currentTick mouseCoordX mouseCoordY playerPositionX playerPositionY playerPositionZ playerVelocityX playerVelocityY playerVelocityZ crouchStateYOffset*

**Output Example**

```
Entity 250280 345.097046 358.725586 200.976746 706.085266 80.031250 180.222641 0.000000 -17.836735 64.062561
```


## Events

Game events related to the player are much less straight-forward to understand, as they have a common part and a final one that is dependent on the particular event itself.

A Game Event, or *Action* is defined as it follows:

*Action Tick Type playerPositionX playerPositionY playerPositionZ*

This part of the output is common to all events. Then, for some events, the output continues. Here they are.

Note that the events not listed below follow the standard output definition.

### weapon_fire

*Action Tick Type playerPositionX playerPositionY playerPositionZ weapon*

**Output Example**

```
Action 250360 weapon_fire 867.432922 2405.222412 144.230499 weapon_hegrenade
```

### player_crouch -> Custom Event

*Action currentTick, player_crouch playerPositionX, playerPositionY, playerPositionZ)*

**Output Example**

```
Action 176724 player_crouch -1274.234619 -987.730347 -125.380936
```


### player_death

We differenciated the player_death event in three "sub-events".
- *player_death_k*
- *player_death_a*
- *player_death_d*

All of those three have at least both the victim's position and the attacker's position, as follows:

*Action Tick Type VictimPositionX VictimPositionY VictimPositionZ AttackerPositionX AttackerPositionY AttackerPositionZ*

If an assister was also involved in the kill, you will find their position to the end.

*Action Tick Type VictimPositionX VictimPositionY VictimPositionZ AttackerPositionX AttackerPositionY AttackerPositionZ AssisterPositionX AssisterPositionY AssisterPositionZ*

When looking at the output, you will need to be careful in picking the right set of coordinates.

- *player_death_k* : The target player killed someone. *AttackerPositionX AttackerPositionY AttackerPositionZ* are the coordinates of our target player.
- *player_death_a* : The target player assisted a kill. *AssisterPositionX AssisterPositionY AssisterPositionZ* are the coordinates of our target player
- *player_death_d* : The target player died. *VictimPositionX VictimPositionY VictimPositionZ* are the coordinates of our target player.

**Output Examples**

Our Target Player *kills* someone. 
```
Action 293485 player_death_k 19.783495 1378.299927 100.990913 581.881653 2115.028076 135.162598 
```

Our target player *kills* someone and is *assisted*.
```
Action 373847 player_death_k 512.931580 2595.294678 160.031250 656.311829 2641.969971 148.708939 656.311829 2641.969971 148.708939 
```

Our target player *is killed* by someone.
```
Action 387770 player_death_d 741.657166 2752.417480 129.301987 431.821808 2507.880127 160.031250 
```

Our target player *is killed* by someone, and someone else *assisted* the kill.
```
Action 409267 player_death_d 1499.356689 -61.885181 130.031250 2226.073730 200.545563 133.284622 2226.073730 200.545563 133.284622 
```

Our target player *assisted* a kill.
```
Action 147596 player_death_a 2150.851318 520.078491 160.031250 2223.748779 -283.663879 92.872452 2001.362671 1122.605347 156.803253 
```

### item_pickup

*Action Tick Type playerPositionX playerPositionY playerPositionZ weapon*

**Output Example**

```
Action 147828 item_pickup 2358.369629 921.952942 157.287231 ak47 
```

### item_equip


*Action Tick Type playerPositionX playerPositionY playerPositionZ weapon*

**Output Example**

```
Action 149056 item_equip 2449.139893 2010.219971 128.031250 knife 
```

### item_purchase


*Action Tick Type playerPositionX playerPositionY playerPositionZ weapon*

No Output Example available as it never got logged.

### player_blind

*Action Tick Type playerPositionX playerPositionY playerPositionZ blind_duration*

**Output Example**

```
Action 149056 player_blind 2449.139893 2010.219971 128.031250 3.030241
```

### player_falldamage

*Action Tick Type playerPositionX playerPositionY playerPositionZ damage*

**Output Example**

```
Action 149056 player_blind 2449.139893 2010.219971 128.031250 6.994048 
```






