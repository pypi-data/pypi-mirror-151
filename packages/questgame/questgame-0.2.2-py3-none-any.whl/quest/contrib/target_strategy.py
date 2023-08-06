from quest.strategy import Strategy
from math import sqrt

def distance(a, b):
    """A helper function to find the distance between two points. 
    Uses the pythagorean theorem!

    Arguments:
        a: (x, y) point
        b: (x, y) point
    """
    ax, ay = a
    bx, by = b
    x = ax - bx
    y = ay - by
    return sqrt(x * x + y * y)

class TargetStrategy(Strategy):
    """A strategy to go toward a target until the target is reached
    (or another condition is satisfied). Then re-choose the target.

    Attributes:
        epsilon: A distance to consider "close enough," used to decide if the sprite reached
                 its target. (If you insist on exactly reaching the target, the sprite will
                 always overshoot a little, causing it to jiggle in place forever.)
    """

    epsilon = 10
    
    def choose_course(self, sprite, game):
        """Returns a (x, y) vector representing the chosen course.
        
        First, makes sure the sprite has a target. Then checks to see if a 
        new target is needed. If so, chooses a new target. If not, sets the course
        toward the target.
        """
        self.setup_sprite(sprite, game)
        if self.needs_new_target(sprite, game):
            self.choose_new_target(sprite, game)
        return self.course_to_target(sprite, game)

    def setup_sprite(self, sprite, game):
        """Makes sure the sprite has a target set.

        Arguments:
            sprite: The sprite who is about to act.
        """
        if not hasattr(sprite, "target"):
            sprite.target = (sprite.center_x, sprite.center_y)

    def needs_new_target(self, sprite, game):
        """Decides whether the sprite needs a new target. By default, 
        a sprite needs a new target if it has (nearly) reached its original target.
        """
        current_position = (sprite.center_x, sprite.center_y)
        return distance(current_position, sprite.target) <= self.epsilon

    def choose_new_target(self, sprite, game):
        """Chooses a new target and applies it to the sprite. By defualt, this does nothing.
        Subclasses of TargetStrategy should re-implement this method for desired behavior. 
        """
        sprite.target = sprite.target

    def course_to_target(self, sprite, game):
        """Returns a (x, y) vector representing the direction to the target.
        """
        target_x, target_y = sprite.target
        return (target_x - sprite.center_x, target_y - sprite.center_y)

    



