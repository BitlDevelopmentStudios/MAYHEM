""" spriteEngine.py modified from the gameEngine.py from Andy Harris,
    2006

    modified to be more minimal for use in other pygame-built engines so we can use SuperSprite functions without worrying about event registration.
"""

import pygame, math, sys

class SuperSprite(pygame.sprite.Sprite):
    """ An enhanced Sprite class
        Use methods to change image, direction, speed
        Will automatically travel in direction and speed indicated
        Automatically rotates to point in indicated direction
        Five kinds of boundary collision
    """

    def __init__(self, screen, background, **kwargs):
        super().__init__(**kwargs)
        self.screen = screen
        self.background = background
        
        #create constants
        self.WRAP = 0
        self.BOUNCE = 1
        self.STOP = 2
        self.HIDE = 3
        self.CONTINUE = 4
        # kill sthe sprite
        self.KILL = 5
        
        #create a default text image as a placeholder
        #This will usually be changed by a setImage call
        self.font = pygame.font.Font("freesansbold.ttf", 30)
        self.imageMaster = self.font.render(">sprite>", True, (0, 0,0), (0xFF, 0xFF, 0xFF))
        self.image = self.imageMaster
        self.rect = self.image.get_rect()
        
        #create properties
        #most will be changed through method calls
        self.x = 200
        self.y = 200
        # position
        self.pos = (self.x, self.y)
        self.dx = 0
        self.dy = 0
        self.dir = 0
        self.rotation = 0
        self.speed = 0
        self.maxSpeed = 10
        self.minSpeed = -3
        self.boundAction = self.WRAP
        self.pressed = False
        self.oldCenter = (100, 100)
        # init frametime and deltatime (dt)
        self.frametime = 0
        self.dt = 0
    
    def update(self, frametime):
        self.oldCenter = self.rect.center
        #save the frametime and delta time so we have access to these variables.
        self.frametime = frametime
        self.dt = self.frametime >> 10
        self.__rotate()
        self.__calcVector()
        self.__calcPosition()
        self.checkBounds()
        #update position
        self.pos = (self.x, self.y)
        self.rect.center = (self.x, self.y)
        self.updateOverride()
        #checkEvents got removed because whenever it is called, KEYDOWN events didn't apply to the object.

    def updateOverride(self):
        # allows us to call methods in update() without creating and therefore overriding an update function.
        # this was done so we can make our own update functions for player and AI.
        pass

    def __rotate(self):
        """ PRIVATE METHOD
            change visual orientation based on 
            rotation property.
            automatically called in update.
            change rotation property directly or with 
            rotateBy(), setAngle() methods
        """
        oldCenter = self.rect.center
        self.oldCenter = oldCenter
        self.image = pygame.transform.rotate(self.imageMaster, self.rotation)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter
    
    def __calcVector(self):
        """ calculates dx and dy based on speed, dir
            automatically called in update() 
        """
        theta = self.dir / 180.0 * math.pi
        # added delta time so it remains at the same speed regardless of framerate
        self.dx = math.cos(theta) * self.speed * self.dt
        self.dy = math.sin(theta) * self.speed * self.dt
        self.dy *= -1
    
    def __calcPosition(self):
        """ calculates the sprites position adding
            dx and dy to x and y.
            automatically called in update()
        """
        self.x += self.dx
        self.y += self.dy

    def checkBounds(self):
        """ checks boundary and acts based on 
            self.BoundAction.
            WRAP: wrap around screen (default)
            BOUNCE: bounce off screen
            STOP: stop at edge of screen
            HIDE: move off stage and wait
            CONTINUE: keep going at present course and speed
            
            automatically called by update()
        """
        
        scrWidth = self.screen.get_width()
        scrHeight = self.screen.get_height()
        
        #create variables to simplify checking
        offRight = offLeft = offTop = offBottom = offScreen = False
        
        if self.x > scrWidth:
            offRight = True
        if self.x < 0:
            offLeft = True
        if self.y > scrHeight:
            offBottom = True
        if self.y < 0:
            offTop = True
            
        if offRight or offLeft or offTop or offBottom:
            offScreen = True
        
        if self.boundAction == self.WRAP:
            if offRight:
                self.x = 0
            if offLeft:
                self.x = scrWidth
            if offBottom:
                self.y = 0
            if offTop:
                self.y = scrHeight
        
        elif self.boundAction == self.BOUNCE:
            if offLeft or offRight:
                self.dx *= -1
            if offTop or offBottom:
                self.dy *= -1
                
            self.updateVector()
            self.rotation = self.dir
        
        elif self.boundAction == self.STOP:
            if offScreen:
                self.speed = 0
                if offRight:
                    self.x -= 5
                if offLeft:
                    self.x += 5
                if offBottom:
                    self.y -= 5
                if offTop:
                    self.y += 5
        
        elif self.boundAction == self.HIDE:
            if offScreen:
                self.speed = 0
                self.setPosition((-1000, -1000))

        elif self.boundAction == self.KILL:
            if offScreen:
                self.kill()
        
        elif self.boundAction == self.CONTINUE:
            pass
            
        else:
            # assume it's CONTINUE - keep going forever
            pass    
    
    def setSpeed(self, speed):
        """ immediately sets the objects speed to the 
            given value.
        """
        self.speed = speed

    def speedUp(self, amount):
        """ changes speed by the given amount
            Use a negative value to slow down
        """
        self.speed += amount
        if self.speed < self.minSpeed:
            self.speed = self.minSpeed
        if self.speed > self.maxSpeed:
            self.speed = self.maxSpeed
    
    def setAngle(self, dir):
        """ sets both the direction of motion 
            and visual rotation to the given angle
            If you want to set one or the other, 
            set them directly. Angle measured in degrees
        """            
        self.dir = dir
        self.rotation = dir
    
    def turnBy (self, amt):
        """ turn by given number of degrees. Changes
            both motion and visual rotation. Positive is
            counter-clockwise, negative is clockwise 
        """
        self.dir += amt
        if self.dir > 360:
            self.dir = amt
        if self.dir < 0:
            self.dir = 360 - amt
        self.rotation = self.dir
    
    def rotateBy(self, amt):
        """ change visual orientation by given
            number of degrees. Does not change direction
            of travel. 
        """
        self.rotation += amt
        if self.rotation > 360:
            self.rotation = amt
        if self.rotation < 0:
            self.rotation = 360 - amt
    
    def setImage (self, image):
        """ loads the given file name as the master image
            default setting should be facing east.  Image
            will be rotated automatically """
        self.imageMaster = pygame.image.load(image).convert_alpha()
    
    def setDX(self, dx):
        """ changes dx value and updates vector """
        self.dx = dx
        self.updateVector()
    
    def addDX(self, amt):
        """ adds amt to dx, updates vector """
        self.dx += amt
        self.updateVector()
        
    def setDY(self, dy):
        """ changes dy value and updates vector """
        self.dy = dy
        self.updateVector()

    def addDY(self, amt):
        """ adds amt to dy and updates vector """
        self.dy += amt
        self.updateVector()
    
    def setComponents(self, components):
        """ expects (dx, dy) for components
            change speed and angle according to dx, dy values """
            
        (self.dx, self.dy) = components
        self.updateVector()
        
    def setBoundAction (self, action):
        """ sets action for boundary.  Values are
            self.WRAP (wrap around edge - default)
            self.BOUNCE (bounce off screen changing direction)
            self.STOP (stop at edge of screen)
            self.HIDE (move off-stage and stop)
            self.CONTINUE (move on forever)
            Any other value allows the sprite to move on forever
        """
        self.boundAction = action

    def setPosition (self, position):
        """ place the sprite directly at the given position
            expects an (x, y) tuple
        """
        (self.x, self.y) = position
        
    def moveBy (self, vector):
        """ move the sprite by the (dx, dy) values in vector
            automatically calls checkBounds. Doesn't change 
            speed or angle settings.
        """
        (dx, dy) = vector
        self.x += dx
        self.y += dy
        self.checkBounds()

    def forward(self, amt):
        """ move amt pixels in the current direction
            of travel
        """
        
        #calculate dx dy based on current direction
        radians = self.dir * math.pi / 180
        dx = amt * math.cos(radians)
        dy = amt * math.sin(radians) * -1
        
        self.x += dx
        self.y += dy
        
    def addForce(self, amt, angle):
        """ apply amt of thrust in angle.
            change speed and dir accordingly
            add a force straight down to simulate gravity
            in rotation direction to simulate spacecraft thrust
            in dir direction to accelerate forward
            at an angle for retro-rockets, etc.
        """

        #calculate dx dy based on angle
        radians = angle * math.pi / 180
        dx = amt * math.cos(radians)
        dy = amt * math.sin(radians) * -1
        
        self.dx += dx
        self.dy += dy
        self.updateVector()
        
    def updateVector(self):
        #calculate new speed and angle based on dx, dy
        #call this any time you change dx or dy
        
        self.speed = math.sqrt((self.dx * self.dx) + (self.dy * self.dy))
        
        dy = self.dy * -1
        dx = self.dx
        
        radians = math.atan2(dy, dx)
        self.dir = radians / math.pi * 180

    def setSpeedLimits(self, max, min):
        """ determines maximum and minimum
            speeds you will allow through
            speedUp() method.  You can still
            directly set any speed you want
            with setSpeed() Default values:
                max: 10
                min: -3
        """
        self.maxSpeed = max
        self.minSpeed = min

    def dataTrace(self):
        """ utility method for debugging
            print major properties
            extend to add your own properties
        """
        print("x: %d, y: %d, speed: %.2f, dir: %.f, dx: %.2f, dy: %.2f" % \
              (self.x, self.y, self.speed, self.dir, self.dx, self.dy))
            
    def mouseDown_button(self):
        """ boolean function. Returns True if the mouse is 
            clicked over the sprite, False otherwise
        """
        self.pressed = False
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.pressed = True
        return self.pressed
    
    def clicked_button(self):
        """ Boolean function. Returns True only if mouse
            is pressed and released over sprite
            
        """
        released = False
        if self.pressed:
            if pygame.mouse.get_pressed() == (0, 0, 0):
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    released = True
            return released

    def mouseDown(self):
        """ boolean function. Returns True if the mouse is 
            clicked, False otherwise
        """
        self.pressed = False
        if pygame.mouse.get_pressed() == (1, 0, 0):
            self.pressed = True
        return self.pressed
    
    def clicked(self):
        """ Boolean function. Returns True only if mouse
            is pressed and released
        """
        released = False
        if self.pressed:
            if pygame.mouse.get_pressed() == (0, 0, 0):
                released = True
            return released

    # returns true if a key is pressed.
    def isKeyPressed(self,key):
        keys = pygame.key.get_pressed()
        
        if keys[key]:
            return True
        else:
            return False

    # checks if we have any valid joysticks plugged in.
    def isJoystickValid(self):
        try:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            return True
        except:
            return False

    # returns true if a joystick button is pressed.
    def isJoystickButtonPressed(self,buttonID):
        if self.isJoystickValid() == True:
            isPressed = False
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            buttons = joystick.get_numbuttons()
            for i in range(buttons):
                button = joystick.get_button(i)
                if buttonID == i and button == 1:
                    isPressed = True
                    break
            return isPressed

    # returns true if an area of the joystick's d-pad is pressed.
    def isJoystickHatAreaPressed(self, curhatpos):
        if self.isJoystickValid() == True:
            (curhatx,curhaty) = curhatpos
            isPressed = False
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            
            hats = joystick.get_numhats()
            for i in range(hats):
                hat = joystick.get_hat(i)
                (hatx,haty) = hat
                if curhatx != 2:
                     if hatx == curhatx:
                        isPressed = True
                        break
                    
                if curhaty != 2:
                    if haty == curhaty:
                        isPressed = True
                        break
            return isPressed

    # returns true if we move our thumbstick or press the trigger
    def isJoystickAxisChanged(self, curaxis, isMin):
         if self.isJoystickValid() == True:
            isPressed = False
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            
            axes = joystick.get_numaxes()
            for i in range(axes):
                axis = joystick.get_axis(i)
                if curaxis == i:
                    if isMin == True:
                        if axis < -0.6:
                            isPressed = True
                            break
                    elif isMin == False:
                        if axis > 0.6:
                            isPressed = True
                            break
                        
            return isPressed
                
    def collidesWith(self, target):
        """ boolean function. Returns True if the sprite
            is currently colliding with the target sprite,
            False otherwise
        """
        collision = False
        if self.rect.colliderect(target.rect):
            collision = True
        return collision
    
    def collidesGroup(self, target):
        """ wrapper for pygame.sprite.spritecollideany() function
            simplifies checking sprite - group collisions
            returns result of collision check (sprite from group 
            that was hit or None)
        """
        collision = pygame.sprite.spritecollideany(self, target)
        return collision
        
    def distanceTo(self, point):
        """ returns distance to any point in pixels
            can be used in circular collision detection
        """
        (pointx, pointy) = point
        dx = self.x - pointx
        dy = self.y - pointy
        
        dist = math.sqrt((dx * dx) + (dy * dy))
        return dist

    def distanceFromObject(self, obj):
        """ returns distance from any object
            can be used in circular collision detection
        """
        dx = self.x - obj.x
        dy = self.y - obj.y
        
        dist = math.sqrt((dx * dx) + (dy * dy))
        return dist

    """ Returns a bool if we are DIRECTLY ON A SPECIFIC X POSITION of an object.
        """
    def isDirectlyOnX(self, rec1x, rec2x, distance):
        dx = rec1x - rec2x
        dist = math.sqrt((dx * dx))
        
        if dist < distance:
            return True
        else:
            return False

    """ Returns a bool if we are DIRECTLY ON A SPECIFIC Y POSITION of an object.
        """

    def isDirectlyOnY(self, rec1y, rec2y, distance):
        dy = rec1y - rec2y
        dist = math.sqrt((dy * dy))
        
        if dist < distance:
            return True
        else:
            return False
    
    def dirTo(self, point):
        """ returns direction (in degrees) to 
            a point """
        
        (pointx, pointy) = point
        dx = self.x - pointx
        dy = self.y - pointy
        dy *= -1
        
        radians = math.atan2(dy, dx)
        dir = radians * 180 / math.pi
        dir += 180
        return dir

    def moveToPos(self, point, speed, mindistance):
        # move to other object's position
        if self.distanceTo(point) > mindistance:
            self.dir = self.dirTo(point)
            self.forward(speed)
            return False
        else:
            return True
    
    def drawTrace(self, color=(0x00, 0x00, 0x00)):
        """ traces a line between previous position
            and current position of object 
        """
        pygame.draw.line(self.background, color, self.oldCenter,
                         self.rect.center, 3)
        self.screen.blit(self.background, (0, 0))
