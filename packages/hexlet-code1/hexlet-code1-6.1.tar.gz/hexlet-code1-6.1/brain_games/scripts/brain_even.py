# !/usr/bin/env python3
"""Brain_even package."""

from brain_games.games.brain_even import brain_even


def greet():
    print('Welcome to the Brain Games!')


def main():
    greet()
    brain_even()


if __name__ == '__main__':
    main()
