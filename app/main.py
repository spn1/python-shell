import sys

def echo(args):
    print(' '.join(args))

commands = {
   'echo': echo,
}


def main():
    while True:
        sys.stdout.write("$ ")
        args = input().split(' ')
        # print(args)
        command = args[0]

        if command in commands:
            commands[command](args[1:])
        elif command == 'exit':
            return args[1]
        else:
            print('{command}: command not found'.format(command=command))



if __name__ == "__main__":
    main()
