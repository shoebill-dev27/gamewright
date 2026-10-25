"""Lamplight Keeper - play an input script.

Usage: python3 play.py [--trace] SCRIPT
"""
import sys

from lamplight import run_script


def main(argv):
    args = argv[1:]
    trace = False
    if args and args[0] == "--trace":
        trace = True
        args = args[1:]
    if len(args) != 1:
        sys.stderr.write("usage: python3 play.py [--trace] SCRIPT\n")
        return 2
    try:
        with open(args[0], encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        sys.stderr.write("cannot read script: %s\n" % e)
        return 2
    out, code = run_script(text, trace)
    sys.stdout.write(out)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
