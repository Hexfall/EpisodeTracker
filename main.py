#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace

from ShowManager import ShowManager


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('show', type=str, nargs='?', help='The name of the show', default=None)
    parser.add_argument('-l', '--list_shows', action='store_true', help='List all shows in store and exit.')
    parser.add_argument('-w', '--watch', action='store_true', help='To be used in conjunction with other flags. Start '
                                                                   'show after performing other actions.')
    parser.add_argument('-r', '--reset', action='store_true', help='Reset a shows episode index back to 0.')
    parser.add_argument('-s', '--set', type=str, help='Update a shows episode index. Can be used with + or - for '
                                                      'relative index. Example: \'-s +3\' or \'-s -10\'.')
    parser.add_argument('--remove', action='store_true', help='Remove a show from the list, along with tracking data.')
    parser.add_argument('-a', '--add', type=str, help='Add a show to the list. Use with path to the show.')

    return parser.parse_args()


def main() -> None:
    args = get_args()
    print(args)
    with ShowManager() as sm:
        sm.play(args.show)


if __name__ == '__main__':
    main()
