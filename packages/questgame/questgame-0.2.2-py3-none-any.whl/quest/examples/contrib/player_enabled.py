from quest.examples.island import IslandAdventure
from quest.contrib.player_enabled import PlayerEnabledMixin
from datetime import datetime

class SleepyIslandAdventure(PlayerEnabledMixin, IslandAdventure):
    """The Island Adventure, but in this version the player occasionally needs to sleep.
    """

    def on_update(self, delta_time):
        if self.is_sleeping():
            self.player_enabled = False
            self.message_str = "Sleeping..."
        else:
            self.player_enabled = True
            self.message_str = ""
        super().on_update(delta_time)


    def is_sleeping(self):
        """Determines whether the player is sleeping. Alternates every three seconds.
        """
        return datetime.now().second % 6 < 3

    def message(self):
        return self.message_str
    
if __name__ == '__main__':
    game = SleepyIslandAdventure()
    game.run()
