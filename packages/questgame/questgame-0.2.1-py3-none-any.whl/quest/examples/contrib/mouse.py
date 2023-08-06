from quest.examples.island import IslandAdventure
from quest.contrib.mouse import MouseMotionMixin

class IslandWithMouse(MouseMotionMixin, IslandAdventure):
    "The island adventure with mouse control."

if __name__ == '__main__':
    game = IslandWithMouse()
    game.run()
