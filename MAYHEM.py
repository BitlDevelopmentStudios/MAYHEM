#import projects and init
import pygame, random, math, sys
import actorEngine, playerEngine, aiEngine
pygame.init()

# the game global vars
game_globals = None

class Globals():
    def __init__(self, game):
        #resolution
        self.width, self.height = 800, 600
        self.resolution = (self.width, self.height)
        #debug mode. gives us an FPS counter, god mode, and we can see the hitbox for every object in-game.
        self.debug = False
        #graphics
        self.background_color = (1, 64, 18)
        #sprite groups
        #players
        self.playerSprites = pygame.sprite.Group()
        #enemies
        self.enemySprites = pygame.sprite.Group()
        #cover/walls
        self.coverSprites = pygame.sprite.Group()
        #bullets
        self.bulletSprites = pygame.sprite.Group()
        #the crosshairs
        self.uiSprites = pygame.sprite.Group()
        #GRASS
        self.grassSprites = pygame.sprite.Group()
        #HUD
        self.uiText = pygame.sprite.Group()
        #controller aiming sensitivity
        self.aimingSensitivity = 7
        #damage
        # enemy bullet to player
        self.bulletToPlayerDamage = 7
        # player bullet to enemy
        self.bulletToEnemyDamage = 15
        # zombie to player
        self.zombieToPlayerDamage = 5
        # bullet to cover
        self.bulletToCoverDamage  = 3
        # counter for deaths/kills
        self.playerDeaths = 0
        self.playerKills = 0
        # waves
        self.wave = 0
        self.spawncount = 3
        self.curenemycount = 0
        # the maximum wave we can play up to before we spawn a boss the next wave.
        if self.debug == False:
            self.maxWave = 9
        else:
            self.maxWave = 3
        #game
        self.game = game

# bullet that fires at the enemies/player and dies upon collision.
class Bullet(actorEngine.Object):
    def __init__(self, screen, background, image, spread, **kwargs):
        super().__init__(screen, background, image, **kwargs)
        # make the bullet die upon collision with the window border.
        self.boundAction = self.KILL
        # did we fire?
        self.isFired = False
        #are we an enemy bullet?
        self.isEnemyBullet = False
        # fast bullet
        self.bulletspeed = 7
        self.bulletspread = spread

    def objectUpdate(self):
        # if we fired, move forward.
        if self.isFired == True:
            self.setSpeed(self.bulletspeed)
            self.forward(self.bulletspeed)

    def propel(self, pos):
        self.otherpos = pos
        # move to wherether the other target's position is. Also add some spread too.
        self.dir = self.dirTo(self.otherpos)-(random.randint(-self.bulletspread, self.bulletspread))
        self.rotation = self.dir-90
        self.isFired = True

# the crosshair for player weapons.
class Target(actorEngine.Object):
    def __init__(self, screen, background, **kwargs):
        super().__init__(screen, background, "target.png", **kwargs)
        self.sped = game_globals.aimingSensitivity
        self.boundAction = self.STOP

    #movement functions copied from normal player so we have finer control of the movement on joypad.
    def front(self):
        #moving forward
        self.dir = 90
        self.forward(self.sped)

    def left(self):
        #going left
        self.dir = 180
        self.forward(self.sped)

    def right(self):
        # going right
        self.dir = 0
        self.forward(self.sped)

    def back(self):
        # going backwards
        self.dir = 270
        self.forward(self.sped)

