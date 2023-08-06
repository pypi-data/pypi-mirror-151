# Contributions Directory
This directory will store student feature contributions to the Quest framework. Features will be added here as mixin classes you can add to extension like `Game`, `Sprite`, `Strategy`, ect.

## Using a mixin

You can import a mixin from the contrib directory into your game module like this:

    from quest.contrib.MIXIN_NAME import MixinClass

## Contributing a feature

1. Create and checkout a branch off of the `master branch: `git checkout -b BRANCH_NAME`
1. Develop a mixin that works with one of the existing classes in the framework i.e. `QuestGame`, `QuestSprite`
2. Place your code into a module named `FEATURENAME.py` and move it to this folder.
3. Write documentation for your mixin. Follow the patterns in the core Quest files, writing class and method documentation ising docstrings.
4. Commit and push your code to the Quest GitHub repository.
5. Create a pull request to merge your branch into the `master` branch.
