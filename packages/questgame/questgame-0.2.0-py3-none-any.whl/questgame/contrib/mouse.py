class MouseMotionMixin:
    """Extends `quest.QuestGame` to allow the player to be controlled by the mouse.
    Example usage::

        from quest.examples.island import IslandAdventure
        from quest.contrib.mouse import MouseMotionMixin

        class IslandWithMouse(MouseMotionMixin, IslandAdventure):
            "The island adventure with mouse control."

        IslandWithMouse().run()
    """

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        Keep track of the mouse's new coordinates whenever it moves.
        This method is called automatically whenever the mouse moves.

        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method was called
        :param float dy: Change in y since the last time this method was called
        """

        if self.player.center_y != y:
            self.player.change_y = dy
        if self.player.center_x != x:
            self.player.change_x = dx
