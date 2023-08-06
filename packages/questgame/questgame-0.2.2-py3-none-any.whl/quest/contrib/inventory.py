from quest.contrib.removable import RemovableMixin
from quest.contrib.submodal import SubmodalMixin, CLOSE_SUBMODAL
from quest.modal import Modal
from collections import Counter
import arcade

class InventoryMixin(RemovableMixin):
    """A mixin for QuestGame which provides an inventory.

    Pick up and drop  behavior can be implemented in a very simple way
    because `RemovableMixin` provides most of what we need. Also creates an
    `InventoryModal` and binds a key to open it (by default, 'i').

    Attributes:
        inventory_shortcut: A key which should open the inventory.
    """
    inventory_shortcut = arcade.key.I

    def __init__(self):
        super().__init__()
        self.inventory_modal = InventoryModal(self, self.inventory())

    def inventory(self):
        "A helper to return the inventory"
        return self.removed_sprite_lists['inventory']

    def pick_up(self, sprite):
        """Removes a sprite from the game and adds it to the inventory.
        """
        self.remove_sprite_from_game(sprite, "inventory")

    def drop(self, sprite):
        """Removes a sprite from the inventory and adds it to the game.

        Moves the sprite to the player's position and sets its `dropped_by` property
        to the player (to make sure it doesn't immediately get picked up).
        """
        self.add_sprite_to_game(sprite)
        sprite.recently_dropped = True
        sprite.center_x = self.player.center_x
        sprite.center_y = self.player.center_y

    def on_key_press(self, key, modifier):
        """Overrides `on_key_press` so that when the inventory shortcut key is
        pressed, opens the inventory. Otherwise, delegates to the parent
        `on_key_press` method.
        """
        if key == self.inventory_shortcut:
            self.open_modal(self.inventory_modal)
        else:
            super().on_key_press(key, modifier)

class InventoryItemMixin:
    """A mixin for QuestSprite which allows it to behave as an inventory item.

    Attributes:
        detailed_description (str): A more detailed description.
        dropped_by (QuestSprite): Keeps track of whether the sprite was recently dropped.
        usable (bool): Indicates whether the item can be used.
    """

    detailed_description = "An inventory item"
    recently_dropped = False
    usable = False
    droppable = True

    def on_update(self, game):
        """When this sprite has recently been dropped, checks to see whether the
        dropped (probably the player) is still colliding. If not, sets `self.dropped_by`
        to None, indicating that the sprite can be picked up again.
        """
        if self.recently_dropped:
            if not self.collides_with_sprite(game.player):
                self.recently_dropped = False

    def on_collision(self, sprite, game):
        """Causes the sprite to be picked up, unless it was just dropped.
        """
        if sprite == game.player and not self.recently_dropped:
            game.pick_up(self)

    def use(self, game):
        """What should happen when used. By default, kills the item.
        """
        self.kill()

class InventoryModal(SubmodalMixin, Modal):
    """An extension of Modal which interaacts with inventories.
    """
    welcome_message = "Your inventory:"
    close_modal_option = "OK"

    def __init__(self, game, inventory):
        self.inventory = inventory
        super().__init__(game)

    def text_label_contents(self):
        return [self.welcome_message]

    def option_label_contents(self):
        labels = []
        for description in self.unique_item_descriptions():
            count = self.count_items_with_description(description)
            labels.append("{} ({})".format(description, count))
        labels.append(self.close_modal_option)
        return labels

    def choose_option(self, value):
        choice = self.option_label_contents()[value]
        if choice == self.close_modal_option:
            self.game.close_modal()
        else:
            description = self.unique_item_descriptions()[value]
            item = self.get_item_with_description(description)
            self.open_submodal(self.get_detail_modal(item))

    def get_detail_modal(self, item):
        count = self.count_items_with_description(item.description)
        return InventoryItemModal(self.game, item, count)

    def get_item_with_description(self, description):
        for item in self.inventory:
            if item.description == description:
                return item

    def unique_item_descriptions(self):
        return sorted(set([item.description for item in self.inventory]))

    def count_items_with_description(self, description):
        return len([item for item in self.inventory if item.description == description])

class InventoryItemModal(SubmodalMixin, Modal):
    """A modal for interacting with an inventory item.
    """
    name = "inventory item modal"
    use_option = "use"
    drop_option = "drop"
    close_modal_option = "back"

    def __init__(self, game, item, count):
        self.item = item
        self.count = count
        super().__init__(game)

    def text_label_contents(self):
        return [
            "{} ({})".format(self.item.description, self.count),
            self.item.detailed_description
        ]

    def option_label_contents(self):
        verbs = []
        if self.item.usable:
            verbs.append(self.use_option)
        if self.item.droppable:
            verbs.append(self.drop_option)
        verbs.append(self.close_modal_option)
        return verbs

    def choose_option(self, value):
        verb = self.option_label_contents()[value]
        if verb == self.drop_option:
            self.game.drop(self.item)
        elif verb == self.use_option:
            self.item.use(self.game)
        self.close()