# player with top down shooter capabilities. TODO: add fire rate and burst fire
class TDSPlayer(playerEngine.Player):
    def __init__(self, screen, background, image, **kwargs):
        #assign better sprite
        super().__init__(screen, background, image, 200, **kwargs)
        self.sped = 3
        # create the crosshair
        self.target = Target(screen, background)
        actorEngine.addObject(self.target, self.pos, game_globals.uiSprites)
        self.timeSinceLastRegened = pygame.time.get_ticks()
        # can we regen health?
        self.canRegen = True
        # can we shoot?
        self.canShoot = True
        self.timeSinceLastFired = pygame.time.get_ticks()
        # set weapon settings
        self.bulletsprite = "playerbullet.png"
        self.weaponFireRate = 0.1
        self.spread = 7
        self.bulletCount = 1
        self.stopRectRotate = True

    def actorOnDeath(self):
        # delete player and add a death to our counter.
        self.target.kill()
        game_globals.playerDeaths += 1
        self.kill()

    def playerUpdate(self):
        if self.canRegen == True:
            # regenerate health if we haven't been damaged for at least half a second.
            seconds=(pygame.time.get_ticks()-self.timeSinceLastDamaged)/1000
            if self.health < self.maxHealth and seconds >= 0.5:
                self.health += 5
                self.canRegen = False
        else:
            # regenerate 5 health every 0.05 seconds
            seconds=(pygame.time.get_ticks()-self.timeSinceLastRegened)/1000
            if seconds > 0.05:
                self.timeSinceLastRegened = pygame.time.get_ticks()
                self.canRegen = True

        #wait out our fire rate time to fire next bullet.
        if self.canShoot == False:
            seconds=(pygame.time.get_ticks()-self.timeSinceLastFired)/1000
            if seconds > self.weaponFireRate:
                self.timeSinceLastFired = pygame.time.get_ticks()
                self.canShoot = True

        # rotate to target position.
        self.setAngle(self.dirTo(self.target.pos)-90)
                
        self.TDSPlayerUpdate()

    def TDSPlayerUpdate(self):
        # update for TDSPlayer
        pass

    def shoot(self, count):
        #create and shoot a bullet at the target position.
        if self.canShoot == True:
            cur = 0
        
            while cur < count:
                if cur == count:
                # break the loop if we shot enough.
                    break

                cur += 1
                #shoot bullet at the target.
                bullet = Bullet(self.screen, self.background, self.bulletsprite, self.spread)
                actorEngine.addObject(bullet, self.pos, game_globals.bulletSprites)
                bullet.propel(self.target.pos)
                # reset for firerate
                self.canShoot = False
        
    def front(self):
        #moving forward
        self.dir = 90
        self.forward(self.sped)

    def left(self):
        #going left
        self.dir = 180
        self.forward(self.sped)

    def right(self):
        # going right
        self.dir = 0
        self.forward(self.sped)

    def back(self):
        # going backwards
        self.dir = 270
        self.forward(self.sped)

# player #1, using keyboard controls.
class TDSPlayer1(TDSPlayer):
    def __init__(self, screen, background, **kwargs):
        super().__init__(screen, background, "p1.png", **kwargs)

    def TDSPlayerUpdate(self):
        # place crosshair at mouse position
        (self.target.x,self.target.y) = pygame.mouse.get_pos()

    def keyCustomKeys(self):
        # shoot with left mouse button
        if self.mouseDown() == True:
            self.shoot(self.bulletCount)
            self.onKeyPress()

