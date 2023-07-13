# Requirements:
1. sudo apt mpg123 install

# Controls:

1. W/S/A/D : king movement
2. <SPACE> : king normal attack
3. l : king levaithan axe attack
4. h : health spell
5. r : rage spell
6. 1/2/3: barbarian spawning
7. n : nuke
8. q : quit

# Implemented features and Bonus:

#### OOPS CONCEPTS (20)
1. Inheritance : done for Class Building : containing townhall, walls, canons, huts and similarly for moving characters 
2. Polymorphism: barbarians have their own attack function that overrides inherited attack function
3. Encapsulation: used a class and object based approach throughout
4. Abstractrion: we have different methods within the class just like move() or attack() etc.

#### Village (20):
1. Spawning Points: have 3 spawning predefined spawning points controlled using keys:- '1', '2', '3'.

2. TownHall: only one townhall placed near centre and has size 4*3

3. Huts: have 5 huts of size 1*1 

4. Walls: there are walls which are acting as boundary to protect the village, have size 1*1

5. There are two canons which can shoot within 6-tile range. At a given point the canon targets a single troop and priority is king.

6. All buildings have a health attribute and the color of the building depends on the following split:
- Green: 50% to 100% hitpoints
- Yellow: 20%-50% hitpoints
- Red: 0%-20% hitpoints
- A building with 0 hit points is considered destroyed and is not displayed on the screen or targeted by troops.


#### King (20):
1. W/S/A/D controls for king
2. <SPACE> is used for normal attack
3. The King attacks a single location with a sword. This location is specified relative to the location of the king, any building present in that location would be damaged by the king’s attack.

4. Attributes:
- Damage/attack_power
- health bar shown at the bottom all the times
- When the health of the king drops to 0, the King would be dead and cannot move or attack anymore.
- Movement Speed: The distance that the king moves in each time step. One adjacent block movement is 1 move/time step

#### Barbarians (15):
1. Attributes:
- Damage/attack_power
- Health and color changes : green, yellow, red 
- Once the health of a barbarian drops to 0, they are considered dead and
cannot move or attack any longer.
-  Movement Speed: The distance that the king moves in each time step. One adjacent block movement is 1 move/time step

2. Movement : The barbarians will always try to attack the nearest non-wall building and will always move towards it. The barbarian movement is automated. If there is a wall in its path then the barbarian is expected to first destroy the wall and then move forward.

#### Spells (5):
- Both Rage and Health Spell implemented

#### Game Endings (5):
- Implemented

#### Replay (15):
- Done, replays getting saved in a seperate replay folder

#### Bonus:
- Leviathan Axe for king implemented (10)
- Extra features:
1. Nuke weapon : A Nuke gets launched and destroys the townhall (with a sound effect)

2. Score board : A dynamic score board in which barbarians will try to break more walls on way but in an optimistic manner

3. Barbarian count and limit : there is a limit on barbarians that can be deployed

