class PlayerEnabledMixin:
    """Extends `quest.QuestGame` to allow setting whether the player is enabled or not.
    When the player is disabled, user input is ignored. Note that the game may still take 
    actions affecting the player sprite, just not the user.

    Attrs:
        player_enabled (bool): When True (default), user input controls the player.

    """

    player_enabled = True

    def on_key_press(self, key, modifiers):
        """Delegates to the regular `on_key_press` method when `player_enabled` is True.

        Arguments:
            key: The key that was pressed.
            modifiers: A list of currently-active modifier keys (e.g. shift).
        """
        if self.player_enabled:
            super().on_key_press(key, modifiers)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        Delegates to the regular `on_mouse_motion` when `player_enabled` is True.

        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method was called
        :param float dy: Change in y since the last time this method was called
        """
        if self.player_enabled:
            super().on_mouse_motion(x, y, dx, dy)
