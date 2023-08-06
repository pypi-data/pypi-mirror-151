# npchase.py
# by NpChase and Jacob Wolf

from quest.strategy import Strategy

class Chase(Strategy):
    def choose_course(self, sprite, game):
        """Moves the NPC towards the character.

        Arguments:
            sprite: The sprite who is about to act.
            game: The game object (to access attributes useful in choosing the course).

        Returns:
            (int, int) pair of the amount to change in the x and y direction
        """
        x_npc = sprite.center_x
        y_npc = sprite.center_y
        x_player = game.player.center_x
        y_player = game.player.center_y
        x_int = x_player - x_npc
        y_int = y_player -  y_npc
        return (x_int, y_int)
