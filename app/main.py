import sys
from os import listdir, environ, chdir
from os.path import isfile, isdir, join
from subprocess import run
from pathlib import Path

# for p in environ['PATH'].split(':'): print(p)
        
def exit(args):
    sys.exit(int(args[1]))


def not_found(command):
    print('{command}: not found'.format(command=command))


def echo(args):
    print(' '.join(args[1:]))


def check_builtins(args):
    command = args[1]

    if command in commands:
        return True    
    

def run_command(args):
    run(args)
        

def find_in_env_paths(command):
    path = environ['PATH']

    directories = path.split(':')
    for directory in directories:
        try:
            if is_command_in_dir(directory, command):
                return directory
        except:
            continue

    return None


def is_command_in_dir(directory, command):
    dir_list = listdir(directory)
    files_in_directory = [f for f in dir_list if isfile(join(directory, f))]
    # print(files_in_directory)
    if command in files_in_directory:
        return True


def report_type(args):
    command = args[1]

    if check_builtins(args):
        print('{command} is a shell builtin'.format(command=command))
        return
    else:
        directory = find_in_env_paths(command)
        if directory:
            print('{command} is {directory}/{command}'.format(command=command, directory=directory))
            return

            
    not_found(command)


def pwd(args):
    print(Path('.').absolute())


def change_directory(args):
    path = args[1]
    if '~' in path:
        path = path.replace('~', environ['HOME'])

    try:
        if isdir(path):
            chdir(path)
        else:
            print('cd: {path}: No such file or directory'.format(path=path))
    except:
        print('error')


commands = {
   'echo': echo,
   'exit': exit,
   'type': report_type,
   'pwd': pwd,
   'cd': change_directory
}

double_quote_allowed_backslash_characters = ['$', '\\', '"']


def flatten(lists):
    return [arg for inner_list in lists for arg in inner_list]


def remove_empty_strings(args): 
    return [arg for arg in args if len(arg) != 0]


# Hack use for double quote, don't like it, see parse_args
def get_args(user_input):
    #                         # Hack for double quote
    quotes_split = user_input.replace('\'\'', '').split('\'')

    if len(quotes_split) == 1:
        return user_input.strip().split()

    # non-quoted args will have spaces at the start or end - only split these
    args_stripped = [
        arg.strip().split()
        if len(arg) > 0 and (arg[0] == ' ' or arg[-1] == ' ') else [arg]
        for arg in quotes_split
    ]

    return remove_empty_strings(flatten(args_stripped))


def parse_arg_character(char, is_proceeding_backslash, is_inside_quotes, is_inside_double_quotes):
    pass


def parse_args(user_input):
    args = []
    current_arg = []
    is_inside_quotes = False
    is_inside_double_quotes = False
    is_proceeding_backslash = False

    for char in user_input:
        # file = "/tmp/quz/'f 38'"
        # error = "cat: /tmp/quz/f 38: No such file or directory"
        # char = \
        # is_inside_quotes = False
        # is_inside_double_quotes = True
        # is_proceeding_backslash = False
        if not is_inside_quotes and not is_proceeding_backslash and char == '\\':
            is_proceeding_backslash = True
            continue

        if not is_proceeding_backslash:
            if char == '\'':
                if is_inside_double_quotes:
                    current_arg.append(char)
                else: 
                    is_inside_quotes = not is_inside_quotes
            elif char == '\"' and not is_inside_quotes:
                is_inside_double_quotes = not is_inside_double_quotes
            elif char == ' ' and not is_inside_quotes and not is_inside_double_quotes:
                if current_arg:
                    args.append(''.join(current_arg))
                    current_arg = []
            else:
                current_arg.append(char)
        else:
            if is_inside_double_quotes and not any(c in char for c in double_quote_allowed_backslash_characters):
                current_arg.append('\\')
                current_arg.append(char)
            else:
                current_arg.append(char)

            is_proceeding_backslash = False

    if current_arg:
        args.append(''.join(current_arg))
        is_inside_quotes = False
        is_inside_double_quotes = False
        current_arg = []

    return args


def main():
    while True:
        sys.stdout.write("$ ")
        user_input = input()

        args = parse_args(user_input)

        command = args[0]

        if command in commands:
            commands[command](args)
        elif find_in_env_paths(command):
            run(args)
        else:
            not_found(command)


if __name__ == "__main__":
    main()