# player #2, using controller.
class TDSPlayer2(TDSPlayer):
    def __init__(self, screen, background, **kwargs):
        super().__init__(screen, background, "p2.png", **kwargs)
        self.isJoystick = True
        self.lastPressedButton = False
        # change weapon type to suit controller/alt keyboard keys.
        self.spread = 15
        self.bulletCount = 8
        self.weaponFireRate = 0.5
        # where we should move the crosshair based on what direction we point it at (8-way)
        self.targetAimChange = 100
        self.target.boundAction = self.WRAP
        # check if joystick is valid.
        if self.isJoystickValid() == False:
            #warn us that our experience might not be great without a second controller.
            print("This game supports a gamepad for the most optimal gameplay experience on the second player.")

    def TDSPlayerUpdate(self):
        # place the crosshair in front of us if:
        # 1. we are using the alternate layout or
        # 2. we are using the ABXY buttons.
        if ((self.isJoystickValid() == False) and (self.isKeyPressed(pygame.K_LEFT) == False and self.isKeyPressed(pygame.K_RIGHT) == False and self.isKeyPressed(pygame.K_DOWN) == False and self.isKeyPressed(pygame.K_UP) == False)) or (self.lastPressedButton == True and self.isJoystickButtonPressed(0) == False and self.isJoystickButtonPressed(3) == False and self.isJoystickButtonPressed(2) == False and self.isJoystickButtonPressed(1) == False):
            (self.target.x,self.target.y) = (self.x,self.y-self.targetAimChange)

        # toggle movement by pressing and holding RSHIFT on alt layout
        if (self.isJoystickValid() == False) and (self.isKeyPressed(pygame.K_RCTRL) == False):
            self.canMove = True

    def joyCustomKeys(self):
        #joystick movement (360 degrees) with Right Joystick

        # move target around with joystick movement.
        if (self.isJoystickAxisChanged(3, True) == True):
            self.lastPressedButton = False
            self.target.front()
            self.onKeyPress()
            
        if (self.isJoystickAxisChanged(4, True) == True):
            self.lastPressedButton = False
            self.target.left()
            self.onKeyPress()
            
        if (self.isJoystickAxisChanged(4, False) == True):
            self.lastPressedButton = False
            self.target.right()
            self.onKeyPress()

        if (self.isJoystickAxisChanged(3, False) == True):
            self.lastPressedButton = False
            self.target.back()
            self.onKeyPress()
        
        #8-way button aiming with ABXY
        if self.isJoystickButtonPressed(3) == True:
            # align target
            if self.isJoystickButtonPressed(2) == False and self.isJoystickButtonPressed(1) == False:
                self.target.x = self.x
                
            self.target.y = self.y-self.targetAimChange
            self.lastPressedButton = True
            self.onKeyPress()
            
        if self.isJoystickButtonPressed(2) == True:
            # align target
            if self.isJoystickButtonPressed(0) == False and self.isJoystickButtonPressed(3) == False:
                self.target.y = self.y
                
            self.target.x = self.x-self.targetAimChange
            self.lastPressedButton = True
            self.onKeyPress()
            
        if self.isJoystickButtonPressed(1) == True:
            # align target
            if self.isJoystickButtonPressed(0) == False and self.isJoystickButtonPressed(3) == False:
                self.target.y = self.y
                
            self.target.x = self.x+self.targetAimChange
            self.lastPressedButton = True
            self.onKeyPress()

        if self.isJoystickButtonPressed(0) == True:
            # align target
            if self.isJoystickButtonPressed(2) == False and self.isJoystickButtonPressed(1) == False:
                self.target.x = self.x
                
            self.target.y = self.y+self.targetAimChange
            self.lastPressedButton = True
            self.onKeyPress()

        # shooting with RB or RT
        if (self.isJoystickButtonPressed(5) == True) or (self.isJoystickAxisChanged(2, True) == True):
            self.shoot(self.bulletCount)
            self.onKeyPress()

    def keyCustomKeys(self):
        # when shooting, align the crosshair to wherever we move.
        if self.isKeyPressed(pygame.K_DOWN) == True:
            # align target
            if self.isKeyPressed(pygame.K_LEFT) == False and self.isKeyPressed(pygame.K_RIGHT) == False:
                self.target.x = self.x
            
            self.target.y = self.y+self.targetAimChange
            self.onKeyPress()
            
        if self.isKeyPressed(pygame.K_LEFT) == True:
            # align target
            if self.isKeyPressed(pygame.K_DOWN) == False and self.isKeyPressed(pygame.K_UP) == False:
                self.target.y = self.y
                
            self.target.x = self.x-self.targetAimChange
            self.onKeyPress()
            
        if self.isKeyPressed(pygame.K_RIGHT) == True:
            # align target
            if self.isKeyPressed(pygame.K_DOWN) == False and self.isKeyPressed(pygame.K_UP) == False:
                self.target.y = self.y
                
            self.target.x = self.x+self.targetAimChange
            self.onKeyPress()

        if self.isKeyPressed(pygame.K_UP) == True:
            # align target
            if self.isKeyPressed(pygame.K_LEFT) == False and self.isKeyPressed(pygame.K_RIGHT) == False:
                self.target.x = self.x
                
            self.target.y = self.y-self.targetAimChange
            self.onKeyPress()
        
        if self.isKeyPressed(pygame.K_RCTRL) == True:
            #shoot with RCTRL
            self.shoot(self.bulletCount)
            self.onKeyPress()
            self.canMove = False

