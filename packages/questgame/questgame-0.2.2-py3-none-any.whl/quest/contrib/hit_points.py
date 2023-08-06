class HitPointsMixin:
    """A mixin for `quest.Sprite` which adds hit points to a sprite.

    Attributes:
        max_hit_points (int): hit_points can't go above this value. Default 100.
        min_hit_points (int): hit_points can't go below this value. Default 0.
        hit_points (int): the sprite's current hit points
    """

    max_hit_points = 100
    min_hit_points = 0
    hit_points = 100

    def change_hit_points(self, delta):
        """Changes hit points by `delta`, keeping hit points within bounds. 
        Calls on_max_hit_points and on_min_hit_points if needed.
        """
    
        self.hit_points += delta
        if self.hit_points >= self.max_hit_points:
            self.hit_points = self.max_hit_points
            self.on_max_hit_points()
        if self.hit_points <= self.min_hit_points:
            self.hit_points = self.min_hit_points
            self.on_min_hit_points()

    def on_max_hit_points(self):
        """Called whenever the sprite's hit points reach the maximum
        By default, does nothing.
        """
        pass

    def on_min_hit_points(self):
        """Called whenever the sprite's hit points reach the maximum
        By default, kills the sprite.
        """
        self.kill()
