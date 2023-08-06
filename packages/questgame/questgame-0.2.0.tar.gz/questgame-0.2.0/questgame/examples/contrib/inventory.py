from quest.game import QuestGame
from quest.map import TiledMap
from quest.dialogue import Dialogue
from quest.modal import Modal, DialogueModal
from quest.sprite import QuestSprite, Player, Wall, NPC
from quest.helpers import scale, resolve_resource_path
from quest.strategy import RandomWalk
from quest.contrib.inventory import InventoryMixin, InventoryItemMixin
import arcade
import os
from pathlib import Path

class GrandmasSoupWithInventory(InventoryMixin, QuestGame):
    """Help Grandma find all the ingredients for her soup.

    This version has an inventory, which you can access by pressing 'i'.
    """

    player_sprite_image = resolve_resource_path("images/boy_simple.png")
    player_initial_x = 300
    player_initial_y = 300
    player_speed = 8

    def __init__(self):
        super().__init__()
        self.dialogue = Dialogue.from_ink(resolve_resource_path("grandma.ink"))
        self.modal = DialogueModal(self, self.dialogue)
        self.items = []

    def setup_maps(self):
        """Sets up the standard island map.
        """
        super().setup_maps()
        sprite_classes = {
            "Obstacles": Wall,
            "Background": QuestSprite,
        }
        self.add_map(TiledMap(resolve_resource_path("images/island/island.tmx"), sprite_classes))

    def setup_walls(self):
        """As in other examples, assigns all sprites in the "Obstacles" layer to be walls.
        """
        self.wall_list = self.get_current_map().get_layer_by_name("Obstacles").sprite_list

    def setup_npcs(self):
        """Creates and places Grandma and the vegetables.
        """
        npc_data = [
            [Grandma, "images/people/grandma.png", 3, 400, 400],
            [Carrots, "images/items/carrots.png", 1, 220, 640],
            [Mushroom, "images/items/mushroom.png", 1, 1028, 264],
            [Potatoes, "images/items/potatoes.png", 1, 959, 991],
            [Tomatos, "images/items/tomatos.png", 1, 323, 1055],
        ]
        self.npc_list = arcade.SpriteList()
        for sprite_class, image, scale, x, y in npc_data:
            sprite = sprite_class(resolve_resource_path(image), scale)
            sprite.center_x = x
            sprite.center_y = y
            self.npc_list.append(sprite)

        grandma = self.npc_list[0]
        grandma.strategy = RandomWalk(0.05) 

    def talk_with_grandma(self):
        """Opens the dialogue modal to show conversation with Grandma. This is called
        when the player collides with Grandma.
        """
        item_count = len(self.inventory())
        if item_count == 1:
            self.dialogue.run(self.inventory()[0].description.upper())
        elif item_count == 2:
            self.dialogue.run("TWO")
        elif item_count == 3:
            self.dialogue.run("THREE")
        elif item_count == 4:
            self.dialogue.run("SOUP")
        self.open_modal(self.modal)

class Grandma(NPC):
    """Grandma is an NPC. 

    Attributes:
        repel_distance: How far back the player should be pushed after colliding
            with Grandma. This is necessary because otherwise when the dialogue modal 
            closed, it would immediately reopen. Grandma is interesting, but not that 
            interesting.
    """
    repel_distance = 20

    def on_collision(self, sprite, game):
        """When the player collides with Grandma, she repels the player and then 
        :py:meth:`talk_with_grandma` is called to open the dialogue modal.
        """
        self.repel(sprite)
        if isinstance(sprite, Player):
            game.talk_with_grandma()

    def repel(self, sprite):
        "Backs the sprite away from self"
        away = (self.center_x - sprite.center_x, self.center_y - sprite.center_y)
        away_x, away_y = scale(away, self.repel_distance)
        sprite.center_x = sprite.center_x - away_x
        sprite.center_y = sprite.center_y - away_y
        sprite.stop()

class Vegetable(InventoryItemMixin, NPC):
    """A vegetable is an NPC that can be picked up.
    """
    description = "item"

class Carrots(Vegetable):
    description = "carrots"
    detailed_description = "A slightly wilted bunch of carrots"

class Mushroom(Vegetable):
    description = "mushroom"
    detailed_description = "A lovely chanterelle."

class Potatoes(Vegetable):
    description = "potatoes"
    detailed_description = "Four russet potatoes, still covered in soil."

class Tomatos(Vegetable):
    description = "tomatos"
    detailed_description = "Three shiny red tomatos."

if __name__ == '__main__':
    game = GrandmasSoupWithInventory()
    game.run()

