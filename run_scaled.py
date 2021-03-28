#!/usr/bin/env python3

copyright_info = '''\
run-scaled, a Python script to run an X application scaled via Xpra
Copyright (c) 2021, Sam L. Yes <https://github.com/SamLukeYes>

Original bash script:
run_scaled <https://github.com/kaueraal/run_scaled>
Copyright (c) 2017, Alexander Kauer
All rights reserved.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

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

print(copyright_info)

resolution = os.popen("xrandr | grep \\* | cut -d' ' -f4").read().strip()
scaled_resolution = tuple(
    map(
        lambda x: int(int(x) / args.scaling_factor),
        resolution.split('x')
    )
)

displaynum = random.randint(10000, 99999999)
escaped_params = os.popen(
    f"sh -c \"printf '%q ' '{' '.join(args.application)}'\""
).read()

cmd = f'xpra start ":{displaynum}" --xvfb="Xvfb +extension Composite \
-screen 0 {scaled_resolution[0]}x{scaled_resolution[1]}x24+32 \
-nolisten tcp -noreset -auth \\$XAUTHORITY" \
--env=GDK_SCALE=1 --env=GDK_DPI_SCALE=1 \
--start-child="{escaped_params}" --exit-with-children '

if args.input_method:
    if args.input_method == 'ibus':
        cmd += '--start=ibus-daemon --input-method=ibus'
    else:
        cmd += f'--start={args.input_method} --input-method={args.input_method}'

print(cmd)
os.system(cmd)
time.sleep(args.sleeptime)

os.system(
    f'xpra attach ":{displaynum}" \
    "--desktop-scaling={args.scaling_factor}" \
    "--opengl={args.opengl}" {performance_options} || \
    xpra stop ":{displaynum}"'
)