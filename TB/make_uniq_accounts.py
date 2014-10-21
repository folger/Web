#! /usr/bin/python


def main():
    names = set()
    with open('accounts.txt', 'w') as ac:
        with open('account_files.txt') as f:
            for account in f:
                with open(account.rstrip()) as account_f:
                    for line in account_f:
                        line = line.rstrip()
                        name = line.split('|')[0]
                        if len(line) == 0 or name in names:
                            continue
                        names.add(name)
                        ac.write(line + '\n')


if __name__ == '__main__':
    main()
