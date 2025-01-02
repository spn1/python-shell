import sys


def main():
    while True:
        sys.stdout.write("$ ")
        command = input()

        if command == 'exit':
            break

        print('{command}: command not found'.format(command=command))


if __name__ == "__main__":
    main()
