from pyperclip import copy


def format_static(file):
    formatted_string = f"url_for('static', filename='{file}')"
    formatted_string = '{{' + formatted_string + '}}'

    return formatted_string


def format_on_input():
    while True:
        some_file = input('Filename: ')
        formatted_string = format_static(some_file)
        print('\n')

        # copy it
        copy(formatted_string)
