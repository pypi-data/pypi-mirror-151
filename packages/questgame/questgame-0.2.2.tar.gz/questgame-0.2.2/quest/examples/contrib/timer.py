# timer.py example game
# by Xuxi917 and Jacob Wolf
#
# Example game to demoinstrate mixing in a timer to a game

from quest.contrib.timer import TimerMixin
from quest.examples.maze import MazeGame
from quest.engines import ContinuousPhysicsEngine

TIME_LIMIT = 30

class TimedContPhysicsEngine(TimerMixin, ContinuousPhysicsEngine):
    """ Physics engine that also makes time-based updates
    """

    def __init__(self, game):
        """ Starts timer.
        """
        self.init_timer(TIME_LIMIT)
        super().__init__(game)

class TimedMazeGame(MazeGame):
    """ Generates a game with MazeGame with a time limit using the TimerMixin.
    """

    def setup_physics_engine(self):
        """ Sets up a physics engine with a timer using the TimerMixin
        """
        self.physics_engine = TimedContPhysicsEngine(self)

    def message(self):
        """Returns a string representation of the time remaining in the game.
        """
        if self.physics_engine.time_remaining() <= 0:
            return "You got {} stars!".format(self.score)
        else:
            return "Time remaining: {}".format(int(self.physics_engine.time_remaining()))

if __name__ == '__main__':
    game = TimedMazeGame()
    game.run()


