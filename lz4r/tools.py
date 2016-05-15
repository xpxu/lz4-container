
import os.path
from lz4r.opts import (
    opt_parser,
    opts_check
)
from lz4r.lz4rfile import Lz4rFile

def run():
    (options, args) = opt_parser.parse_args()
    opts_check(options, args)
    if options.extractfile:
        Lz4rFile.decompress(options.extractfile)
    elif options.createfile:
        Lz4rFile.compress(args[0], outname=options.createfile)
