#
# Copyright 2016 XP Corporation
#
import lz4
import os.path
from lz4container.opts import (
    opt_parser,
    opts_check
)

def run():
    (options, args) = opt_parser.parse_args()
    opts_check(options, args)
    if options.extractfile:
        extractfile(options.extractfile)
    elif options.createfile:
        createfile(options.createfile, args[0])


def extractfile(archive):
    with open(archive, 'r') as f:
        lZ4_DATA = f.read()
        DATA = lz4.uncompress(lZ4_DATA)
    archive_name = os.path.basename(archive)
    extractfile = archive_name.split('.')[0]
    print 'extractfile is %r' % extractfile
    with open(extractfile, 'w') as f:
        f.write(DATA)

def createfile(archive, file):
    with open(file, 'r') as f:
        DATA = f.read()
        LZ4_DATA = lz4.compress(DATA)
    with open(archive, 'w') as f:
        f.write(LZ4_DATA)
