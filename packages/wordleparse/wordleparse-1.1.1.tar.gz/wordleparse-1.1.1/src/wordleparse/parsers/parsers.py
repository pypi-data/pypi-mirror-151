from wordleparse.parser import MessageParser, RegexParser

num_re = r"[0-9]+"
basic_score_re = r"[1-6X]/6"

wordle_parser = MessageParser(
    "Wordle", RegexParser(rf"Wordle (?P<num>{num_re}) (?P<score>{basic_score_re}\*?)\n")
)
woordle_parser = MessageParser(
    "Woordle", RegexParser(rf"Woordle (?P<num>{num_re}) (?P<score>{basic_score_re})\n")
)
woordle6_parser = MessageParser(
    "Woordle6",
    RegexParser(rf"Woordle6 (?P<num>{num_re}) (?P<score>{basic_score_re})\n"),
)
worldle_parser = MessageParser(
    "Worldle",
    RegexParser(
        r"#Worldle (?P<num>#[0-9]+) (?P<score>[1-6X]/6(?: \([0-9]{1,3}%\))?(?: 🙈)?)(?: 🙁)?\n",
    ),
)
squardle_win_parser = MessageParser(
    "Squardle",
    RegexParser(
        r"I won Daily Squardle (?P<num>#[0-9]+) with (?P<score>[0-9]+) guess(?:es)? to spare!\n",
    ),
)
squardle_loss_parser = MessageParser(
    "Squardle",
    RegexParser(
        r"I solved (?P<score>[0-9]{1,2}/21) squares in Daily Squardle (?P<num>#[0-9]+)\n",
    ),
)
crosswordle_parser = MessageParser(
    "Crosswordle",
    RegexParser(r"Daily Crosswordle (?P<num>[0-9]+): (?P<score>[\w ]+) .*\n"),
)
primel_parser = MessageParser(
    "Primel", RegexParser(rf"Primel (?P<num>{num_re}) (?P<score>{basic_score_re})")
)
letterle_parser = MessageParser(
    "Letterle", RegexParser(r"Letterle(?P<num> )(?P<score>[0-9]{1,2}/26)")
)
not_wordle_parser = MessageParser(
    "Not Wordle",
    RegexParser(rf"Not Wordle (?P<num>{num_re}) (?P<score>{basic_score_re})\n"),
)
nerdle_parser = MessageParser(
    "Nerdle",
    RegexParser(
        rf"(?:Nerdle|nerdlegame) (?P<num>{num_re}) (?P<score>{basic_score_re})\n",
    ),
)
vardle_parser = MessageParser(
    "Vardle", RegexParser(rf"Vardle (?P<num>{num_re}) (?P<score>[1-8X]/8)\n")
)
diffle_parser = MessageParser(
    "Diffle",
    RegexParser(
        r"Diffle (?P<num>[0-9]{4}-[0-9]{1,2}-[0-9]{1,2})\n(?P<score>[0-9]+ words / [0-9]+ letters)",
    ),
)
waffle_parser = MessageParser(
    "Waffle", RegexParser(rf"#(waffle(?P<num>{num_re})|canuffle) (?P<score>[0-5X]/5)\n")
)