# AI
# base AI class that is built for the top down shooter.
class TDSAI(aiEngine.AI):
    def __init__(self, screen, background, image, health, speed, distance, name, **kwargs):
        super().__init__(screen, background, image, health, None, speed, distance, **kwargs)
        # have we decided a target?
        self.decidedTarget = False
        self.name = name

    def actorOnDeath(self):
        # actor death event
        game_globals.playerKills += 1
        game_globals.curenemycount -= 1
        self.kill()

    def aiUpdate(self):
        if self.target != None:
            self.setAngle(self.dirTo(self.target.pos)-90)
        
        # update method for ai
        if self.decidedTarget == False:
            # choose random target
            randtar = random.randint(0,2)
            if randtar == 0:
                self.target = game_globals.game.player1
                self.decidedTarget = True
            elif randtar == 1:
                self.target = game_globals.game.player2
                self.decidedTarget = True
        else:
            # if one player or the other are dead, target whichever player is left.
            if game_globals.game.player1.isDead == True:
                self.target = game_globals.game.player2
                self.decidedTarget = True
            elif game_globals.game.player2.isDead == True:
                self.target = game_globals.game.player1
                self.decidedTarget = True
            # if both are dead, stop looking for targets.
            elif game_globals.game.player2.isDead == True and game_globals.game.player1.isDead == True:
                self.target = None
            
        self.shootingAIUpdate()

    def shootingAIUpdate(self):
        # update method for shooting ai
        pass

# base AI class that allows shooting of bullets.
class TDSAIWeapon(TDSAI):
    def __init__(self, screen, background, image, health, speed, name, bulletsprite, spread, fireRate, bulletCount, **kwargs):
        super().__init__(screen, background, image, health, speed, 100, name, **kwargs)
        #can we shoot?
        self.canShoot = False
        self.timeSinceLastFired = pygame.time.get_ticks()
        # force us to stop shooting if the players die.
        self.forceStopShooting = False
        # set weapon settings
        self.bulletsprite = bulletsprite
        self.spread = spread
        self.weaponFireRate = fireRate
        self.bulletCount = bulletCount

    #shooting events
    def shootingAIUpdate(self):
        # check if we are forced to stop shooting.
        if self.forceStopShooting == False:
            if self.target != None:
                # fire our bullet
                self.shoot(self.bulletCount)
                
                #wait out our fire rate time to fire next bullet.
                if self.canShoot == False:
                    seconds=(pygame.time.get_ticks()-self.timeSinceLastFired)/1000
                    if seconds > self.weaponFireRate:
                        self.timeSinceLastFired = pygame.time.get_ticks()
                        self.canShoot = True

    def shoot(self, count):
        #create and shoot a bullet at the target position.
        if self.canShoot == True:
            cur = 0
        
            while cur < count:
                if cur == count:
                # break the loop if we shot enough.
                    break

                #shoot bullet at the target.
                cur += 1
                bullet = Bullet(self.screen, self.background, self.bulletsprite, self.spread)
                bullet.isEnemyBullet = True
                actorEngine.addObject(bullet, self.pos, game_globals.bulletSprites)
                bullet.propel(self.target.pos)

                # reset for firerate
                self.canShoot = False

#I AM A ROBOT. match for player 2
class Robot(TDSAIWeapon):
    def __init__(self, screen, background, **kwargs):
        super().__init__(screen, background, "robot.png", 150, 1, "Robot", "robotbullet.png", 15, 0.5, 8, **kwargs)

#blarg. match for player 1
class Alien(TDSAIWeapon):
    def __init__(self, screen, background, **kwargs):
        super().__init__(screen, background, "alien.png", 100, 1.5, "Alien", "alienbullet.png", 7, 0.1, 1, **kwargs)

#the mothership. final boss
class UFO(TDSAIWeapon):
    def __init__(self, screen, background, **kwargs):
        super().__init__(screen, background, "ufo.png", 500, 0.3, "UFO", "ufobullet.png", 90, 0.1, 2, **kwargs)
        #increase the size of the collision box...
        self.collideRect =  pygame.rect.Rect((0, 0), (self.image.get_width()/2,self.image.get_height()*2))

#brains...
class Zombie(TDSAI):
    def __init__(self, screen, background, **kwargs):
        super().__init__(screen, background, "zombie.png", 75, 0.5, 30, "Zombie", **kwargs)

# the cover
class Cover(actorEngine.Actor):
    def __init__(self, screen, background, health, **kwargs):
        super().__init__(screen, background, "platform.png", health, **kwargs)

    def actorOnDeath(self):
        # actor death event
        self.kill()

