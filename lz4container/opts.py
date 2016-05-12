#
# Copyright 2016 XP Corporation
#

import os.path
from optparse import OptionParser


opt_parser = OptionParser()

opt_parser.add_option('-c', '--createfile',
                      action='store',
                      help="create a new archive"
                      )

opt_parser.add_option('-x', '--extractfile',
                      action='store',
                      help="extract files from an archive",
                      )

opt_parser.usage = '%prog [options] [file]'


def opts_check(options, args):
    '''
    1. check archived file name is ended with '.lz4r'
    2. -x and -c are mutually exclusive
    3. a file or a directory arguments are needed to create an archived file
    '''
    print "options is ", options, "args is ", args
    extractfile = options.extractfile
    createfile = options.createfile
    if extractfile and createfile:
        opt_parser.error("Please run with '-c' OR '-x'")
    elif extractfile:
        if not extractfile.endswith('.lz4r'):
            opt_parser.error("extracted file should be ended with '.lz4r'")
        if len(args):
            opt_parser.error("args are not supported for extracting file")
    elif createfile:
        if not createfile.endswith('.lz4r'):
            opt_parser.error("extracted file should be ended with '.lz4r'")
        if len(args) != 1 or not (os.path.isfile(args[0]) or os.path.isdir(args[0])):
            opt_parser.error("please put an invalid file name or directory name to archive")
