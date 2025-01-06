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


def main():
    while True:
        sys.stdout.write("$ ")
        args = input().split(' ')
        # print(args)
        command = args[0]

        if command in commands:
            commands[command](args)
        elif find_in_env_paths(command):
            run(args)
        else:
            not_found(command)



if __name__ == "__main__":
    main()
