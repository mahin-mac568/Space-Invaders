"""
Primary module for Space Invaders

This module contains the main controller class for the Space Invaders application.

# Mahin Chowdhury 
# NetID: mac568
# Completed on: 12/4/18
"""
from consts import *
from game2d import *
from wave import *


class Invaders(GameApp):
    """
    The primary controller class for the Space Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, I do NOT create an
    initializer __init__ for this class. Any initialization is done in the 
    start method instead. This is only for this class.  All other classes
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

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    _rounds: the number of waves of aliens in one game[int]

    """

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__. This 
        method is called once the game is running. 

        This method makes sure that all of the attributes satisfy the given invariants. 
        When done, it sets the _state to STATE_INACTIVE and create a message (in 
        attribute _text) saying that the user should press to play a game.
        """
        self._state = 0
        self._wave = None
        if self._state == STATE_INACTIVE:
            self._text = self._starttext()
        self._rounds = 3
        if self._state >= 2:
            self._text = None

    def update(self, dt):
        """
        Animates each single frame in the game.

        This is the method that does most of the work. It is NOT in charge of playing 
        the game. That is the job of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        STATE_INACTIVE: This is the state when the application first opens. It is a
        paused state, waiting for the player to start the game. It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key. In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay. The player can move the
        ship and fire laser bolts. All of this is handled inside of class Wave (NOT 
        in this class). Hence the Wave class has an update() method.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is won.

        STATE_LOSE: The player lost all lives and the game is lost.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self._rounds = 3
            self.ispdown()
            self.triggermute()
        if self._state == STATE_NEWWAVE:
            self.new_helper()
        if self._state == STATE_ACTIVE:
            self.active_helper(dt)
        if self._state == STATE_PAUSED:
            self.triggermute()
            self.iscdown()
        if self._state == STATE_CONTINUE:
            self.triggermute()
            self._wave.update(dt)
            self._state = STATE_ACTIVE
        if self._state == STATE_COMPLETE:
            self.complete_helper()
        if self._state == STATE_LOSE:
            self.triggermute()
            self.pressplayagain()

    def new_helper(self):
        """
        STATE_NEWWAVE: This is the state that creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.
        """
        self.triggermute()
        if self._rounds == 3:
            self._wave = Wave(ALIEN_SPEED)
        if self._rounds == 2:
            self._wave = Wave(.2*ALIEN_SPEED)
        if self._rounds == 1:
            self._wave = Wave(.05*ALIEN_SPEED)
        self._state = STATE_ACTIVE

    def active_helper(self, dt):
        """
        STATE_ACTIVE: This is a session of normal gameplay. The player can move the
        ship and fire laser bolts. All of this is handled inside of class Wave (NOT 
        in this class). Hence the Wave class has an update() method.
        """
        self._wave.update(dt)
        self.triggermute()
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
        STATE_COMPLETE: The three waves are over, and the game is either won or lost. 
        If three waves of aliens have not been cleared, create a new wave of aliens.
        """
        if self._rounds > 0:
            self._rounds -= 1
        if self._rounds != 0:
            self._state = STATE_NEWWAVE
        self.triggermute()
        self.pressplayagain()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing I want to draw in this game is a GObject. To draw a 
        GObject g, I simply use the method g.draw(self.view).

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, I either need to add getters for these attributes
        or I need to add a draw method to class Wave. 
        """
        if self._state == STATE_INACTIVE:
            self._text.draw(self.view)
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

    def _starttext(self):
        """
        Creates the text specifying how to start the game.
        """
        xcoord = 0.825 * GAME_WIDTH/2
        ycoord = 1.1 * GAME_HEIGHT/2
        s = GLabel(text="\n \
                           SPACE INVADERS \n \
                           \n \
                           There are aliens arranged in rows and columns. At the bottom \n \
                           of the screen is the player's ship. There is also a horizontal \n \
                           line at the bottom of the screen. This is the defense line. If \n \
                           the aliens make it past this line, they have successfully \n \
                           invaded and you have lost the game. \n \
                           \n \
                           There are three levels. That means you must defeat three waves \n \
                           of aliens in order to clear the game. Bear in mind, you only \n \
                           have three lives per wave of aliens... And the enemies get \n \
                           progressively faster after each level. Tread carefully. \n \
                           \n \
                           While the game is being played, you can press 'M' to mute \n \
                           or unmute the game. \n \
                           \n \
                           Press 'P' to Play",
                   font_size=20,
                   bold=True,
                   x=xcoord,
                   y=ycoord)
        return s

    def ispdown(self):
        """
        Creates the button to press to start the game. 
        Changes the state of the game to active.
        """
        currentkey = self.input.key_count
        pkey = self.input.is_key_down('p')
        if currentkey > 0 and currentkey < 2 and pkey is True:
            self._state = (self._state + 1) % 6
            return True

    def iscdown(self):
        """
        Creates the button to press to exit the pause screen. 
        Changes the state of the game to active.
        """
        currentkey = self.input.key_count
        ckey = self.input.is_key_down('c')
        if currentkey > 0 and currentkey < 2 and ckey is True:
            self._state = STATE_CONTINUE
            self._wave.setShip(self.respawn())

    def pressplayagain(self):
        """
        Creates the botton to press to return to the start menu and play again
        """
        currentkey = self.input.key_count
        pkey = self.input.is_key_down('p')
        if currentkey > 0 and currentkey < 2 and pkey is True:
            self._state = STATE_INACTIVE

    def triggermute(self):
        """
        Creates the button to press to mute the volume
        """
        currentkey = self.input.key_count
        mkey = self.input.is_key_down('m')
        if currentkey > 0 and currentkey < 2 and mkey is True:
            if self._wave.getfiresound().volume == 0 and self._wave.getdeathsound().volume == 0:
                self._wave.getfiresound().volume = 1
                self._wave.getdeathsound().volume = 1
            else:
                self._wave.getfiresound().volume = 0
                self._wave.getdeathsound().volume = 0

    def respawn(self):
        """
        Creates a ship object SHIP_BOTTOM pixels from the bottom of the screen
        and x-position of halfway along the screen
        """
        xcoord = GAME_WIDTH / 2
        ycoord = SHIP_BOTTOM + .5*SHIP_HEIGHT
        player = Ship(xcoord, ycoord, SHIP_WIDTH, SHIP_HEIGHT, 'ship.png')
        return player

    def pausegame(self):
        """
        Creates the text specifying how to exit the pause menu.
        """
        xcoord = GAME_WIDTH/2
        ycoord = GAME_HEIGHT/2
        c = GLabel(text="Press 'C' to Continue", font_size=20, bold=True,
                   x=xcoord, y=ycoord)
        return c

    def wingame(self):
        """
        Creates the text telling the user that he/she has won the game.
        """
        xcoord = GAME_WIDTH/2
        ycoord = GAME_HEIGHT/2
        w = GLabel(text="You WIN!", font_size=20, bold=True,
                   x=xcoord, y=ycoord)
        return w

    def losegame(self):
        """
        Creates the text telling the user that he/she has won the game.
        """
        xcoord = GAME_WIDTH/2
        ycoord = GAME_HEIGHT/2
        l = GLabel(text="You LOSE!", font_size=20, bold=True,
                   x=xcoord, y=ycoord)
        return l

    def playagain(self):
        """
        Creates the text specifying how to return to the start menu to play again.
        """
        xcoord = GAME_WIDTH/2
        ycoord = DEFENSE_LINE + 100
        h = GLabel(text="Press 'P' to Play Again", font_size=20, bold=True,
                   x=xcoord, y=ycoord)
        return h
