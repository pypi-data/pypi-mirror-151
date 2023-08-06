from quest.game import QuestGame
from quest.map import TiledMap
from quest.dialogue import Dialogue
from quest.modal import Modal, AlertModal, DialogueModal
from quest.sprite import QuestSprite, Player, Wall, NPC
from quest.helpers import scale, resolve_resource_path
from quest.strategy import RandomWalk
from quest.contrib.inventory import InventoryMixin, InventoryItemMixin
from quest.contrib.shop import ShopMixin
from quest.contrib.coin import CoinMixin
from quest.examples.grandmas_soup import Grandma
import arcade
import os
from pathlib import Path

class GrandmasSoupWithShop(InventoryMixin, ShopMixin, CoinMixin, QuestGame):
    """Help Grandma find all the ingredients for her soup.

    This game demonstrates how to use a shop attribute as part of a game.
    """

    player_sprite_image = resolve_resource_path("images/boy_simple.png")
    player_initial_x = 300
    player_initial_y = 300
    player_speed = 8
    total_coins = 12
    map_dimensions = (1000, 1000)
    money = 0

    def __init__(self):
        super().__init__()
        self.welcome = AlertModal(self, "Press i for inventory and z to enter the shop.")
        self.dialogue = Dialogue.from_ink(resolve_resource_path("grandma.ink"))
        self.modal = DialogueModal(self, self.dialogue)
        self.shop_inventory().append(Tomatos(resolve_resource_path("images/items/tomatos.png"), 1))
        self.shop_inventory().append(Potatoes(resolve_resource_path("images/items/potatoes.png"), 1))
        #self.open_modal(self.welcome)

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
        super().setup_npcs()
        npc_data = [
            [Carrots, "images/items/carrots.png", 1, 220, 640],
            [Mushroom, "images/items/mushroom.png", 1, 1028, 264],
            [Grandma, "images/people/grandma.png", 3, 400, 400],
        ]
        for sprite_class, image, scale, x, y in npc_data:
            sprite = sprite_class(resolve_resource_path(image), scale)
            sprite.center_x = x
            sprite.center_y = y
            self.npc_list.append(sprite)

        grandma = self.npc_list[-1]
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

    def got_coin(self):
        self.money += 1

    def message(self):
        return "${}".format(self.money)

class Vegetable(InventoryItemMixin, NPC):
    """A vegetable is an NPC that can be picked up.
    """
    description = "item"
    price = 4

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
    game = GrandmasSoupWithShop()
    game.run()
