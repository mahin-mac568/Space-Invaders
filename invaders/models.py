"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

# Mahin Chowdhury 
# 12/4/18
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y, width, height, source):
        super().__init__(x=x, y=y, width=SHIP_WIDTH, height=SHIP_HEIGHT,
                         source='ship.png')
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.
    """

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, width, height, source):
        super().__init__(x=x, y=y, width=ALIEN_WIDTH, height=ALIEN_HEIGHT,
                         source=source)


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getVelocity(self):
        """
        Returns the value of the hidden attribute _velocity
        """
        return self._velocity
    # INITIALIZER TO SET THE VELOCITY

    def __init__(self, x, y, width, height, fillcolor, velocity=BOLT_SPEED):
        super().__init__(x=x, y=y, width=BOLT_WIDTH,
                         height=BOLT_HEIGHT, fillcolor=fillcolor)
        self._velocity = velocity

    # MORE METHODS AS NECESSARY

    def isplayerbolt(self):
        """
        Returns True if the _velocity is positive, False otherwise
        """
        if self._velocity > 0:
            return True
        else:
            return False


class sound():
    """
    A class representing sound

    INSTANCE ATTRIBUTES:
        source: the sound file to play [.wav file]
        volume: how loud the sound is in range 0..1, 0 being muted and 1 being the loudest
    """

    def __init__(self, source, volume=1):
        self.source = source
        self.volume = volume
