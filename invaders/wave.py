"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# Mahin Chowdhury mac568
  William Lee wl433
# 12/4/18
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    _right:   True for right,
              False for left

    _rate:    A random int in range 1..BOLT_RATE
              The number of steps the aliens will take before firing another bolt

    _steps:   int in range 1..BOLT_RATE
              The number of steps taken by the aliens

    _win:     True if all elements in the nested list of Alien objects are None

    _firesound: the sound object for the player shooting bolts [.WAV file]

    _deathsound: the sound object for the aliens being collided with the bolts [.WAV file]

    _alienspeed: the speed of the aliens marching [int]
    """


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAliens(self):
        """Returns the value of the hidden attribute _aliens"""
        return self._aliens

    def getShip(self):
        """Returns the value of the hidden attribute _ship"""
        return self._ship

    def setShip(self, value):
        """Modifies the value of the hidden attribute _ship"""
        assert isinstance(value,Ship)
        self._ship = value

    def getDefense(self):
        """Returns the value of the hidden attribute _dline"""
        return self._dline

    def getBolts(self):
        """Returns the value of the hidden attribute _bolts"""
        return self._bolts

    def getLives(self):
        """Returns the value of the hidden attribute _lives"""
        return self._lives

    def getWin(self):
        """Returns the value of the hidden attribute _win"""""
        return self._win

    def getfiresound(self):
        """Returns the value of the hidden attribute _firesound"""
        return self._firesound

    def getdeathsound(self):
        """Returns the value of the hidden attribute _deathsound"""
        return self._deathsound

    def getAlienspeed(self):
        """"Returns the value of the hidden attribute _alienspeed"""
        return self._alienspeed

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, alienspeed):
        """
        Initializes the Wave of aliens.

        Parameter alienspeed: the speed of the aliens
        Precondition: alienspeed is an int or float
        """
        self._aliens = self.alienrows()
        self._ship = self.player()
        self._dline = GPath(points = [0, DEFENSE_LINE, GAME_WIDTH,DEFENSE_LINE], linecolor = 'black')
        self._time = 0
        self._right = True
        self._bolts = []
        self._rate = random.randint(1,BOLT_RATE)
        self._steps = 0
        self._lives = 3
        self._win = False
        self._firesound = Sound('pew1.wav')
        self._deathsound = Sound('blast1.wav')
        self._alienspeed = alienspeed

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, time):
        """
        Walks the aliens back and forth: Move the aliens to the right ALIEN_H_WALK pixels
        every ALIEN_SPEED seconds. When the the rightmost alien is less than ALIEN_H_SEP
        pixels from the right wall, walk the aliens down ALIEN_V_WALK pixels down only once,
        then walk the aliens to the left ALIEN_H_WALK pixels every ALIEN_SPEED seconds. When
        the leftmost alien is less than ALIEN_H_SEP distance from the left wall, walk the
        aliens down ALIEN_V_WALK pixels down only once, then reverse the horizontal direction
        of the aliens. Keep repeating this movement until the game is over.

        For a player bolt on the screen, continually increase its y-position by BOLT_SPEED
        until it either the bolt reaches y=GAME_HEIGHT or it touches an alien. Then remove that
        bolt from the screen. For an alien bolt on the screen, continually decrease its y-position
        by BOLT_SPEED until it either reaches y=0 or it touches the ship. Then remove that bolt
        from the screen. When a player bolt is contained by and alien image, or an alien bolt is
        contained by the ship image, delete that image.

        If the bottom-most alien in a wave reaches the defense line, set the player's lives equal
        to zero. If all of the aliens in the wave are None, set the _win attribute to True.

        Parameter time: The time in seconds since last update
        Precondition: time is a number (int or float)
        """
        rand1 = random.randint(0,ALIEN_ROWS-1)
        rand2 = random.randint(0,len(self._aliens)-1)
        if self._right == True:
            self.aliensmoveright(time)
        if self._right == False:
            self.aliensmoveleft(time)
        if self.rightmostalien() != None and (GAME_WIDTH - self.rightmostalien().x) <= ALIEN_H_SEP and self._time == 0:
            self._right = False
            self.aliensmovedown()
        if self.leftmostalien() != None and self.leftmostalien().x <= ALIEN_H_SEP and self._time == 0:
            self._right = True
            self.aliensmovedown()
        for x in self._bolts:
            if x.isplayerbolt():
                x.y += BOLT_SPEED
                self.del_player_bolt()
            else:
                x.y -= BOLT_SPEED
                self.del_alien_bolt()
        self.alienbolts(rand2, rand1)
        self.aliencollide()
        self.shipcollide()
        self.breach()
        self.victory()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Iterates through the 2d list of aliens and draws each alien if it is not None.
        Draws the ship if it is not None.
        Draws the defense line.
        Iterates throught the list of bolts and and draws each bolt if it is not None.
        """
        for x in self.getAliens():
            for y in x:
                if y != None:
                    y.draw(view)
        if self._ship != None:
            self._ship.draw(view)
        self._dline.draw(view)
        for bolt in self._bolts:
            if bolt != None:
                bolt.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def alienrows(self):
        """
        Creates the wave of aliens by appending aliens objects to the 2d list _aliens.
        Creates ALIEN_ROWS rows of aliens and ALIENS_IN_ROW columns of aliens. The aliens
        are created in bottom-up and left-right order.

        Each alien is created using the attributes x, y, width, height, and source to specify
        how it looks on screen.

        The first alien (bottom-left) is created at ALIEN_H_SEP pixels from the left edge
        of the screen and GAME_HEIGHT - ALIEN_CEILING - .5*ALIEN_HEIGHT - (ALIEN_ROWS-1)*
        (ALIEN_HEIGHT+ALIEN_V_SEP) pixels from the top of the screen. All subsequent adjacent
        aliens are created ALIEN_H_SEP pixels away from each other horizontally, and ALIEN_V_SEP
        pixels away from each other vertically.
        """
        xcoord = ALIEN_H_SEP + .5*ALIEN_WIDTH
        a = GAME_HEIGHT - ALIEN_CEILING - .5*ALIEN_HEIGHT
        b = (ALIEN_ROWS-1)*(ALIEN_HEIGHT+ALIEN_V_SEP)
        ycoord = a - b
        all = []
        for x in range(ALIENS_IN_ROW):
            col = []
            for y in range(ALIEN_ROWS):
                num_images = y // 2
                which_image = num_images % 3
                alien = Alien(xcoord, ycoord, ALIEN_WIDTH, ALIEN_HEIGHT, ALIEN_IMAGES[which_image])
                col.append(alien)
                ycoord = ycoord + ALIEN_HEIGHT + ALIEN_V_SEP
            ycoord = a - b
            xcoord = xcoord + ALIEN_H_SEP + ALIEN_WIDTH
            all.append(col)
        return all

    def rightmostalien(self):
        """
        Returns the alien object that is the rightmost alien in the wave of aliens.
        """
        rightmost_x = 0
        rightmost_col = ALIENS_IN_ROW
        alien = self._aliens[-1][-1]
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if self._aliens[x][y] != None and self._aliens[x][y].x > rightmost_x:
                    rightmost_x = self._aliens[x][y].x
                    rightmost_col = self._aliens[x]
        for i in rightmost_col:
            if i != None:
                alien = i
        return alien

    def leftmostalien(self):
        """
        Returns the alien object that is the leftmost alien in the wave of aliens.
        """
        leftmost_x = GAME_WIDTH
        leftmost_col = 0
        alien = self._aliens[0][-1]
        for x in range(len(self._aliens)):
            for y in range(len(self._aliens[x])):
                if self._aliens[x][y] != None and self._aliens[x][y].x < leftmost_x:
                    leftmost_x = self._aliens[x][y].x
                    leftmost_col = self._aliens[x]
        for i in leftmost_col:
            if i != None:
                alien = i
        return alien

    def player(self):
        """
        Creates the ship object SHIP_BOTTOM pixels from the bottom of the screen
        and x-position of halfway along the screen
        """
        xcoord = GAME_WIDTH / 2
        ycoord = SHIP_BOTTOM + .5*SHIP_HEIGHT
        player = Ship(xcoord,ycoord,SHIP_WIDTH,SHIP_HEIGHT,'ship.png')
        return player

    def aliensmoveright(self, time):
        """
        Moves all aliens to the right every interval of time

        Parameter time: The time in seconds since last update
        Precondition: time is a number (int or float)
        """
        self._time += time
        if self._time > self._alienspeed:
            for x in self._aliens:
                for y in x:
                    if y != None:
                        y.x += ALIEN_H_WALK
                        self._time = 0
            self._steps += 1

    def aliensmoveleft(self, time):
        """
        Moves all aliens to the left every interval of time

        Parameter time: The time in seconds since last update
        Precondition: time is a number (int or float)
        """
        self._time += time
        if self._time > self._alienspeed:
            for x in self._aliens:
                for y in x:
                    if y != None:
                        y.x -= ALIEN_H_WALK
                        self._time = 0
            self._steps += 1

    def aliensmovedown(self):
        """
        Moves all aliens down ALIEN_V_WALK pixels
        """
        for x in self._aliens:
            for y in x:
                if y != None:
                    y.y -= ALIEN_V_WALK
        self._steps += 1

    def playerbolts(self):
        """
        Returns, creates, and identifies the bolts shot by the ship. The bolts are fired from
        the ship's x-coordinate and the top most edge of the ship's height.
        """
        count = 0
        for x in self._bolts:
            if x.isplayerbolt():
                count += 1
        if count == 0:
            self._firesound.play()
            xcoord = self._ship.x
            ycoord = self._ship.y + .5*SHIP_HEIGHT
            bolt = Bolt(xcoord, ycoord, BOLT_WIDTH, BOLT_HEIGHT, 'red', BOLT_SPEED)
            self._bolts.append(bolt)
            return self._bolts

    def alienbolts(self,a,b):
        """
        Returns, creates, and identifies the bolts shot by the aliens. The bolts are fired from
        the alien's x-coordinate and y-coordinate.

        Parameter a: the column of the aliens
        Precondition: a is a random int in range 0..ALIENS_IN_ROW

        Parameter b: the row of the aliens
        Precondition: b is a random int in range 0..ALIEN_ROWS
        """
        count = 0
        for x in self._bolts:
            if not x.isplayerbolt():
                count += 1
        if count == 0 and self._steps == self._rate:
            alien = self._aliens[a][b]
            if alien != None:
                xcoord = alien.x
                ycoord = alien.y
                bolt = Bolt(xcoord, ycoord, BOLT_WIDTH, BOLT_HEIGHT, 'green', -BOLT_SPEED)
                self._bolts.append(bolt)
        self._steps = 0
        self._rate = random.randint(1,BOLT_RATE)
        return self._bolts

    def del_player_bolt(self):
        """
        Removes a player bolt object from the list self._bolts
        """
        for x in range(len(self._bolts)):
            if len(self._bolts) > x:
                if self._bolts[x].y >= GAME_HEIGHT and len(self._bolts) != 0:
                    del self._bolts[x]

    def del_alien_bolt(self):
        """
        Removes an alien bolt object from the list self._bolts
        """
        for x in range(len(self._bolts)):
            if len(self._bolts) > x:
                if self._bolts[x].y <= 0 and len(self._bolts) != 0:
                    del self._bolts[x]

    def aliencollide(self):
        """Iterates through the 2d list of alien objects and the list of bolt objects,
        checks if a player bolt is contained by an alien image. If so, the alien
        object is set equal to None, and the bolt object is removed from the list
        self._bolts."""

        collided = []
        ylist = []
        zlist = []
        for x in range(len(self._bolts)):
            bolt = self._bolts[x]
            if bolt.isplayerbolt():
                x1 = bolt.x - .5*BOLT_WIDTH    # top left
                y1 = bolt.y + .5*BOLT_HEIGHT
                x2 = bolt.x + .5*BOLT_WIDTH    # top right
                y2 = y1
                x3 = x1                     # bottom left
                y3 = bolt.y - .5*BOLT_HEIGHT
                x4 = x2                     # bottom right
                y4 = y3
                for y in range(len(self._aliens)):
                    for z in range(len(self._aliens[y])):
                        alien = self._aliens[y][z]
                        if alien != None and len(self._bolts) > x:
                            a = alien.contains((x1,y1))
                            b = alien.contains((x2,y2))
                            c = alien.contains((x3,y3))
                            d = alien.contains((x4,y4))
                            if a or b or c or d:
                                collided.append(x)
                                ylist.append(y)
                                zlist.append(z)
        collided.reverse()
        for i in collided:
            self._bolts.remove(self._bolts[i])
        for k in range(len(ylist)):
            self._aliens[ylist[k]][zlist[k]] = None
            self._deathsound.play()

    def shipcollide(self):
        """Iterates through the 2d list of alien objects and the list of bolt objects,
        checks if an alien bolt is contained by the ship image. If so, the ship
        object is set equal to None, and the bolt object is removed from the list
        self._bolts."""
        collided = []
        for x in range(len(self._bolts)):
            bolt = self._bolts[x]
            if not bolt.isplayerbolt():
                x1 = bolt.x - .5*BOLT_WIDTH    # top left
                y1 = bolt.y + .5*BOLT_HEIGHT
                x2 = bolt.x + .5*BOLT_WIDTH    # top right
                y2 = y1
                x3 = x1                     # bottom left
                y3 = bolt.y - .5*BOLT_HEIGHT
                x4 = x2                     # bottom right
                y4 = y3
                ship = self._ship
                if ship != None and len(self._bolts) > x:
                    a = ship.contains((x1,y1))
                    b = ship.contains((x2,y2))
                    c = ship.contains((x3,y3))
                    d = ship.contains((x4,y4))
                    if a or b or c or d:
                        collided.append(x)
        collided.reverse()
        for i in collided:
            self._bolts.remove(self._bolts[i])
            if self._ship != None:
                self._ship = None
                self._deathsound.play()
                self._lives -= 1

    def breach(self):
        """
        Sets the player lives to 0 when the bottom-most alien touches the defence line
        """
        for x in self._aliens:
            for y in x:
                if y != None and y.y <= DEFENSE_LINE:
                    self._lives = 0

    def victory(self):
        """
        Keeps track of the aliens that are destroyed. If all the aliens are destroyed,
        then the player wins the game and self._win is set to True.
        """
        total = ALIEN_ROWS * ALIENS_IN_ROW
        count = 0
        for x in self._aliens:
            for y in x:
                if y == None:
                    count += 1
        if count == total:
            self._win = True
