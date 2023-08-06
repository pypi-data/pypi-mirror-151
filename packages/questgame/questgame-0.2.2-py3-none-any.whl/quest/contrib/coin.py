# coin.py
# by Jacob Wolf

from quest.sprite import NPC
from quest.helpers import resolve_resource_path
from arcade import check_for_collision_with_list
from random import randint


class CoinMixin:
    """ Mixin to add collectable coins to your game. Coins are randomly placed
    around the walkable area of the game's map.

    attributes:
        coins_collected: the number of coins collected so far by the player

    Note: The game this class is mixed into must define a total_coins property
    and a map_dimensions property.

    See examples/contrib/shop.py for an example of how this mixin can be used.
    """
    coins_collected = 0

    def setup_npcs(self):
        """Randomly places coins around the walkable area of the
        map.
        """
        super().setup_npcs()
        for i in range(self.total_coins):
            sprite = Coin()
            while True:
                sprite.center_x = randint(0, self.map_dimensions[0])
                sprite.center_y = randint(0, self.map_dimensions[1])
                if not check_for_collision_with_list(sprite, self.wall_list):
                    break
            self.npc_list.append(sprite)

    def got_coin(self):
        """Called when the player collides with a coin. Increments the
        coin property of the game.
        """
        print("Got coin!")
        self.coins_collected += 1


class Coin(NPC):
    """A coin to be collected by the player
    """
    description = "coin"

    def __init__(self):
        super().__init__(resolve_resource_path("images/items/coin.png"), .1)

    def on_collision(self, sprite, game):
        """When the player collides with a coin, it tells the game and then
        kills itself.
        """
        game.got_coin()
        self.kill()
