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

*Action Tick Type*

This part of the output is common to all events. Then, for some events, the output continues. Here they are.

Note that the events not listed below follow the standard output definition.

### weapon_fire

*Action Tick Type weapon*

**Output Example**

```
Action 250360 weapon_fire 867.432922 2405.222412 144.230499 weapon_hegrenade
```

### player_death *

We differenciated the player_death event in three "sub-events".
- *player_death_k* : The target player killed someone.
- *player_death_a* : The target player assisted a kill.
- *player_death_d* : The target player died.

*Action Tick Type(_k/_a/_d)*

**Output Example**

```
Action 293485 player_death_k 
```

### item_pickup

*Action Tick Type weapon*

**Output Example**

```
Action 147828 item_pickup ak47 
```

### item_equip


*Action Tick Type weapon*

**Output Example**

```
Action 149056 item_equip knife 
```

### item_purchase


*Action Tick Type weapon*

No Output Example available as it never got logged.

### player_blind

*Action Tick Type blind_duration*

**Output Example**

```
Action 149056 player_blind 3.030241
```

### player_falldamage

*Action Tick Type damage*

**Output Example**

```
Action 149056 player_blind 6.994048 
```
