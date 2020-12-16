# class that allows sprites to track a specific target down and stay at a certain distance

import pygame, spriteEngine, actorEngine, math, sys, random

# the base class of enemies.
class AI(actorEngine.Actor):
    def __init__(self, screen, background, image, health, target, speed, distance, **kwargs):
        super().__init__(screen, background, image, health, **kwargs)
        # the target enemy
        self.target = target
        # min distance to enemy to stop.
        self.minDistToEnemy = distance
        self.sped = speed
        self.collided = False
        self.timeSinceLastCollided = pygame.time.get_ticks()
        #proxy collision object.
        self.collideRect =  pygame.rect.Rect((0, 0), (self.image.get_width()/4,self.image.get_height()))
        self.collideRect.center = (int(self.x), int(self.y))

    def actorUpdate(self):
        # update collision box
        self.collideRect.center = (int(self.x), int(self.y))

        if self.collided == True:
            seconds=(pygame.time.get_ticks()-self.timeSinceLastCollided)/1000
            if seconds > 0.07:
                self.timeSinceLastCollided = pygame.time.get_ticks()
                self.collided = False
        else:
            # move to the target.
            if self.target != None:
                self.moveToPos(self.target.pos, self.sped, self.minDistToEnemy)
            
        # allow custom AI code.
        self.aiUpdate()

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

        self.collided = True

    def aiUpdate(self):
        # update method for ai
        pass
