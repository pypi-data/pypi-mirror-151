from quest.examples.island import IslandAdventure
from quest.sprite import Player
from quest.contrib.hit_points import HitPointsMixin
import arcade

class MortalPlayer(HitPointsMixin, Player):
    """MortalPlayer uses `HitPointsMixin` to add hit point
    properties and methods like `change_hit_points`. Here, we re-define
    `on_collision` to lower the player's hit points whenever she bumps
    into another sprite (like a wall). Because the default behavior of
    `on_min_hit_points` is to kill the sprite, the player will be removed
    when she runs out of hit points.
    """

    max_hit_points = 3
    hit_points = 3

    def on_collision(self, other_sprite, game):
        self.change_hit_points(-1)
    

class DangerousIsland(IslandAdventure):
    """Extends `IslandAdventure` to use `MortalPlayer` and to 
    constantly report the player's hit points.
    """

    def setup_player(self):
        """Creates the player sprite. Almost the same as the regular 
        `setup_player`, except uses `MortalPlayer` instead of `Player`.
        """
        self.player = MortalPlayer(self.player_sprite_image, self.player_scaling)
        self.player.center_x = self.player_initial_x
        self.player.center_y = self.player_initial_y
        self.player.speed = self.player_speed
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def message(self):
        return "Hit points: {}/{}".format(
            self.player.hit_points,
            self.player.max_hit_points,
        )
        
if __name__ == '__main__':
    game = DangerousIsland()
    game.run()
