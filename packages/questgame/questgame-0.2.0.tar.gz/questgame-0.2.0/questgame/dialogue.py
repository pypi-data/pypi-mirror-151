from quest.helpers import SimpleInkParser

class Dialogue:
    """Models a dialogue interaction as a graph of knots. Each knot has a list of content
    and then a list of choices leading to further knots (or ending the dialogue).
    where each choice links to another talk turn or ends the dialogue. A Dialogue
    instance has a "result" property which the game can use to determine what
    happened.
    """

    @classmethod
    def from_ink(cls, ink_path):
        """Reads talk turns from a YAML file and uses them to initialize a new
        Dialogue. Note that this is a @classmethod, which means it should be used
        by the Dialogue class, not an instance of Dialgoue. For example:

            >>> dialogue = Dialogue.from_ink("examples/dialogue_sample.ink")

        Arguments:
            ink_path: A string with the ink filename containing talk turns.
                talk turns. For an example of the expected format, see
                `quest/examples/dialogue_sample.ink`.

        Returns:
            A newly-created Dialogue instance.
        """
        parser = SimpleInkParser()
        with open(ink_path) as dialogue_file:
            knots = parser.parse(dialogue_file)
        return Dialogue(knots)

    def __init__(self, knots):
        self.knots = knots
        self.dialogue_vars = None
        self.run()

    def run(self, start_at="START"):
        """Starts (or re-starts) a run of the dialogue by setting the
        current knot to `start_at` and `running` to True.

        Arguments:
            start_at: (default "START") Name of knot to start at.
        """
        self.current_knot = start_at
        self.knots_visited = [self.current_knot]
        self.running = True

    def get_content(self):
        """Returns a list of the content for the current knot.
        """
        content =  self.knots[self.current_knot]['content']
        if self.dialogue_vars:
            content = self.replace_vars(content)
        return content

    def get_options(self):
        """Returns a list of option text for the current knot.
        """
        options = list(self.knots[self.current_knot]['options'].keys())
        if self.dialogue_vars:
            options = self.replace_vars(options)
        return options

    def choose(self, choice):
        """Chooses an option and moves to another knot. If that knot is "END",
        ends the current dialogue run.

        Arguments:
            choice (int): The index of the choice to follow.
        """
        choices = list(self.knots[self.current_knot]['options'].values())
        if choices[choice] == 'END':
            self.running = False
        else:
            self.current_knot = choices[choice]
            self.knots_visited.append(self.current_knot)

    def replace_vars(self, contents):
        """Returns the content items of a knot or option content list with the ink variables replaced with variables
        from the game's dialogue_vars dictionary.

        Arguments:
            content (str): the ink content
            dialogue_vars (dict): the variables from the game associated with their value
        """
        var_filled_contents = []
        for content_item in contents:
            var_filled_content_item = []
            content_item_vars = content_item.split("}")
            for num, text_with_var in enumerate(content_item_vars):
                if num == len(content_item_vars)-1:                  # last item in list, no variables, append whole string
                    var_filled_content_item.append(text_with_var)
                else:                                                # replace variables and append
                    if text_with_var[-1] == "\\":   # found "}" was actually "\}"
                        var_filled_content_item.append(text_with_var)
                        var_filled_content_item.append("}")
                    else:                           # replace ink variable
                        static_text, ink_var = text_with_var.rsplit("{", 1)
                        var_filled_content_item.append(static_text)
                        try:
                            ink_var_value = self.dialogue_vars[ink_var]
                        except Exception as e:
                            raise ValueError(f"Variable {ink_var} from ink file not found in dialogue_vars dictionary.")
                        var_filled_content_item.append(str(ink_var_value))
            content_item_string = "".join(var_filled_content_item)
            content_item_string = content_item_string.replace("\\{", "{")
            content_item_string = content_item_string.replace("\\}", "}")
            var_filled_contents.append(content_item_string)
        return var_filled_contents

class DialogueRunner:
    """Runs a Dialgoue from the command line. This is useful for testing out dialogue.
    If you have a file called "conversation.ink", here's an example of how to run it:

        >>> dialogue = Dialogue.from_ink("conversation.ink")
        >>> runner = DialogueRunner()
        >>> runner.run(dialogue)
    """
    def run(self, dialogue, start_at="START", dialogue_vars = None):
        dialogue.run(start_at=start_at)
        while dialogue.running:
            print('-' * 80)
            for content in dialogue.get_content(dialogue_vars):
                print(content + '\n')
            for i, option in enumerate(dialogue.get_options(dialogue_vars)):
                print("{}) {}".format(i, option))
            dialogue.choose(self.get_numeric_choice(maximum=i))

    def get_numeric_choice(self, maximum=None):
        choice = input("> ")
        while not choice.isdigit() and int(choice) <= maximum:
            print("Please enter a number between 0 and {}.".format(maximum))
            choice = input("> ")
        return int(choice)

if __name__ == '__main__':
    dialogue = Dialogue.from_ink("examples/dialogue_sample.ink")
    runner = DialogueRunner()
    runner.run(dialogue)
