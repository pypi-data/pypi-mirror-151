from quest.examples.maze import MazeGame
from quest.contrib.maze_walk_strategy import MazeWalkStrategy
from quest.sprite import NPC
from quest.helpers import resolve_resource_path
from datetime import datetime

class MazeWalkerGame(MazeGame):
    """Extends the MazeGame to add an evil NPC who steals loot. 
    """

    def setup_npcs(self):
        super().setup_npcs()
        enemy = NPC(resolve_resource_path("images/people/pops.png"), 1.5)
        grid = self.get_current_map().get_layer_by_name("walls")
        enemy.strategy = MazeWalkStrategy(grid, self.wall_list)
        enemy.center_x = self.player.center_x
        enemy.center_y = self.player.center_y
        enemy.speed = 4
        self.npc_list.append(enemy)

    def on_loot_collected(self, collector):
        """A method to be called whenever loot is collected.

        See the :py:class:`Loot` NPC sprite below. It calls this method whenever there is
        a collision with the player.
        """
        if collector == self.player:
            self.score += 1
        else:
            self.max_score -= 1
        if self.score == self.max_score:
            self.game_over = True
            self.final_elapsed_time = (datetime.now() - self.level_start).seconds
    
    def message(self):
        """Returns a string like "Time 12 (12/25)"
        """
        if self.game_over:
            return "Final score: {} in {} seconds".format(self.max_score, self.final_elapsed_time)
        else:
            elapsed_time = datetime.now() - self.level_start
            return "Time {} ({}/{})".format(elapsed_time.seconds, self.score, self.max_score)

if __name__ == '__main__':
    game = MazeWalkerGame()
    game.run()
