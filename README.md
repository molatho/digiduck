# digiduck

A simple Python 3 tool that translates duckyscript files into arduino sketches that can be uploaded to Digisparks.

## Installation

Simply clone the repo:
```
git clone https://github.com/molatho/digiduck
```

## Usage

Taken from the generated program usage:
```
usage: digiduck [-h] [-ofile OFILE] [-l L] [-t T] [-loops LOOPS] [-loopdelay LOOPDELAY] [-initialdelay INITIALDELAY] [-blink BLINK] [-blinkdelay BLINKDELAY] ifile

Converts duckyscript into arduino sketches!

positional arguments:
  ifile                 Specifies the duckyscript input file.

optional arguments:
  -h, --help            show this help message and exit
  -ofile OFILE          Specifies the arduino output sketch. Defaults to "digiduck.ino".
  -l L                  The keyboard-layout to be used for encoding the duckyscript. Defaults to "gb".
  -t T                  Template file used for generating the arduino sketch. Defaults to digiduck's "template.inot".
  -loops LOOPS          Count of code-executions.
  -loopdelay LOOPDELAY  Delay (in ms) between code-executions.
  -initialdelay INITIALDELAY
                        Delay (in ms) before any code is executed. Used to give the computer some time to perform device-initialization.
  -blink BLINK          Blink when code is done running.
  -blinkdelay BLINKDELAY
                        Delay (in ms) between blinks.
```

You can supply your own, custom sketch template. Ideally, it should include the following placeholders (which compatible types):
* `%payloadlen%` (uint32_t)
* `%payload%` (uint8_t[])
* `%loops%` (uint32_t)
* `%loopdelay%` (uint32_t)
* `%initialdelay%` (uint32_t)
* `%blink%` (bool)
* `%blinkdelay%` (uint32_t)

## Credits
* Script encoder based on [DuckToolKit](https://github.com/Audition-CSBlock/DuckToolkit/commit/79954821f3c9e0f4985d2f43b838049423849851)
    * Due to the inactivity of the DuckToolKit project I copied over its content and fixed it where necessary.
* Sketch generator based on [duck2spark](https://github.com/mame82/duck2spark), also copied their `example.duck`