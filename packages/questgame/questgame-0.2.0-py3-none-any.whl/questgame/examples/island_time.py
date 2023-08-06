# island_time.py
#
# game that extends the basic island game to implement a clock that changes the
# appearance of the sprites based on the time of the game

from quest.examples.island import IslandAdventure
from quest.engines import ContinuousPhysicsEngine
from quest.contrib.timer import TimerMixin
import arcade
import os
from pathlib import Path

class TimedContinuousPhysicsEngine(ContinuousPhysicsEngine, TimerMixin):
    """ Physics engine that also makes time-based updates
    """

    def __init__(self, game):
        self.init_timer()
        super().__init__(game)

    def update(self):
        """Calculates shade by converting the time passed since the start of the game to a percentage
        of the current day/night cycle.
        """
        super().update()
        time_since_start = self.time_since_start() 
        curr_mod = time_since_start%self.game.time_cycle_secs
        grade = abs(curr_mod - self.game.time_cycle_secs/2) / (self.game.time_cycle_secs/2)
        color_value = grade*(255-self.game.max_darkness) + self.game.max_darkness
        for sprite in self.all_sprites:
            sprite.color = (color_value, color_value, color_value)


class IslandTime(IslandAdventure):
    """ A game that implements a day/night cycle by tracking the time since the game started
    and shading the sprites based on a day/night cycle
    """

    max_darkness = 100
    time_cycle_secs = 30
    display_time = True
    
    def __init__(self):
        super().__init__()
        

    def setup_physics_engine(self):
        """Passes optional `time` parameter to the standard :py:class:`ContinuousPhysicsEngine`.
        The result is that the sprites in the game change their appearance as time progresses in
        the game.
        """
        self.physics_engine = TimedContinuousPhysicsEngine(self)

    def message(self):
        """ Displays the time in the game relative to the time cycle
        """
        if self.display_time:
            return "Time: {}".format(int(self.physics_engine.time_since_start()%self.time_cycle_secs))

if __name__ == '__main__':
    game = IslandTime()
    game.run()
