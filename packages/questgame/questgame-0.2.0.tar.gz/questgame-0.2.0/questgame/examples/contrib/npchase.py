# npchase.py example game
# by NpChase and Jacob Wolf

from quest.contrib.npchase import Chase
from quest.examples.grandmas_soup import GrandmasSoupGame


class AffectionateGrandmaGame(GrandmasSoupGame):
    """Same game as GrandmasSoup but in this version she REALLY wants to talk to you.
    """

    def setup_npcs(self):
        """ Sets up the NPCs and gives grandma a chase strategy
        """
        super().setup_npcs()
        grandma = self.npc_list[0]
        walk = Chase()
        grandma.strategy = walk

if __name__ == '__main__':
    game = AffectionateGrandmaGame() 
    game.run()

