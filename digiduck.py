import argparse
import sys
import os

from generator import Generator
from ducktoolkit import encoder


def main():
    parser = argparse.ArgumentParser("digiduck", description="Converts duckyscript into arduino sketches!")
    parser.add_argument(
        'ifile',
        type=str,
        help='Specifies the duckyscript input file.'
    )
    parser.add_argument(
        '-ofile',
        type=str,
        help='Specifies the arduino output sketch. Defaults to "digiduck.ino".',
        default="digiduck.ino"
    )
    parser.add_argument(
        '-l',
        type=str,
        help='The keyboard-layout to be used for encoding the duckyscript. Defaults to "gb".',
        default="gb",
    )
    parser.add_argument(
        '-t',
        type=str,
        help='Template file used for generating the arduino sketch. Defaults to digiduck\'s "template.inot".',
        default="template.inot"
    )
    parser.add_argument(
        '-loops',
        type=int,
        help="Count of code-executions.",
        default=1
    )
    parser.add_argument(
        '-loopdelay',
        type=int,
        help="Delay (in ms) between code-executions.",
        default=2000
    )
    parser.add_argument(
        '-initialdelay',
        type=int,
        help="Delay (in ms) before any code is executed. Used to give the computer some time to perform device-initialization.",
        default=5000
    )
    parser.add_argument(
        '-blink',
        type=bool,
        help="Blink when code is done running.",
        default=True
    )
    parser.add_argument(
        '-blinkdelay',
        type=int,
        help="Delay (in ms) between blinks.",
        default=500
    )

    args = parser.parse_args(sys.argv[1::])

    duckyscript = ''
    if not args.ifile:
        print("[!] Missing input file!")
        return parser.print_help()
    duckyscript = open(args.ifile, "r").read()

    result = encoder.encode_script(duckyscript, args.l)
    if not result['valid']:
        print(f"[!] Invalid duckyscript: {result['message']}")
        return
    print(f"Successfully encoded {result['line_count']} lines!")
    bin = result['encoded_file']

    templatefile = ''
    template = ''
    if args.t:
        templatefile = args.t
    else:
        digiduckdir = os.path.split(os.path.abspath(__file__))[0]
        templatefile = os.path.join(digiduckdir, args.t)
    template = open(templatefile, "r").read()

    with open(args.ofile, 'w') as f:
        f.write(Generator.process(bin, template, args))

    print("Done!")
    return


if __name__ == '__main__':
    main()
