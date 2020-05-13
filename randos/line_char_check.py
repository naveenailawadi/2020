# user input the file name
print('Make sure that your file and this executable is in the same folder. \n')
file_name = input('What is the name of the file that you would like to prep for Woods? \n')
MAX_CHARS = 100

# read the file
with open(file_name, 'r') as file:
    # make a count to keep track of line numbers
    count = 1
    exceeded_limit = False
    for line in file:
        line_chars = len(line)
        if line_chars > MAX_CHARS:
            print(f"Line {count} is longer than {MAX_CHARS} characters. \nContains: {line_chars} characters \nDelete: {line_chars - MAX_CHARS} characters \n")
            exceeded_limit = True
        count += 1

if not exceeded_limit:
    print(f'All lines are under {MAX_CHARS} characters.')
