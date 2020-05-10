import random


def run_game():
    max_numbers = int(input('Max number: '))
    guesses = int(input('Guesses: '))
    some_nums = list(range(1, max_numbers + 1))
    random.shuffle(some_nums)
    selection = some_nums[0]
    user_input = max_numbers + 5

    guess_count = 0
    try:
        user_input = int(input('Guess a number: '))
    except ValueError:
        try:
            user_input = int(input('Try again: '))
        except ValueError:
            print('You are a moron. Learn what a number is.')
            return
    while user_input != selection:
        guess_count += 1
        if user_input > selection:
            print('Too high')
        elif user_input < selection:
            print('Too low')
        if guesses == guess_count:
            print('You are a failure')
            break
        user_input = int(input('Try again: '))
        if user_input == selection:
            print('You got it! The number is {selection}.')


if __name__ == '__main__':
    run_game()
