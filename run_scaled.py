#!/usr/bin/env python3

import argparse
import os
import random
import time

performance_options = "--encoding=rgb --mmap=yes --compress=0"

parser = argparse.ArgumentParser()

parser.add_argument(
    '--scale',
    dest='scaling_factor',
    default=2.0,
    type=float,
    help='Sets the factor the application is scaled by. \
        Fractional scales are supported. It is set to 2 by default.'
)

parser.add_argument(
    '--opengl',
    choices=['auto', 'yes', 'no'],
    default='auto',
    help='Sets whether xpra should use opengl for rendering. \
        If you get rendering errors, \
        especially when the window is resized, try setting it to no. \
        It is set to auto by default.'
)

parser.add_argument(
    '--sleep',
    default=1.0,
    dest='sleeptime',
    type=float,
    help='Sets how many seconds to wait after starting xpra before \
        attaching to the xpra session. It is set to 1 by default. \
        You might need to increase the value if your machine is \
        particularly slow.'
)

parser.add_argument(
    '--input-method',
    choices=['ibus', 'fcitx', 'fcitx5'],
    help='[Experimental] Sets the IME to use in the application.'
)

parser.add_argument('application', nargs='+')
args = parser.parse_args()

resolution = os.popen("xrandr | grep \* | cut -d' ' -f4").read().strip()
displaynum = random.randint(10000, 99999999)
escaped_params = os.popen(
    f"sh -c \"printf '%q ' '{' '.join(args.application)}'\""
).read()

cmd = f'xpra start ":{displaynum}" --xvfb="Xvfb +extension Composite \
-screen 0 {resolution}x24+32 -nolisten tcp -noreset  \
-auth \$XAUTHORITY" --env=GDK_SCALE=1 --env=GDK_DPI_SCALE=1 \
--start-child="{escaped_params}" --exit-with-children'

if args.input_method:
    if args.input_method == 'ibus':
        cmd += ' --start=ibus-daemon --input-method=ibus'
    else:
        cmd += f' --start={args.input_method} --input-method={args.input_method}'

print(cmd)
os.system(cmd)
time.sleep(args.sleeptime)

os.system(
    f'xpra attach ":{displaynum}" \
    "--desktop-scaling={args.scaling_factor}" \
    "--opengl={args.opengl}" {performance_options} || \
    xpra stop ":{displaynum}"'
)