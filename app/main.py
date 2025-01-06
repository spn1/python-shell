import sys

def not_found(command):
    print('{command}: not found'.format(command=command))

def echo(args):
    print(' '.join(args[1:]))

def report_type(args):
    command = args[1]
    if command in commands:
        print('{command} is a shell builtin'.format(command=command))
    else:
        not_found(command)
        
def exit(args):
    sys.exit(int(args[1]))

commands = {
   'echo': echo,
   'exit': exit,
   'type': report_type
}


def main():
    while True:
        sys.stdout.write("$ ")
        args = input().split(' ')
        # print(args)
        command = args[0]

        if command in commands:
            commands[command](args)
        else:
            not_found(command)



if __name__ == "__main__":
    main()
