from quest.game import QuestGame
from quest.map import Map, GridMapLayer
from quest.maze import Maze
from quest.sprite import Wall, NPC
from quest.helpers import resolve_resource_path
from itertools import product
import arcade
import random
from datetime import datetime
import os
from pathlib import Path

class MazeGame(QuestGame):
    """Get all the stars as fast as you can! My record is 45 seconds.

    :py:class:`MazeGame` is an example of how you can make a fairly complex 
    game without making too many changes. Because :py:class:`MazeGame` is a 
    subclass of :py:class:`QuestGame`, we just need to change the parts we 
    want to work differently. We need to set some of the :py:class:`MazeGame` 
    properties and override a few of the class methods. 

    To run this example::

        $ python -m quest.examples.maze

    After you play it, check out the sorce code by clicking on "source" in the
    blue bar just above.


    Attributes:
        tile_size=32: Each square tile in the map is 32 pixels across.
        grid_columns=33: The map will have 33 columns of tiles.
        grid_rows=33: The map will have 33 rows of tiles.
        player_sprite_image="images/boy_simple.png": The sprite's image file.
        player_scaling=0.5: The image is too big, so we scale it down. (We could
            also just resize the image itself.)
        player_initial_x=1.5 * tile_size: By starting the player at 1.5 times `tile_size`, 
            the player will initially be positioned at the center of tile (1, 1).
            The outer edge of the map is walls.
        player_initial_y=1.5 * tile_size: Again, centering the player at (1, 1)
        score=0: Keeps track of how much loot has been collected.
        max_score=25: Total amount of loot to be distributed through the maze.
        game_over=False: Keeps track of whether the game has ended.
    """
    tile_size = 32
    grid_columns = 33
    grid_rows = 33
    player_sprite_image = resolve_resource_path("images/boy_simple.png")
    player_scaling = 0.5
    player_speed = 5
    player_initial_x = 1.5 * tile_size
    player_initial_y = 1.5 * tile_size
    score = 0
    max_score = 25
    game_over = False

    def __init__(self):
        super().__init__()
        self.level_start = datetime.now()

    def setup_maps(self):
        """Creates a :py:class:`MazeMap` (see below) and adds it to game's list of maps.
        """
        super().setup_maps()
        maze_map = MazeMap(self.grid_columns, self.grid_rows, self.tile_size, self.max_score)
        self.add_map(maze_map)

    def setup_walls(self):
        """Assigns `self.wall_list` to be all the sprites in the map's "walls" layer.
        """
        self.wall_list = self.get_current_map().get_layer_by_name("walls").sprite_list

    def setup_npcs(self):
        """Assigns `self.npc_list` to be all the sprites in the map's "loot" layer.
        """
        self.npc_list = self.get_current_map().get_layer_by_name("loot").sprite_list

    def on_loot_collected(self, collector):
        """A method to be called whenever loot is collected.

        See the :py:class:`Loot` NPC sprite below. It calls this method whenever there is
        a collision with the player.
        """
        self.score += 1
        if self.score == self.max_score:
            self.game_over = True
            self.final_elapsed_time = (datetime.now() - self.level_start).seconds

    def message(self):
        """Returns a string like "Time 12 (12/25)"
        """
        if self.game_over:
            return "You won in {} seconds!".format(self.final_elapsed_time)
        else:
            elapsed_time = datetime.now() - self.level_start
            return "Time {} ({}/{})".format(elapsed_time.seconds, self.score, self.max_score)

class Loot(NPC):
    """Loot is a NPC which shows up in the game as a star. Its only job is to
    get collected by the player.
    """
    def on_collision(self, sprite, game):
        """When the player collides with a Loot, it calls :py:meth:`quest.maze.MazeMap.on_loot_collected` to tell
        the game to make needed updates. Then the Loot kills itself.
        """
        game.on_loot_collected(sprite)
        print("Got a star!")
        self.kill()

class MazeMap(Map):
    """A Map which creates a wall layer using a :py:class:`Maze`.

    :py:class:`MazeMap` is a subclass of :py:class:`Map` which automatically generates a 
    maze. It uses a :py:class:`Maze` to figure out where to put walls, 
    and adds wall sprites to a map layer in a corresponding pattern.
    Args:
        columns: The number of columns of tiles in the map
        rows: The number of rows of tiles in the map
        tile_size: The size (in pixels) of each square tile
        num_loot: The number of loot sprites to add to the map
        
    """
    def __init__(self, columns, rows, tile_size, num_loot):
        super().__init__()
        self.columns = columns
        self.rows = rows
        self.tile_size = tile_size
        self.num_loot = num_loot
        self.maze = Maze(self.columns, self.rows)

        self.background_color = (20,80,20)
        self.add_layer(self.get_wall_map_layer())
        self.add_layer(self.get_loot_map_layer())
        self.generate_maze()

    def generate_maze(self, seed=None):
        """Generates (or re-generates) the map. The :py:class:`Maze` does most of the work.

        Regenerates the maze, clears the wall map layer and the loot map layer (in case
        there was a previous maze), and then populates these layers with new wall sprites
        and loot sprites.
        
        Args:
            seed: Random seed to pass to the maze (see :py:meth:`Maze.generate`)
        """
        self.maze.generate(seed)
        wall_map_layer = self.get_layer_by_name("walls")
        wall_map_layer.clear()
        for x, y in self.maze.get_walls():
            wall_map_layer.add_sprite(x, y)
        loot_map_layer = self.get_layer_by_name("loot")
        loot_map_layer.clear()
        for x, y in random.sample(self.possible_loot_locations(), self.num_loot):
            loot_map_layer.add_sprite(x, y)

    def get_wall_map_layer(self):
        """Creates a new :py:class:`GridMapLayer` to hold walls.
        """
        return GridMapLayer(
            name="walls",
            columns=self.columns,
            rows=self.rows,
            pixel_width=self.columns * self.tile_size,
            pixel_height=self.rows * self.tile_size,
            sprite_filename=resolve_resource_path("images/box.png"),
            sprite_class=Wall,
        )

    def get_loot_map_layer(self):
        """Creates a new :py:class:`GridMapLayer` to hold loot.
        """
        return GridMapLayer(
            name="loot",
            columns=self.columns,
            rows=self.rows,
            pixel_width=self.columns * self.tile_size,
            pixel_height=self.rows * self.tile_size,
            sprite_filename=resolve_resource_path("images/star.png"),
            sprite_class=Loot
        )

    def possible_loot_locations(self):
        """Returns a list of points where loot could be placed. 
        """
        X = range(1, self.columns, 2)
        Y = range(1, self.rows, 2)
        return list(product(X, Y))

if __name__ == '__main__':
    game = MazeGame()
    game.run()
