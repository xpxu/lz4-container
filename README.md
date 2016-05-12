lz4 container
===============

overview
========
This tool will use lz4 to archive/extract files.


how to run
==========
Usage: lz4 [options] [file]

Examples:
  lz4 -c archive.lz4r archive  # Create archive.lz4r from archive.
  lz4 -x archive.lz4r          # Extract all files from archive.lz4r.

Options:
  -h, --help       show this help message and exit
  -c, --create     create a new archive
  -x, --extract    extract files from an archive
