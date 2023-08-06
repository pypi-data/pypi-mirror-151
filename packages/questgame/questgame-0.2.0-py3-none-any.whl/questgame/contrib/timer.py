# timer.py
# by Xuxi9197
#
# Mixin to the physics engine to add a timer to the game.
# Update physics engine to call time_updates() in the update() function.

from time import time

class TimerMixin:
    """ Maintains a clock for the game that can enforce time-based game states
    and elements like a countdown.

    You can mix this class into a physics engine like this:
        class TimedPhysicsEngine(PhysicsEngine, TimerMixin):
        ...
        ...
    """
    def init_timer(self, total_game_time=None):
        """ Records the start time of the game

        Arguments:
            display (Boolean): whether to display the timer or not
            total_game_time (int): how much time a game should last
        """
        self.start_time = time()
        self.total_game_time = total_game_time

    def update(self):
        """ Updates the game based on the timer and stops the game from running if the total
        time of the game has elapsed.
        """
        
        if self.total_game_time:
            if self.time_since_start() >= self.total_game_time:
                self.game.running = False
        super().update()

    def time_since_start(self):
        """ Returns time since the start of the game.
        """
        return time() - self.start_time

    def time_remaining(self):
        """ Returns the time remaining or None if no total_game_time was set.
        """
        if self.total_game_time:
            return self.total_game_time - self.time_since_start()
        return None

