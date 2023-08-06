"""This module about command line interaction."""

import prompt


def welcome_user():
    """Ask user his name and greet him."""
    name = prompt.string('May I have your name? ')
    print('Hello, {0}!'.format(name))