# grass. adds some visual flair to the scene.
class Grass(actorEngine.Object):
    def __init__(self, screen, background, **kwargs):
        super().__init__(screen, background, "grass.png", **kwargs)

# Displays text in a specific position. Used for UI/HUD    
class Text(pygame.sprite.Sprite):
    def __init__ (self, font, text, color, size, pos):
        pygame.sprite.Sprite. __init__ (self)
        self.position = pos
        #set font and create text image.
        self.font = pygame.font.SysFont(font, size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        # relative to the top left of the window
        self.rect.left, self.rect.top = pos

# the game code
class Game():
    def spawnRandomCover(self, count):
        #creates cover objects in the map.
        cur = 0
        
        while cur < count:
            # break the loop if we spawned enough
            if cur == count:
                break

            # Spawn cover
            cur += 1
            actorEngine.addObject(Cover(self.screen, self.background, random.randint(40,150)), (random.randint(0,game_globals.width), random.randint(0,game_globals.height)), game_globals.coverSprites)

    def spawnGrass(self, count):
        #creates grass objects in the map.
        cur = 0
        
        while cur < count:
            # break the loop if we spawned enough
            if cur == count:
                break

            # Spawn grass
            cur += 1
            actorEngine.addObject(Grass(self.screen, self.background), (random.randint(0,game_globals.width), random.randint(0,game_globals.height)), game_globals.grassSprites)

    # spawn the players.
    def spawnPlayers(self):
        # spawns players in random position.
        (player1x,player1y) = (random.randint(0,game_globals.width),random.randint(0,game_globals.height))
        p1pos = (player1x,player1y)
        #move the second player a bit.
        p2pos = (player1x,player1y + 50)
        
        # init player1
        self.player1 = TDSPlayer1(self.screen, self.background)
        #change starting pos
        actorEngine.addObject(self.player1, p1pos, game_globals.playerSprites)
        # init player2
        self.player2 = TDSPlayer2(self.screen, self.background)
        #change starting pos
        actorEngine.addObject(self.player2, p2pos, game_globals.playerSprites)

    # spawn multiple AI enemies in random locations.
    def spawnAIs(self):
        while game_globals.curenemycount < game_globals.spawncount:
            # break the loop if we spawned all the enemies.
            if game_globals.curenemycount == game_globals.spawncount:
                break

            # increment the current enemy count
            game_globals.curenemycount += 1
            image = ""
            newAI = None

            # grab a random enemy and spawn
            randim = random.randint(0,2)

            if randim == 0:
                newAI = Robot(self.screen, self.background)
            elif randim == 1:
                newAI = Alien(self.screen, self.background)
            elif randim == 2:
                newAI = Zombie(self.screen, self.background)
                
            actorEngine.addObject(newAI, (random.randint(0,game_globals.width), random.randint(0,game_globals.height)), game_globals.enemySprites)

    #display UI text in the world.
    def displayText(self, text, pos):
        notification = Text(pygame.font.get_default_font(), text, (0,0,0), 30, pos)
        return notification

    # begin a new wave and spawn random enemies.
    def newWave(self):
        game_globals.wave += 1
        game_globals.curenemycount = 0
        game_globals.spawncount += 1
        self.spawnAIs()

    # update the HUD/UI text.
    def addHUDText(self):
        # tell us if the players are dead or not
        p1hp = str(self.player1.health) + "/" + str(self.player1.maxHealth)
        if self.player1.isDead == True:
            p1hp = "DECEASED"

        p2hp = str(self.player2.health) + "/" + str(self.player2.maxHealth)
        if self.player2.isDead == True:
            p2hp = "DECEASED"

        # display all the text.
        notification1 = self.displayText("PLAYER 1 HEALTH: " + str(p1hp), (0,0))
        notification2 = self.displayText("PLAYER 2 HEALTH: " + str(p2hp), (0,20))
        notification3 = self.displayText("KILLS: " + str(game_globals.playerKills), (0,40))
        notification4 = self.displayText("WAVE " + str(game_globals.wave) + " | " + str(game_globals.curenemycount) + "/" + str(game_globals.spawncount), (0,60))
        game_globals.uiText.add(notification1, notification2, notification3, notification4)

    # game logic code
    def gameLogic(self):
        #update the user interface
        game_globals.uiText.empty()
        self.addHUDText()

        # if both players are dead or we triggered the ending, end the game
        if game_globals.playerDeaths == 2 or self.gameEnd == True:
            # stop the AI from shooting.
            for en in game_globals.enemySprites:
                en.forceStopShooting = True

            # choose the text depending on if the game ends or if we lost.
            notificationText = "GAME OVER!"

            if self.gameEnd == True:
                notificationText = "GAME COMPLETE!"

            # update the text and show cursor
            notification5 = self.displayText(notificationText, (0,80)) 
            game_globals.uiText.add(notification5)
            
            pygame.mouse.set_visible(True)
        # print the text "LAST MAN STANDING!" if there is only one player left standing.
        elif game_globals.playerDeaths == 1:
            # update the text 
            notification5 = self.displayText("LAST MAN STANDING!", (0,80))
            game_globals.uiText.add(notification5)

        # show the boss health if the boss exists.
        if self.finalBoss != None:
            if self.finalBoss.health > 0:
                notification6 = self.displayText("UFO HEALTH: " + str(self.finalBoss.health), (0,100)) 
                game_globals.uiText.add(notification6)

        # add debug frame rate counter
        if game_globals.debug == True:
            notification7 = self.displayText("FPS: " + str(int(self.clock.get_fps())), (0,120)) 
            game_globals.uiText.add(notification7)

        # if all enemies are dead
        if game_globals.curenemycount <= 0:
            # if we are on at least wave 2
            if game_globals.wave < game_globals.maxWave:
                # begin new wave
                self.newWave()
            elif game_globals.wave == game_globals.maxWave:
                # begin final wave. we set the wave manually.
                game_globals.wave += 1
                game_globals.spawncount = 6

                # Spawn other enemies. We subtract 1 because of the FINAL BOSS.
                while game_globals.curenemycount < game_globals.spawncount  - 1:
                    # break the loop if we spawned all the enemies.
                    if game_globals.curenemycount == game_globals.spawncount - 1:
                        break

                    # increment the current enemy count
                    game_globals.curenemycount += 1
                    image = ""
                    newAI = None

                    # grab a random enemy and spawn
                    rand = random.randint(0,2)

                    if rand == 0:
                        newAI = Robot(self.screen, self.background)
                    elif rand == 1:
                        newAI = Alien(self.screen, self.background)
                    elif rand == 2:
                        newAI = Zombie(self.screen, self.background)
                
                    actorEngine.addObject(newAI, (random.randint(0,game_globals.width), random.randint(0,game_globals.height)), game_globals.enemySprites)

                # spawn the FINAL BOSS and increase current enemy count
                self.finalBoss = UFO(self.screen, self.background)
                actorEngine.addObject(self.finalBoss, (random.randint(0,game_globals.width), random.randint(0,game_globals.height)), game_globals.enemySprites)
                game_globals.curenemycount += 1
            else:
                self.gameEnd = True

    # collisions for player, bullets, and cover.
    def updateCollisions(self):
        for cov in game_globals.coverSprites:
            for ply in game_globals.playerSprites:
                # Collide with every part of the wall.
                if ply.collideRect.colliderect(cov.rect):
                    ply.collide(cov.rect)

            for en in game_globals.enemySprites:
                if en.name != "UFO":
                    if en.collideRect.colliderect(cov.rect):
                        en.collide(cov.rect)
                else:
                    # if we are the UFO boss, DESTROY COVER.
                    if en.collidesWith(cov):
                        if en.distanceFromObject(cov) < 30:
                            cov.kill()

            # destroy bullets upon collision with cover.
            for bull in game_globals.bulletSprites:
                if bull.collidesWith(cov):
                    cov.damage(game_globals.bulletToCoverDamage)
                    bull.kill()

        for bull in game_globals.bulletSprites:
            # player bullets damage enemies
            for en in game_globals.enemySprites:
                if bull.collidesWith(en) and bull.isEnemyBullet == False:
                    en.damage(game_globals.bulletToEnemyDamage)
                    bull.kill()

        if game_globals.debug == False:
            for bull in game_globals.bulletSprites:
                # enemy bullets damage players
                for ply in game_globals.playerSprites:
                    if bull.collidesWith(ply) and bull.isEnemyBullet == True:
                        ply.damage(game_globals.bulletToPlayerDamage)
                        bull.kill()

            # make zombies damage players on collision
            for en in game_globals.enemySprites:
                for ply in game_globals.playerSprites:
                    if ply.collidesWith(en) and en.name == "Zombie":
                        ply.damage(game_globals.zombieToPlayerDamage)

    # update all active objects in the world.
    def updateGameObjects(self, frametime):
        game_globals.enemySprites.clear(self.screen, self.background)
        game_globals.playerSprites.clear(self.screen, self.background)
        game_globals.grassSprites.clear(self.screen, self.background)
        game_globals.coverSprites.clear(self.screen, self.background)
        game_globals.bulletSprites.clear(self.screen, self.background)
        game_globals.uiText.clear(self.screen, self.background)
        game_globals.uiSprites.clear(self.screen, self.background)

        # keep enemy sprites on top to prevent a glitch where enemies stop shooting.
        # update frametime for all objects
        game_globals.uiSprites.update(frametime)
        game_globals.enemySprites.update(frametime)
        game_globals.playerSprites.update(frametime)
        game_globals.grassSprites.update(frametime)
        game_globals.coverSprites.update(frametime)
        game_globals.bulletSprites.update(frametime)
        
        game_globals.grassSprites.draw(self.screen)
        game_globals.enemySprites.draw(self.screen)
        game_globals.playerSprites.draw(self.screen)
        game_globals.coverSprites.draw(self.screen)
        if game_globals.debug == True:
            #color coded for debugging cover collisions
            for cov in game_globals.coverSprites:
                pygame.draw.rect(self.screen, (0,255,255), cov.rect, 2)
            for en in game_globals.enemySprites:
                pygame.draw.rect(self.screen, (255,0,0), en.collideRect, 2)
            for ply in game_globals.playerSprites:
                pygame.draw.rect(self.screen, (0,255,0), ply.collideRect, 2)
        game_globals.bulletSprites.draw(self.screen)
        game_globals.uiSprites.draw(self.screen)
        game_globals.uiText.draw(self.screen)

    # quit the game.
    def quit(self):
        pygame.display.quit()
        pygame.quit()
        self.keepGoing = False
        sys.exit()
    
    def start(self):
        # init graphics
        self.screen = pygame.display.set_mode(game_globals.resolution)
        pygame.display.set_caption("MAYHEM")
        pygame.mouse.set_visible(False)

        #init joystick module
        pygame.joystick.init()

        # init background
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(game_globals.background_color)
        self.screen.blit(self.background, (0, 0))

        # spawn the players in random loocations
        self.spawnPlayers()

        # Spawn cover objects all over the world.
        self.spawnRandomCover(20)

        # spawn grass all over the world.
        self.spawnGrass(100)

        # spawn wave 1. We don't spawn random enemies yet so each player can get used to each individual enemy type.
        game_globals.wave = 1
        game_globals.spawncount = 3
        newAI1 = Robot(self.screen, self.background)
        newAI2 = Alien(self.screen, self.background)
        newAI3 = Zombie(self.screen, self.background)
        actorEngine.addObject(newAI1, (random.randint(0,game_globals.width), random.randint(0,game_globals.height)), game_globals.enemySprites)
        actorEngine.addObject(newAI2, (random.randint(0,game_globals.width), random.randint(0,game_globals.height)), game_globals.enemySprites)
        actorEngine.addObject(newAI3, (random.randint(0,game_globals.width), random.randint(0,game_globals.height)), game_globals.enemySprites)
        game_globals.curenemycount = game_globals.spawncount

        # the final boss
        self.finalBoss = None

        # game loop
        self.clock = pygame.time.Clock()
        self.keepGoing = True
        self.gameEnd = False

        while self.keepGoing:
            #no delay since the game can run at an unlocked framerate now.
            frametime = self.clock.tick(0)

            #game exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            #game logic
            self.gameLogic()

            # update everything
            self.updateCollisions()
            self.updateGameObjects(frametime)

            #update display
            pygame.display.flip()

# does things when we quit the app.
def onQuit():
    if pygame.joystick.get_init() == True:
        pygame.joystick.quit()

# game startup
if __name__ == "__main__":
    game = Game()
    game_globals = Globals(game)
    game.start()
    onQuit()
        
