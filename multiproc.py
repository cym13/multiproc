#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2013 Cédric Picard
#
# LICENSE
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
# END_OF_LICENSE
#
"""
Multiprocessing from the command-line.

Usage: multiproc [-h] [-p N] FORMAT

Arguments:
    FORMAT     The command to be run in each process.
               "%s"    input string
               "%n"    number of the process
               "%%"    litteral "%"

Options:
    -h, --help          Print this help and exit
    -p, --process N     Number of processes to be used.
                        Default is the number of CPU

Example: download multiple files where urls.txt contains the urls list

    $ cat urls.txt | multiproc -p 10 "wget %s -O file.%n"
"""

import re
import sys
import subprocess
from multiprocessing import Pool
from docopt import docopt


def replace(fs, param, regex):
    """
    Replace each occurence of the string matched by `regex' by `param' in `fs'.
    """
    search = True
    count = 0
    search = regex.search(fs)
    while search:
        fs = regex.sub(search.groups()[count] + str(param), fs)
        search = regex.search(fs)
        count += 1

    return fs


def function(number, param, fs):
    """
    The function to be given to the pool's workers.
    """
    number_re = re.compile("([^%])%n")

    print("[%s] Start" % number, file=sys.stderr)

    print(fs)
    fs = replace(fs, "'%s'" % param,  re.compile("([^%])%s"))
    fs = replace(fs, number, re.compile("([^%])%n"))
    fs = fs.replace("%%", "%")

    subprocess.call(fs, shell=True, stdout=sys.stdout, stderr=sys.stdout)
    print("[%s] End" % number, file=sys.stderr)


def main():
    args = docopt(__doc__)

    p_process = args["--process"]
    if p_process:
        p_process = int(p_process)
    pool = Pool(p_process)
    pool.starmap(function, [(n, p[:-1], args["FORMAT"])
                            for (n, p) in enumerate(sys.stdin.readlines())])


if __name__ == "__main__":
    main()
