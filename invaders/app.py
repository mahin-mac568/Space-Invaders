"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

# Mahin Chowdhury mac568
  William Lee wl433
# 12/4/18
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
                STATE_CONTINUE, STATE_COMPLETE, STATE_LOSE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    _rounds: the number of waves of aliens in one game[int]

    """
    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state = 0
        self._wave = None
        self._text = self._starttext()
        self._rounds = 3
        if self._state >= 1:
            self._text = None

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is won.

        STATE_LOSE: The player lost all lives and the game is lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        # Determine what the current state is
        #Process the states. Send to helper methods
        if self._state == STATE_INACTIVE:
            self._rounds = 3
            self.issdown()
            self.isvdown()
            self.isbdown()
        if self._state == STATE_NEWWAVE:
            self.new_helper()
        if self._state == STATE_ACTIVE:
            self.active_helper(dt)
        if self._state == STATE_PAUSED:
            self.isvdown()
            self.iscdown()
            self.isbdown()
        if self._state == STATE_CONTINUE:
            self.isvdown()
            self.isbdown()
            self._wave.update(dt)
            self._state = STATE_ACTIVE
        if self._state == STATE_COMPLETE:
            self.complete_helper()
        if self._state == STATE_LOSE:
            self.isvdown()
            self.isbdown()
            self.ishdown()

    def new_helper(self):
        """
        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.
        """
        #self._wave = Wave(ALIEN_SPEED)
        self.isvdown()
        self.isbdown()
        if self._rounds == 3:
            self._wave = Wave(ALIEN_SPEED)
        if self._rounds == 2:
            self._wave = Wave(.6*ALIEN_SPEED)
        if self._rounds == 1:
            self._wave = Wave(.4*ALIEN_SPEED)
        self._state = STATE_ACTIVE

    def active_helper(self, dt):
        """
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.
        """
        self._wave.update(dt)
        self.isvdown()
        self.isbdown()
        if self._wave.getShip() != None:
            if self.input.is_key_down('left') and self._wave.getShip().x >= .5*SHIP_WIDTH:
                self._wave.getShip().x -= SHIP_MOVEMENT
            if self.input.is_key_down('right') and self._wave.getShip().x <= GAME_WIDTH - .5*SHIP_WIDTH:
                self._wave.getShip().x += SHIP_MOVEMENT
            if self.input.is_key_down('spacebar'):
                self._wave.playerbolts()
        else:
            self._state = STATE_PAUSED
        if self._wave.getLives() == 0:
            self._state = STATE_LOSE
        if self._wave.getWin():
            self._state = STATE_COMPLETE
        if self._rounds == 0:
            self._state = STATE_COMPLETE

    def complete_helper(self):
        """
        STATE_COMPLETE: The waves are over, and the game is either won or lost. If three waves
        of aliens have not been cleared, create a new wave of aliens.
        """
        if self._rounds > 0:
            self._rounds -= 1
        if self._rounds != 0:
            self._state = STATE_NEWWAVE
        self.isvdown()
        self.isbdown()
        self.ishdown()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        if self._state == STATE_INACTIVE:
            self._text.draw(self.view)
            self.soundOff().draw(self.view)
            self.soundOn().draw(self.view)
        if self._state >= 1 and self._wave != None:
            self._wave.draw(self.view)
        if self._state == STATE_PAUSED:
            self.pausegame().draw(self.view)
        if self._state == STATE_CONTINUE:
            self.respawn().draw(self.view)
        if self._state == STATE_COMPLETE:
            if self._rounds == 0:
                self.wingame().draw(self.view)
                self.playagain().draw(self.view)
        if self._state == STATE_LOSE:
            if self._wave != None and self._wave.getLives() == 0:
                self.losegame().draw(self.view)
                self.playagain().draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def _starttext(self):
        """
        Creates the text specifying how to start the game. Should be positioned
        in the center of the screen.
        """
        xcoord = GAME_WIDTH/2
        ycoord = GAME_HEIGHT/2
        s = GLabel(text = "Press 'S' to Play", font_size = 20, bold = True,
                    x = xcoord, y = ycoord)
        return s

    def issdown(self):
        """
        Creates the button to press to start the game. Changes the state of the game to active.
        """
        currentkey = self.input.key_count
        skey = self.input.is_key_down('s')
        if currentkey > 0 and currentkey < 2 and skey is True:
            self._state = (self._state + 1) % 5
            return True

    def iscdown(self):
        """
        Creates the button to press to exit the pause screen. Chang
        es the state of the game to active
        """
        currentkey = self.input.key_count
        ckey = self.input.is_key_down('c')
        if currentkey > 0 and currentkey < 2 and ckey is True:
            self._state = STATE_CONTINUE
            self._wave.setShip(self.respawn())

    def ishdown(self):
        """
        Creates the botton to press to return to the start menu and play again
        """
        currentkey = self.input.key_count
        hkey = self.input.is_key_down('h')
        if currentkey > 0 and currentkey < 2 and hkey is True:
            self._state = STATE_INACTIVE

    def isvdown(self):
        """
        Creates the button to press to mute the volume
        """
        currentkey = self.input.key_count
        vkey = self.input.is_key_down('v')
        if currentkey > 0 and currentkey < 2 and vkey is True:
            self._wave.getfiresound().volume = 0
            self._wave.getdeathsound().volume = 0

    def isbdown(self):
        """
        Creates the button to press to unmute the volume
        """
        currentkey = self.input.key_count
        bkey = self.input.is_key_down('b')
        if currentkey > 0 and currentkey < 2 and bkey is True:
            self._wave.getfiresound().volume = 1
            self._wave.getdeathsound().volume = 1

    def soundOff(self):
        """
        Creates the text specifiying how to mute the volume. Should be positioned below
        the start text on the start menu
        """
        xcoord = GAME_WIDTH/2
        ycoord = DEFENSE_LINE + 100
        v = GLabel(text = "Press V to Turn Sound Off", font_size = 20, bold = True,
                    x = xcoord, y = ycoord)
        return v

    def soundOn(self):
        """
        Creates the text specifying how to unmute the volume. Should be positioned below
        the 'how to mute' text on the start menu
        """
        xcoord = GAME_WIDTH/2
        ycoord = DEFENSE_LINE + 50
        v = GLabel(text = "Press B to Turn Sound On", font_size = 20, bold = True,
                    x = xcoord, y = ycoord)
        return v

    def respawn(self):
        """
        Creates a ship object SHIP_BOTTOM pixels from the bottom of the screen
        and x-position of halfway along the screen
        """
        xcoord = GAME_WIDTH / 2
        ycoord = SHIP_BOTTOM + .5*SHIP_HEIGHT
        player = Ship(xcoord,ycoord,SHIP_WIDTH,SHIP_HEIGHT,'ship.png')
        return player


    def pausegame(self):
        """
        Creates the text specifying how to exit the pause menu. Should be positioned at
        the center of the screen.
        """
        xcoord = GAME_WIDTH/2
        ycoord = GAME_HEIGHT/2
        c = GLabel(text = "Press 'C' to Continue", font_size = 20, bold = True,
                    x = xcoord, y = ycoord)
        return c


    def wingame(self):
        """
        Creates the text telling the user that he/she has won the game. Should be positioned
        at the center of the screen.
        """
        xcoord = GAME_WIDTH/2
        ycoord = GAME_HEIGHT/2
        w = GLabel(text = "You WIN!", font_size = 20, bold = True,
                    x = xcoord, y = ycoord)
        return w


    def losegame(self):
        """
        Creates the text telling the user that he/she has won the game. Should be positioned
        at the center of the screen.
        """
        xcoord = GAME_WIDTH/2
        ycoord = GAME_HEIGHT/2
        l = GLabel(text = "You LOSE!", font_size = 20, bold = True,
                    x = xcoord, y = ycoord)
        return l


    def playagain(self):
        """
        Creates the text specifying how to return to the start menu to play again.
        """
        xcoord = GAME_WIDTH/2
        ycoord = DEFENSE_LINE + 100
        h = GLabel(text = "Press 'H' to Play Again", font_size = 20, bold = True,
                    x = xcoord, y = ycoord)
        return h
