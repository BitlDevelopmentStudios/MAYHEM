# class that allows sprites to have health events or have special attributes.
import pygame, spriteEngine, math, sys

# objects are things in the world that can be changed and edited.
class Object(spriteEngine.SuperSprite):
    def __init__(self, screen, background, image, **kwargs):
        #INIT
        super().__init__(screen, background, **kwargs)
        self.setImage(image)
        self.imageFile = image
        
    def updateOverride(self):
        # object update
        self.objectUpdate()

    def objectUpdate(self):
        # update method for object
        pass

# actor class. this is a class that defines health and has events for when health is depleted.
class Actor(Object):
    def __init__(self, screen, background, image, health, **kwargs):
        super().__init__(screen, background, image, **kwargs)
        # health
        self.health = health
        self.maxHealth = health
        self.isDead = False
        self.timeSinceLastDamaged = pygame.time.get_ticks()
        self.canBeDamaged = True

    def objectUpdate(self):
        #wait 0.2 seconds before we can be damaged again
        if self.canBeDamaged == False:
            seconds=(pygame.time.get_ticks()-self.timeSinceLastDamaged)/1000
            if seconds > 0.2:
                self.timeSinceLastDamaged = pygame.time.get_ticks()
                self.canBeDamaged = True
        
        #check our health. If we are dead, call the death event.
        if self.health > 0:
            # make sure we don't go above max health.
            if self.health > self.maxHealth:
                self.health = self.maxHealth
            #update our actor
            self.actorUpdate()
        elif self.health <= 0:
            # declare the actor dead
            self.health = 0
            self.isDead = True
            self.actorOnDeath()

    def damage(self, amt):
        # damages the actor. Note that negative values can heal the actor.
        if self.canBeDamaged == True:
            self.health -= amt
            self.canBeDamaged = False

    def actorUpdate(self):
        # update method for actor
        pass

    def actorOnDeath(self):
        # actor death event
        pass

# adds the actor/object to a group
def addObject(actor, pos, group):
    (x,y) = pos
    actor.x = x
    actor.y = y
    group.add(actor)
    
