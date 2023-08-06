from quest.dialogue import Dialogue
from quest.modal import Modal, DialogueModal
from quest.examples.grandmas_soup import GrandmasSoupGame
from quest.helpers import resolve_resource_path

import os
from pathlib import Path

class GrandmasSoupVariablesGame(GrandmasSoupGame):
    """Help Grandma find all the ingredients for her soup.

    :py:class:`GrandmasSoupVariablesGame` extends the :py:class:`GrandmasSoupGame` to
    demonstrate the upgraded ink parser's support for variables.

        $ python -m quest.examples.grandmas_soup_variables

    After you play it, check out the sorce code by clicking on "source" in the
    blue bar just above.

    Attributes:
        dialogue: A :py:class:`Dialogue` containing the game's conversation.
        modal: A :py:class:`DialogueModal` to show the dialogue.
        dialogue_vars: A dictionary of dialogue variables which affect what is shown in the dialogue
    """

    def __init__(self):
        super().__init__()
        self.setup_dialogue()

    def setup_dialogue(self):
        """Sets up the dialogue with dialogue variables.
        """
        self.dialogue = Dialogue.from_ink(resolve_resource_path("grandma_variables.ink"))
        self.dialogue_vars =    {"num_veggies_left" : 4,
                                 "veggies" : "tomato, carrots, and potatoes"}
        self.dialogue.dialogue_vars = self.dialogue_vars
        self.modal = DialogueModal(self, self.dialogue)

    def got_item(self, description):
        """Adds the item's description to the items list. This is called when the
        player collides with a vegetable.

        Arguments:
            description: The item description.
        """
        self.items.append(description.upper())
        self.dialogue_vars["num_veggies_left"] -= 1    # decrement the variable tracking the number of veggies left for the dialogue
        if len(self.items) < 4:
            self.dialogue.run(self.items[-1])
        else:
            self.dialogue.run("SOUP")

if __name__ == '__main__':
    game = GrandmasSoupVariablesGame()
    game.run()
