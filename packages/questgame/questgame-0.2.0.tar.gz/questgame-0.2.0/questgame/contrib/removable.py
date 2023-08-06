from arcade import SpriteList
from collections import defaultdict

class RemovableMixin:
    """A mixin for QuestGame which adds support for removing sprites from the game.

    When a sprite is removed, it no longer shows up on the game map. This could already be 
    achieved using `sprite.kill()`, but sometimes you want to keep track of a sprite even though 
    it has been removed: perhaps it will return, or perhaps it has gone somewhere like into 
    the player's inventory. 

    The key to this mixin is that `QuestGame` only renders and checks for collisions on certain
    SpriteLists, such as `self.wall_list` and `self.npc_list`. So when we remove a sprite from 
    one of these "live" SpriteLists, it will no longer show up or trigger collisions.

    RemovableMixin extends initialization to add a dictionary called `removed_sprite_lists`, 
    where each key is the name of a list in which to store removed sprites. If you don't need
    more than one place to store removed sprites, you can ignore this; they will all be stored
    in "default."

    Attributes:
        removed_sprite_list_names: A list of strings naming destinations for 
            removed sprites. By default, there is just one destination, called "default,"
            but you might want others like "inventory" or "shop" or 
            "dead_spirits_seeking_revenge." 
    """

    def __init__(self):
        super().__init__()
        self.removed_sprite_lists = defaultdict(SpriteList)

    def add_sprite_to_game(self, sprite):
        """Adds the sprite to the game and removes it from storage.

        If the sprite is in any of the removed_sprite_lists, it is removed from them.
        If the sprite is not already in `self.npc_list`, adds the sprite.
        """
        for removed_sprite_list in self.removed_sprite_lists.values():
            if sprite in removed_sprite_list:
                removed_sprite_list.remove(sprite)
        if sprite not in self.npc_list:
            self.npc_list.append(sprite)

    def remove_sprite_from_game(self, sprite, destination="default"):
        """Removes the sprite from the game and adds it to storage.

        If the sprite is in `self.npc_list`, it is removed.
        If the sprite is not already in the specified removed sprite list, adds it.
        """
        if sprite in self.npc_list:
            self.npc_list.remove(sprite)
        if sprite not in self.removed_sprite_lists[destination]:
            self.removed_sprite_lists[destination].append(sprite)
