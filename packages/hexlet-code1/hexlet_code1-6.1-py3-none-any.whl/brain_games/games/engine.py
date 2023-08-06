"""Engine of all games."""

import prompt

ROUNDS_NUMBER = 3


def get_username():

    return prompt.string('May I have your name? ')


def ask_question_and_get_answer(
    question,
    question_field='Question: ',
    answer_field='\nYour answer: ',
):
    return prompt.string(question_field + str(question) + answer_field)


def compare_answer(answer, correct_answer, username):
    if answer == correct_answer:
        return 'Correct!'
    return """
        \r"{0}" is wrong answer ;(. Correct answer was "{1}".
        \rLet's try again, {2}!'
    """.format(
        answer,
        correct_answer,
        username,
    )
