# class that allows sprites to play the game like a player.
import pygame, spriteEngine, actorEngine, math, sys

class Player(actorEngine.Actor):
    def __init__(self, screen, background, image, health, **kwargs):
        super().__init__(screen, background, image, health, **kwargs)
        # do we use the joystick/alt layout?
        self.isJoystick = False
        # Can we move?
        self.canMove = True
        #proxy collision object.
        self.collideRect =  pygame.rect.Rect((0, 0), (self.image.get_width()/4,self.image.get_height()))
        self.collideRect.center = (int(self.x), int(self.y))
        
    def actorUpdate(self):
        # update collision box
        self.collideRect.center = (int(self.x), int(self.y))
        
        #update keys
        self.playerKeys()
        self.playerUpdate()

    def playerUpdate(self):
        #update the player.
        pass

    def playerKeys(self):
        if self.isJoystick == False:
            # move with keyboard (WASD)
            if self.canMove == True:
                if self.isKeyPressed(pygame.K_w) == True:
                    self.front()
                    self.onKeyPress()
            
                if self.isKeyPressed(pygame.K_a) == True:
                    self.left()
                    self.onKeyPress()
            
                if self.isKeyPressed(pygame.K_d) == True:
                    self.right()
                    self.onKeyPress()

                if self.isKeyPressed(pygame.K_s) == True:
                    self.back()
                    self.onKeyPress()

            self.keyCustomKeys()
        elif self.isJoystick == True:
            if self.isJoystickValid() == True:
                if self.canMove == True:
                    # move with left joystick
                    if (self.isJoystickAxisChanged(1, True) == True) or (self.isJoystickHatAreaPressed((2,1)) == True):
                        self.front()
                        self.onKeyPress()
            
                    if (self.isJoystickAxisChanged(0, True) == True) or (self.isJoystickHatAreaPressed((-1,2)) == True):
                        self.left()
                        self.onKeyPress()
            
                    if (self.isJoystickAxisChanged(0, False) == True) or (self.isJoystickHatAreaPressed((1,2)) == True):
                        self.right()
                        self.onKeyPress()

                    if (self.isJoystickAxisChanged(1, False) == True) or (self.isJoystickHatAreaPressed((2,-1)) == True):
                        self.back()
                        self.onKeyPress()

                self.joyCustomKeys()
            else:
                if self.canMove == True:
                    # move with alt. keyboard layout. (UP, DOWN, LEFT, RIGHT arrows)
                    if self.isKeyPressed(pygame.K_UP) == True:
                        self.front()
                        self.onKeyPress()
            
                    if self.isKeyPressed(pygame.K_LEFT) == True:
                        self.left()
                        self.onKeyPress()
            
                    if self.isKeyPressed(pygame.K_RIGHT) == True:
                        self.right()
                        self.onKeyPress()

                    if self.isKeyPressed(pygame.K_DOWN) == True:
                        self.back()
                        self.onKeyPress()

                self.keyCustomKeys()

    def keyCustomKeys(self):
        # allows us to define custom keyboard code
        pass

    def joyCustomKeys(self):
        # allows us to define custom joypad code
        pass

    def onKeyPress(self):
        # Do something on keypress
        pass

    def collide(self,rect):
        #collision event. push the player/enemy back a bit depending on the side we hit.
        if self.isDirectlyOnY(rect.top, self.collideRect.bottom, 30):
            self.y -= 3
        elif self.isDirectlyOnY(rect.bottom, self.collideRect.top, 30):
            self.y += 3
            
        if self.isDirectlyOnX(rect.left, self.collideRect.right, 30):
            self.x -= 3
        elif self.isDirectlyOnX(rect.right, self.collideRect.left, 30):
            self.x += 3

    def front(self):
        #going forward
        pass

    def left(self):
        #going left
        pass

    def right(self):
        # going right
        pass

    def back(self):
        # going backward
        pass
