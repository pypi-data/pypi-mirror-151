"""Parity check game."""

from random import randint

from brain_games.games.engine import (
    ROUNDS_NUMBER,
    ask_question_and_get_answer,
    compare_answer,
    get_username,
)


def brain_even():
    username = get_username()

    print('Hello, {0}!'.format(username))
    print('Answer "yes" if the number is even, otherwise answer "no".')

    current_round = 0

    while current_round < ROUNDS_NUMBER:
        num = randint(0, 100)
        user_answer = ask_question_and_get_answer(num)
        correct_answer = 'yes' if num % 2 == 0 else 'no'
        examination = compare_answer(user_answer, correct_answer, username)

        print(examination)

        if examination == 'Correct!':
            current_round += 1
        else:
            break

        if current_round == ROUNDS_NUMBER:
            print('Congratulations, {0}!'.format(username))
