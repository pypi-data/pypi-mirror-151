# sprite_directionality.py example game
# by Team Sonic and Jacob Wolf
#
# This example game showcases the sprite directionality feature found in
# quest/contrib/sprite_directionality.py
#
# Built based on code by Paul Vicent Craven

import arcade

TEXTURE_LEFT = 0
TEXTURE_RIGHT = 1
TEXTURE_DOWN = 2
TEXTURE_UP = 3

class DirectionalMixin:
    """ A mixin for `quest.sprite.Sprite` that allows the sprite to face different
    directions depending on which direction the sprite is moving.

    Arguments:
        player_sprite_image_lr (string): file path to image for left and
                                         right player sprite image
        player_sprite_image_up (string): file path to up facing image
        player_sprite_image_down (string): file path to down facing image
        player_scaling (int): scale for the sprite image
    """
    def __init__(self, player_sprite_image_lr, player_sprite_image_up, player_sprite_image_down, player_scaling):
        super().__init__(player_sprite_image_lr, player_scaling)
        self.textures = []
        texture_left = arcade.load_texture(player_sprite_image_lr, mirrored=True)
        self.textures.append(texture_left)
        texture_right = arcade.load_texture(player_sprite_image_lr)
        self.textures.append(texture_right)
        texture_down = arcade.load_texture(player_sprite_image_down)
        self.textures.append(texture_down)
        texture_up = arcade.load_texture(player_sprite_image_up)
        self.textures.append(texture_up)
        
        self.set_texture(TEXTURE_RIGHT)

    def on_update(self, game):
        """Change texture based on player direction.
        """
        super().on_update(game)
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]
        if self.change_y < 0:
            self.texture = self.textures[TEXTURE_DOWN]
        elif self.change_y > 0:
            self.texture = self.textures[TEXTURE_UP]

