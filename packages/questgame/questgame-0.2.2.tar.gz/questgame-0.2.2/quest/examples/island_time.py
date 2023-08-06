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
from math import cos, pi, floor
from quest.helpers import shade

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
        white = (255,255,255)
        shade_ratio = self.game.max_shade * (cos(self.time_of_day() * 2 * pi) + 1) / 2
        brightness = shade(white, ratio=shade_ratio)
        for sprite in self.all_sprites:
            sprite.color = brightness

    def time_of_day(self):
        "Returns the time of day as a ratio from 0 to 1."
        return (self.time_since_start() % self.game.day_length) / self.game.day_length

    def clock_time(self):
        "Returns an hour:minute string"
        tod = self.time_of_day()
        hour = floor(tod * 24)
        hour_fraction = (tod - hour/24) * 24
        minute = floor(hour_fraction * 60)
        ampm = "am" if hour < 12 else "pm"
        ampm_hour = hour % 12 if (hour % 12) > 0 else 12
        return f"{ampm_hour}:{minute:02d} {ampm}"

    def time_of_day_string(self):
        "Returns the time of day as a string"
        hour = self.time_of_day() * 24
        if hour < 5:
            return "night"
        elif hour < 7:
            return "twilight"
        elif hour < 9:
            return "dawn"
        elif hour < 12:
            return "morning"
        elif hour < 17:
            return "afternoon"
        elif hour < 20:
            return "evening"
        elif hour < 22:
            return "dusk"
        else:
            return "night"


class IslandTime(IslandAdventure):
    """ A game that implements a day/night cycle by tracking the time since the game started
    and shading the sprites based on a day/night cycle
    """

    max_shade = 0.6
    day_length = 20
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
            tods = self.physics_engine.time_of_day_string().capitalize()
            clock_time = self.physics_engine.clock_time()
            return f"{tods} ({clock_time})"

if __name__ == '__main__':
    game = IslandTime()
    game.run()
