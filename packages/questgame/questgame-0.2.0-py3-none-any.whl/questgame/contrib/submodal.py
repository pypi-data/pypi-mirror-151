from quest.text_label import TextLabelStack

# A submodal should return True from `choose_option` when it has completed.
# That might be confusing for other readers. So instead, import CLOSE_SUBMODAL
# and return that.
CLOSE_SUBMODAL = True

class SubmodalMixin:
    """Extends `quest.modal.Modal` so that it can support submodals.

    Sometimes a modal needs to go into a deeper level of detail. For example
    an inventory list might need to present more details about a specific item.
    This could all be implemented within one modal, but it would get complicated
    quickly. Instead, `SubmodalMixin` allows a `Modal` to open its own submodal using
    `open_submodal(modal)`.

    The top-level modal remains in control and is the only modal
    which actually gets rendered; any others are just used to access data and to
    figure out how to respond to choices.
    A modal which mixes in `SubmodalMixin` will check to see whether it has the
    property `submodal` assigned before getting its text labels, option labels, or
    choosing an option. When a submodal is present, that modal's behavior is called
    instead of the modal. (That submodal could have its own submodals!)
    When a submodal is ready to be closed, it should call `self.close()`
    from `choose_option` as usual. Instead of closing all the modals,
    `close` will signal the parent modal that it should resume control. In case
    you want to close more than one layer of modals, you can call `self.parent.close()`.

    Submodal uses two elegant and complex computer science ideas. The first is recursion,
    or having a function call itself. Recursion is useful when you can break a task into
    a simpler version of itself, or when you can accomplish a task by asking someone else to
    do it. (Asking yourself to do a task by asking yourself to do it leads to infinite recursion
    and a headache.) Check out `get_active_modal` to see an example of recursion.

    The second elegant idea is virtualization, the idea that you never know if you're at the top level.
    A submodal acts just like the main modal, attached to a game. Either way, the modal calls `close()`
    when it is finished. If it was a submodal, control passes back to the parent, but the modal calling
    `close()` doesn't know or care. A lot of stories have been written about virtualization--the
    idea of being in a dream and not knowing whether you're in a dream (or whether this reality is itself
    a dream, or maybe even a dream within a dream!

    Attributes:
        parent (Modal): This submodal's parent modal (if it has one).
        submodal (Modal): The current submodal (if any).
    """

    parent = None
    submodal = None

    def open_submodal(self, modal):
        "Attaches a submodal and sets the submodal's parent to self."
        modal.parent = self
        self.submodal = modal

    def close(self, close_all=False):
        """Closes this submodal, handing control back to the parent if there is one.

        Arguments:
            close_all (bool): If True, closes all modals, not just this one.
        """
        if close_all or self.parent is None:
            self.game.close_modal()
        else:
            self.parent.submodal = None

    def get_active_modal(self):
        """Finds the modal who should control rendering and handling input.

        If a modal has a submodal, the submodal should be in charge. (But that submodal
        might have a sub-sub-modal.) So `Submodal.get_active_modal` uses recursion to find a modal that
        doesn't have a submodal. Instead of doing the whole task, it just asks its submodal
        to find the active submodal--using exactly the same method.
        """
        if self.submodal:
            try:
                return self.submodal.get_active_modal()
            except AttributeError:
                return self.submodal
        else:
            return self

    def set_text_labels(self):
        """Creates text labels, using the active submodal if there is one.
        """
        m = self.get_active_modal()
        self.text_labels = TextLabelStack(
            m.text_label_contents(),
            self.x_center,
            self.y_center + self.height / 2
        )

    def set_option_labels(self):
        """Creates option labels, using the active submodal if there is one.
        """
        m = self.get_active_modal()
        options = m.option_label_contents()
        disposable_stack = TextLabelStack(options, 0, 0)
        self.option_labels = TextLabelStack(
            options,
            self.x_center,
            self.y_center - self.height / 2 + disposable_stack.height()
        )
        m.current_option = 0
        self.option_labels.set_highlight(m.current_option)

    def handle_change_option(self, change):
        """Handles a change option, using the active submodal if there is one.
        """
        m = self.get_active_modal()
        m.current_option = (m.current_option + change) % len(m.option_labels)
        self.option_labels.set_highlight(m.current_option)

    def handle_choice(self):
        "Lets submodal choose option, if set"
        m = self.get_active_modal()
        m.choose_option(m.current_option)
        self.set_text_labels()
        self.set_option_labels()
