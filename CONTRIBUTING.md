# How to contribute

## Getting started
* Make sure you have a [GitHub account](https://github.com/signup/free)
* Submit a ticket for your issue, assuming one does not already exist.
  * Clearly describe the issue including steps to reproduce when it is a bug.
  * Make sure you fill in the earliest version that you know has the issue.
* Fork the repository on GitHub

## Making Changes
 * Create a topic branch from where you want to base your work.
    * This is usually the master branch.
    * To quickly create a topic branch based on master; `git checkout -b fix/master/my_contribution master`.
    Please avoid working directly on the `master` branch.
* Make commits of logical units.
* Check for unnecessary whitespace with `git diff --check` before committing.
* Make sure your commit messages are in the proper format.3
* Make sure you have added the necessary tests for your changes.
* Run _all_ the tests to assure nothing else was accidentally broken.

# Submitting Changes

 * Push your changes to a topic branch in your fork of the repository.
 * Submit a pull request to the repository in the cms-l1t-offline organization.
 * Mention the ticket number in your pull request

# Additional Resources
* [General GitHub documentation](https://help.github.com/)
* [GitHub pull request documentation](https://help.github.com/articles/creating-a-pull-request/)
* Plugins/extensions for PEP8 formatting
  * [Atom beautify](https://atom.io/packages/atom-beautify)
  * [Eclipse PyDEV](http://www.pydev.org/)
  * [Emacs pep8](http://avilpage.com/2015/05/automatically-pep8-your-python-code.html)
  * [VIM pep8 formatter](https://github.com/nvie/vim-flake8)
