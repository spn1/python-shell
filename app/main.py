import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input().split()

        if command[0] == 'exit':
            return command[1]

        print('{command}: command not found'.format(command=command[0]))


if __name__ == "__main__":
    main()
