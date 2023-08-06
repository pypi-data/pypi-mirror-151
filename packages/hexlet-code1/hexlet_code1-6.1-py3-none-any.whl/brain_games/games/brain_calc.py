"""Calculator game."""

from random import choice, randint

from brain_games.games.engine import (
    ROUNDS_NUMBER,
    ask_question_and_get_answer,
    compare_answer,
    get_username,
)


def brain_calc():

    username = get_username()

    print('Hello, {0}!'.format(username))
    print('What is the result of the expression?')

    current_round = 0

    while current_round < ROUNDS_NUMBER:
        num1 = randint(0, 100)
        num2 = randint(0, 100)
        operations = ('+', '-', '*')
        operation = choice(operations)

        user_answer = ask_question_and_get_answer(
            '{0} {1} {2}'.format(num1, operation, num2),
        )
        answers = {
            '+': num1 + num2,
            '-': num1 - num2,
            '*': num1 * num2,
        }
        correct_answer = answers[operation]

        examination = compare_answer(
            int(user_answer),
            correct_answer,
            username,
        )

        print(examination)

        if examination == 'Correct!':
            current_round += 1
        else:
            break

        if current_round == ROUNDS_NUMBER:
            print('Congratulations, {0}!'.format(username))
