import pyperclip


def operate_and_copy():
    output = str(input('Operation: \n'))
    num = eval(output)
    num_len = len(str(num))
    rounded_num = round(num, 2)

    if int(rounded_num) == rounded_num:
        pyperclip.copy(int(num))
    else:
        pyperclip.copy(num)

    print(f'Output: \n{round(num, 2)}')
    if len(str(rounded_num).strip('-')) < num_len:
        print('(rounded)')
