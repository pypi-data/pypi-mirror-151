# Maze Walk Strategy

from quest.contrib.target_strategy import TargetStrategy
from quest.maze import Maze
from quest.map import GridMapLayer
from quest.helpers import Direction

class MazeWalkStrategy(TargetStrategy):
    """A strategy to randomly explore a maze.

    This Strategy relies on the insight that if you are stuck in a maze, if you keep your left 
    hand on the wall at all times and keep walking, you will eventually explore the whole maze.
    (There's nothing special about left; you could choose your right hand instead.) This assumes 
    a special definition of a maze, that there should be exactly one path between any two points. 
    No loops allowed. If you are not convinced, draw a few mazes and test it out. 

    To implement this insight, we can start with `quest.contrib.target_strategy.TargetStrategy`, which 
    knows how to direct a sprite toward a target until it gets there, and then to choose a new target.
    We just need to choose new targets in a way that gets the sprite around the maze.

    To choose a target, the sprite needs to have a `heading`, which keeps track of the direction
    it is currently facing. Then, if it's possible to turn left, always do that. Otherwise go straight. 
    If straight is not possible, then turn right. And if turning right is not possible either, then turn
    around and go back. (Update the heading with this new direction.)

    We need a SpriteList of walls so we can check if it's possible to go in a particular direction. 
    It's also helpful to have a grid--instead of using whatever random position the sprite is currently in,
    we can just think in grid squares. This simplifies the math a lot. 

    Arguments:
        grid (quest.map.GridMapLayer): The GridMapLayer used to build the maze.
        walls (arcade.SpriteList): A SpriteList containing all the walls.
    """

    def __init__(self, grid, walls):
        self.grid = grid
        self.wall_positions = [grid.get_grid_position((wall.center_x, wall.center_y)) for wall in walls]

    def choose_new_target(self, sprite, game):
        """Starting with left of the current heading (anticlockwise), keep turning 
        clockwise until a direction is not blocked. Set the sprite's heading to this 
        new direction and return the direction as a vector.

        Arguments:
            sprite: The sprite who is about to act.
            game: The game object (not used in this Strategy).
        """
        new_heading = sprite.heading.turn_anticlockwise()
        while self.direction_is_blocked(sprite, new_heading):
            new_heading = new_heading.turn_clockwise()
        sprite.heading = new_heading
        grid_target = self.get_new_grid_position(sprite, new_heading)
        sprite.target = self.grid.get_pixel_position(grid_target)
        
    def setup_sprite(self, sprite, game):
        """This strategy requires the sprite to remember the direction it is moving (its heading).
        If a sprite has no heading, we'll randomly assign one to get started.

        Arguments:
            sprite: The sprite who is about to act.
        """
        super().setup_sprite(sprite, game)
        if not hasattr(sprite, "heading"):
            sprite.heading = Direction.N

    def direction_is_blocked(self, sprite, direction):
        """Checks whether the direction (from the sprite's current position) is blocked by a wall.

        Arguments:
            sprite: The sprite who is about to act.
            direction (quest.helpers.Direction): The direction to check.
        """
        return self.get_new_grid_position(sprite, direction) in self.wall_positions

    def get_new_grid_position(self, sprite, direction):
        """First, we get the sprite's current position in grid coordinates (something like (3, 6), much
        nicer than pixel coordinates like (365.76, 190,88)). Then we calculate the new position by adding
        the direction's vector coordinates. (For example, Direction.N as a vector is (0, 1).)
        """

        current_x, current_y = self.grid.get_grid_position((sprite.center_x, sprite.center_y))
        direction_x, direction_y = direction.to_vector()
        return (current_x + direction_x, current_y + direction_y)
