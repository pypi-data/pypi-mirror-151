# sprite_directionality.py
# by Team Sonic
#
# This file implements a sprite mixin which causes the sprite's texture
# direction to change based on the last direction the sprite was moving.

from quest.sprite import Player
from quest.examples.grandmas_soup import GrandmasSoupGame, Grandma, Carrots, Mushroom, Potatoes, Tomatos
from quest.contrib.sprite_directionality import SpriteDirectionMixin
from quest.helpers import scale, resolve_resource_path
from quest.strategy import RandomWalk
import arcade

class DirectionalPlayer(SpriteDirectionMixin, Player):
    """ Uses the SpriteDirectionMixin to make the player sprite face different directions
    based on which direction the player is moving
    """

class DirectionalGrandma(SpriteDirectionMixin, Grandma):
    """ Uses the SpriteDirectionMixin to make the player sprite face different directions
    based on which direction the player is moving
    """

class DirectionalGame(GrandmasSoupGame):
    """Extends the GrandmasSoupGame to have a player and grandmother than face different
    directions depending on the dirtection they are moving.
    """

    player_sprite_image = resolve_resource_path("images/people/trixie.png")
    player_scaling = 3
    def setup_player(self):
        """Creates the player sprite.

        Initializes a sprite for the player, assigns its starting position,
        and appends the player sprite to a SpriteList (Arcade likes to work
        with sprites in SpriteLists).
        """
        self.player = DirectionalPlayer(self.player_sprite_image, self.player_sprite_image, self.player_sprite_image, self.player_scaling)
        self.player.center_x = self.player_initial_x
        self.player.center_y = self.player_initial_y
        self.player.speed = self.player_speed
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def setup_npcs(self):
        """Creates and places Grandma and the vegetables.
        """
        static_npc_data = [
            [Carrots, "images/items/carrots.png", 1, 220, 640],
            [Mushroom, "images/items/mushroom.png", 1, 1028, 264],
            [Potatoes, "images/items/potatoes.png", 1, 959, 991],
            [Tomatos, "images/items/tomatos.png", 1, 323, 1055],
        ]
        self.npc_list = arcade.SpriteList()
        grandma_image = resolve_resource_path("images/people/grandma.png")
        grandma = DirectionalGrandma(grandma_image, grandma_image, grandma_image, 3)
        grandma.center_x = 400
        grandma.center_y = 400
        self.npc_list.append(grandma)
        for sprite_class, image, scale, x, y in static_npc_data:
            sprite = sprite_class(resolve_resource_path(image), scale)
            sprite.center_x = x
            sprite.center_y = y
            self.npc_list.append(sprite)

        grandma = self.npc_list[0]
        walk = RandomWalk(0.05)
        grandma.strategy = walk

if __name__ == "__main__":
    game = DirectionalGame()
    game.run()
