#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys
import json
import time
import binascii
from .common import convert_hex

major_version = sys.version_info[0]

DEBUG = False


def hidg_write(elements):
    values = bytearray(elements)
    not_hold = bytearray([0, 0, 0, 0, 0, 0, 0, 0])

    hidg = open("/dev/hidg0", "wb")
    hidg.write(values)
    hidg.write(not_hold)
    hidg.close()


def parse_text(duck_text, lang_file, bunny):

    if major_version == 3:
        # COnvert the lang file to bytes
        lang_file = {key: val.encode() for key, val in lang_file.items()}

    line_count = 0
    encoded_file = []
    duck_text = duck_text.replace("\r", "")
    cmd = instruction = False

    default_delay = 0

    response = {
        "line_count": 0,
        "encoded_file": [],
        "valid": True,
        "message": ""

    }

    for line in duck_text.split('\n'):
        if len(line) > 0:

            # REM Comments
            if line.startswith('REM') or line.startswith('rem'):
                continue

            # Last Command
            last_command = cmd
            last_instruction = instruction

            response['line_count'] += 1
            line = line.lstrip().rstrip()
            parsed_line = line.split(' ', 1)

            if len(parsed_line) >= 2:
                cmd = parsed_line[0].strip()
                instruction = parsed_line[1].rstrip()
            else:
                cmd = parsed_line[0].strip()
                instruction = False

            if DEBUG:
                print("CMD: ", cmd, "Instruction: ", instruction)

            # Default Delay
            if cmd in ['DEFAULT_DELAY', 'DEFAULTDELAY']:
                try:
                    default_delay = int(instruction)
                    continue
                except Exception as e:
                    response['valid'] = False
                    response['message'] = e
                    return response

            # Repeat
            repeat_count = 1
            if cmd.lower() in ['repeat', 'replay']:
                try:
                    repeat_count = int(instruction)
                except Exception as e:
                    response['valid'] = False
                    response['message'] = "Repeat value not valid"
                    return response

                cmd = last_command
                instruction = last_instruction

            for i in range(repeat_count):
                if cmd == 'STRING':
                    for char in instruction:

                        if major_version == 3:
                            char = char  # char.encode(encoding="utf8")

                        elements = lang_file[char].split(b',')
                        elements = [int(i, 16) for i in elements]
                        # Bunny Support
                        if bunny:
                            for i in range(5):
                                elements.append(0)
                            hidg_write(elements)
                        else:
                            # response['encoded_file'].append(convert_hex(elements[2]))
                            # response['encoded_file'].append(convert_hex(elements[0]))
                            response['encoded_file'].append(elements[2])
                            response['encoded_file'].append(elements[0])
                        if DEBUG:
                            print(char, ': ', convert_hex(elements[2]), convert_hex(elements[0]))

                elif cmd == 'DELAY':
                    # Bunny Support
                    if bunny:
                        time.sleep(0.001 * int(instruction))
                    else:
                        response['encoded_file'].extend(add_delay(int(instruction)))

                elif cmd in iter(lang_file.keys()):

                    elements = lang_file[cmd].split(b',')
                    elements = [int(i, 16) for i in elements]
                    # Bunny Support
                    for i in range(5):
                        elements.append(0)

                    if instruction:
                        param = lang_file[instruction].split(b',')
                        param = [int(i, 16) for i in param]
                        elements[0] |= param[0]
                        elements[2] |= param[2]

                    # Bunny Support
                    if bunny:
                        hidg_write(elements)
                    else:
                        response['encoded_file'].append(elements[2])
                        response['encoded_file'].append(elements[0])
                        # response['encoded_file'].append(convert_hex(elements[2]))
                        # response['encoded_file'].append(convert_hex(elements[0]))

                    if DEBUG:
                        print(instruction, ': ', convert_hex(elements[2]), convert_hex(elements[0]))
                else:

                    response['valid'] = False
                    response['message'] = "{0} is not a valid command".format(cmd)
                    return response

                # Add Default Delay
                if default_delay:
                    if bunny:
                        time.sleep(0.001 * int(default_delay))
                    else:
                        response['encoded_file'].extend(add_delay(int(default_delay)))

    return response


def add_delay(delay_value):

    delay_return = []

    # divide by 255 add that many 0xff
    # convert the reminder to hex
    # e.g. 750 = FF FF F0
    while delay_value > 0:
        if delay_value > 255:
            delay_return.extend([0x00, 0xFF])
            delay_value -= 255
        else:
            delay_return.extend([0x00, delay_value])
            delay_value = 0
    return delay_return


def encode_script(duck_text, duck_lang, bunny=None):

    lang_dir = os.path.join(os.path.dirname(__file__), 'languages')
    language_dict = os.path.join(lang_dir, '{0}.json'.format(duck_lang))
    lang_file = json.load(open(language_dict, encoding="utf8"))

    try:
        response = parse_text(duck_text, lang_file, bunny)
    except Exception as e:
        return {
            "line_count": 0,
            "encoded_file": [],
            "valid": False,
            "message": "Error parsing duck_text: {0}".format(e)
        }

    return response
