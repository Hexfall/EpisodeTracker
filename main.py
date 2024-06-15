#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace

from Constants import *
from ShowManager import ShowManager


data_path = os.path.join(os.path.dirname(__file__), 'data')


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('show', type=str, nargs='?', help='The name of the show', default=None)
    parser.add_argument('-l', '--list_shows', action='store_true', help='List all shows in store and exit.')
    parser.add_argument('-p', '--play', action='store_true', help='Play next episode of last played show.')
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
    if os.path.exists(lastshow_path):
        with open(lastshow_path, 'r') as f:
            lastshow = f.read().strip()
    else:
        lastshow = None

    with ShowManager() as sm:
        if args.list_shows:
            longest = max(map(len, sm.get_shows()))
            print("\n".join(
                [f'{show:.<{longest + 4}}{sm.get_progress(show)}' for show in sm.get_shows()]
            ))
        elif args.play:
            if lastshow not in sm.get_shows():
                print("Last played show no longer exists")
                exit()
            sm.play(lastshow)
        else:
            if args.show is None:
                print('Missing show name to interact with.')
                exit()
            action = args.reset or args.set is not None or args.remove or args.add is not None
            if args.add is not None:
                sm.add_show(args.show, args.add)
            if args.reset or args.set is not None or args.remove or not action or args.watch:
                if args.show in sm.get_shows():
                    if args.reset:
                        sm.reset_index(args.show)
                    if args.set is not None:
                        if args.set.startswith("+") or args.set.startswith("-"):
                            sm.inc_index(args.show, int(args.set))
                        else:
                            sm.set_index(args.show, int(args.set))
                    if args.remove:
                        sm.remove_show(args.show)
                    elif not action or args.watch:
                        sm.play(args.show)
                else:
                    print('Show not found in library.')
            with open(lastshow_path, 'w') as f:
                f.write(args.show)


if __name__ == '__main__':
    main()
