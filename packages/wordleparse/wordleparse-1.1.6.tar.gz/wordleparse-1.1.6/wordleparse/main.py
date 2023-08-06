from argparse import ArgumentParser
import logging

from wordleparse.message import Message
from wordleparse.parse import parse_messages
from wordleparse.print import print_result


parser: ArgumentParser = ArgumentParser(description="Parse and aggregate Wordle chats")

parser.add_argument("filename", help="Name of file to read chat messages from")
parser.add_argument(
    "--verbose",
    "-v",
    action="count",
    default=1,
    help="Increases logging level. You can also do -vv and -vvv, etc",
)
parser.add_argument(
    "--logfile",
    "-l",
    help="Filename to log to. Overwrites on each run",
)


def main():
    args = parser.parse_args()

    args.verbose = 40 - (10 * args.verbose) if args.verbose > 0 else 0

    if args.logfile:
        logging.basicConfig(
            filename=args.logfile, filemode="w", encoding="utf-8", level=args.verbose
        )
    else:
        logging.basicConfig(level=args.verbose)

    logging.debug("Reading file %s for messages", args.filename)
    with open(args.filename, encoding="utf8") as f:
        lines = f.readlines()

    messages: list[Message] = list(parse_messages(lines))
    games: set[str] = {m.game for m in messages}

    for game in sorted(games):
        print_result(game, [m for m in messages if m.game == game])
