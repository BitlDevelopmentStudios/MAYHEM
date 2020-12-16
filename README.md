# ![Logo](https://raw.githubusercontent.com/BitlDevelopmentStudios/MAYHEM/main/graphics/logo_small.png)

## Description:
This game is a horde-mode top down shooter where you and a friend must take down hordes of robots, aliens, zombies, and a giant UFO at the end.
This first started off as a single-player platform shooter, but I had issues with platform collisions and I realized that it would have taken way too much time to make as this was a college project built within 2 weeks.
This game was built entiely from scratch, with the exception of the the sprite engine.
The sprite engine was modified from the gameEngine.py from Andy Harris for use in my custom-made engine. (https://www.cs.iupui.edu/~ajharris/pygame/ch10/gameEngine.py)

## Features:
- AI enemies that track down a target (the players) and stand a certain distance away from them to shoot. 3 different types!
- 2 player system. One relying on a keyboard and another relying on a game controller. The second player can also use an alternate keyboard control scheme if there's no controller detected.
- Wave system that spawns more enemies difficult over time.
- Regenerating health!
- Supports an unlocked frame rate!
- Option of 8-way or 360 degree aiming system! (for second player)

## Object Hierarchy:

- SuperSprite (modified super sprite with joystick and keyboard control methods, moving to a position, unlocked framerate and other features.)
- Text (Text that displays on the screen.)
-- Objects (The main objects of the world.)
---- Bullet (Weapon projectile with spread.)
---- Target (Player's crosshair.)
---- Grass (Visual flair)
--- Actors (objects that have health and can "die".)
---- AI (Actors that move around on their own and follow the player. They stop when they are a certain distance away from their targets.)
----- TDSAI (Base AI class built for the game.)
------ TDSAIWeapon (Base AI class that allows shooting bullets. Has options for adjusting fire rate and burst.)
------- Robot (Slow moving metal behemoth that has a lot of health. Shoots red lasers at the player with an auto scatter blaster.)
------- Alien (Fast but weak. Shoots blue lasers at the player with an auto blaster.)
------- UFO (Slow but strong. Final boss that destroys cover. Shoots multiple violet lasers in a huge arc in the front.)
------ Zombie (Slow but attacks players in close range.)
---- Player (Actors that move around using controllers and keyboard)
----- TDSPlayer (Base player class used for the top-down shooter. has regenerating health)
------ TDSPlayer1 (Keyboard user, uses an auto blaster.)
------ TDSPlayer2 (Primarily Controller user, uses an auto scatter blaster.)
---- Cover (Actors used for cover. Destructable by both player and AI bullets.)

## Controls:

- Player 1: 
Movement: W for moving forward, S for moving backwards, A for moving to the left, D for moving to the right.
Combat: Move the crosshair around with the mouse to aim, and press the left mouse button to fire.
- Player 2: 
-- With a controller (tested on an XBOX ONE gamepad): 
Movement: Move with the left joystick or the D-Pad
Combat: Right Joystick to use 360 degree aiming, ABXY to aim with 8-way controls, Right Trigger or Right Bumper to fire.
-- Without a controller: 
Movement: Up Arrow for moving forward, Down Arrow for moving backwards, Left Arrow for moving to the left, Right Arrow for moving to the right.
Combat: Press Right CTRL to fire, then use the movement keys to aim in any direction (8-way controls). Pressing Right CTRL will also stop you from moving, making aiming easier.

# Source Licence info:
![LGPL Logo](https://www.gnu.org/graphics/lgplv3-with-text-154x68.png)

MAYHEM is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

MAYHEM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see https://www.gnu.org/licenses/.